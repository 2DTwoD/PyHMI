import json
import threading
from types import SimpleNamespace

from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusException
from pymodbus.pdu import ExceptionResponse
from pymodbus.transaction import ModbusSocketFramer


class Communication(threading.Thread):
    def __init__(self):
        self.test = 1
        threading.Thread.__init__(self)
        self.thread_name = "communication_thread"
        self.host = "init"
        self.port = 0
        self.run_bit = True
        self.client = None

        self.count = 0
        self.max_count = 10

        self.min_reg = 0
        self.max_reg = 30
        self.cur_reg = 0
        self.comm_data = [0] * self.max_reg
        with open('res/configuration/comm.txt') as comm_config_json:
            comm_config = json.loads(comm_config_json.read(), object_hook=lambda d: SimpleNamespace(**d))
            self.host = comm_config.host
            self.port = comm_config.port
        self.start()

    def run(self):
        while self.run_bit:
            self.run_client()
        self.close()

    def run_client(self):
        self.close()
        self.client = ModbusTcpClient(host=self.host, port=self.port, framer=ModbusSocketFramer)
        self.client.connect()
        if not self.client.connected:
            print("No modbus connection")
            return
        try:
            while self.run_bit:

                if self.cur_reg + self.count > self.max_reg:
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
                    self.comm_data[index] = data.registers[index - self.cur_reg]
                print(self.comm_data)
                self.cur_reg += self.count
                if self.cur_reg >= self.max_reg:
                    self.cur_reg = self.min_reg

        except ModbusException as exc:
            print(f"Received ModbusException({exc}) from library")
            return

    def write(self):
        self.client.write_registers(0, list(range(self.test, self.test + 120)), slave=1)
        print("write" + str(self.test))
        self.test += 1

    def close(self):
        if self.client is not None:
            self.client.close()

    def end(self):
        self.run_bit = False

