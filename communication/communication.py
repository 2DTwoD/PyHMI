import threading
import time

from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusException
from pymodbus.pdu import ExceptionResponse
from pymodbus.transaction import ModbusSocketFramer
import di_conf.container as DI

from utils.structures import CommPair


class Communication(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self, name="communication_thread", daemon=True)
        self.max_count = 100
        self.count = self.max_count

        self.cur_reg = 0
        self.min_reg = 0
        self.max_reg = 15
        self.read_data = [0] * self.max_reg
        self.comm_pair = CommPair()
        self.send_flag = False
        self._connect_flag = False
        self._com_par = DI.Container.comm_pars()
        self.update_period = self._com_par.update_period / 1000.0
        self.client = ModbusTcpClient(host=self._com_par.host, port=self._com_par.port, framer=ModbusSocketFramer)
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
                print(self.read_data)

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


