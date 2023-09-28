import json
import threading
import time
from types import SimpleNamespace

from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusException
from pymodbus.pdu import ExceptionResponse
from pymodbus.transaction import ModbusSocketFramer

from utils.structures import CommPair


class Communication(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self, name="communication_thread", daemon=True)
        self.host = "init"
        self.port = 0
        self.client = None

        self.max_count = 100
        self.count = self.max_count

        self.cur_reg = 0
        self.min_reg = 0
        self.max_reg = 15
        self.read_data = [0] * self.max_reg
        self.comm_pair = CommPair()
        self.send_flag = False
        self._connect_flag = False
        with open('res/configuration/comm.txt') as comm_config_json:
            comm_config = json.loads(comm_config_json.read(), object_hook=lambda d: SimpleNamespace(**d))
            self.host = comm_config.host
            self.port = comm_config.port
            self.update_period = comm_config.update_period / 1000.0
        self.client = ModbusTcpClient(host=self.host, port=self.port, framer=ModbusSocketFramer)
        self.start()

    def run(self):
        while True:
            self.run_client()

    def run_client(self):
        self.close()
        time.sleep(1)
        self.client.connect()
        if not self.client.connected:
            print("No modbus connection")
            return
        try:
            while True:
                if self.cur_reg + self.count >= self.max_reg:
                    self.count = self.max_reg - self.cur_reg
                else:
                    self.count = self.max_count
                data = self.client.read_holding_registers(self.cur_reg, self.count, slave=1)
                if data.isError():
                    print(f"Received Modbus library error({data})")
                    return
                if isinstance(data, ExceptionResponse):
                    print(f"Received Modbus library exception ({data})")
                    return

                for index in range(self.cur_reg, self.cur_reg + self.count):
                    self.read_data[index] = data.registers[index - self.cur_reg]
                self.cur_reg += self.count
                if self.cur_reg >= self.max_reg:
                    self.cur_reg = self.min_reg

                if self.comm_pair.data_ready:
                    self.client.write_registers(self.comm_pair.get["address"], self.comm_pair.get["data"], slave=1)
                self._connect_flag = True
                time.sleep(self.update_period)

        except ModbusException as exc:
            print(f"Received ModbusException({exc}) from library")
            return

    def send(self, address=None, data=None):
        if address is None or data is None:
            return
        self.comm_pair.new_data(address, data)

    def get_data(self, start_address: int, end_address: int):
        return self.read_data[start_address: end_address]

    def close(self):
        self._connect_flag = False
        if self.client is not None and self.client.connected:
            self.client.close()

    @property
    def connected(self):
        return self._connect_flag


