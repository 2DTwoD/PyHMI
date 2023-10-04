import threading

from models.d_actuator_model import DActuatorData
import di_conf.container as DI


class DActuatorPLCService(DActuatorData):
    def __init__(self, start_address: int):
        DActuatorData.__init__(self)
        self.comm = DI.Container.communication()
        self.start_address = start_address
        self.end_address = start_address + 7
        self.send_flag = False

    def receive(self):
        data = self.comm.get_data(self.start_address, self.end_address)
        self.start.set(data[0] & 0x2 > 0)
        self.auto.set(data[0] & 0x4 > 0)
        self.modeling.set(data[0] & 0x8 > 0)
        self.service.set(data[0] & 0x10 > 0)
        self.err_reset.set(data[0] & 0x20 > 0)
        self.status.set(data[0] >> 8)
        self.auto_start.set(data[1] & 0xff)
        self.auto_start_mask.set(data[1] >> 8)
        self.auto_stop.set(data[2] & 0xff)
        self.auto_stop_mask.set(data[2] >> 8)
        self.locks.set(data[3] & 0xff)
        self.locks_mask.set(data[3] >> 8)
        self.errors.set(data[4] & 0xff)
        self.errors_mask.set(data[4] >> 8)
        self.fb_on_err_delay.set(data[5])
        self.fb_off_err_delay.set(data[6])

    def send(self):
        data = [0] * 7
        data[0] = 1 | (self.start.get() << 1) | (self.auto.get() << 2) | (self.modeling.get() << 3) | \
                  (self.service.get() << 4) | (self.err_reset.get() << 5)
        data[0] |= (self.status.get() << 8)
        data[1] |= self.auto_start.get()
        data[1] |= (self.auto_start_mask.get() << 8)
        data[2] |= self.auto_stop.get()
        data[2] |= (self.auto_stop_mask.get() << 8)
        data[3] |= self.locks.get()
        data[3] |= (self.locks_mask.get() << 8)
        data[4] |= self.errors.get()
        data[4] |= (self.errors_mask.get() << 8)
        data[5] = self.fb_on_err_delay.get()
        data[6] = self.fb_off_err_delay.get()
        self.comm.send(self.start_address, data)
