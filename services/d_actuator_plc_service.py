from models.d_actuator_model import DActuatorData
import di_conf.container as DI


class DActuatorPLCService(DActuatorData):
    def __init__(self, start_address: int):
        DActuatorData.__init__(self)
        self.comm = DI.Container.communication()
        self.start_address = start_address
        self.end_address = start_address + 7

    def update(self):
        data = self.comm.get_data(self.start_address, self.end_address)
        self.changed.set(data[0] & 0x1 > 0)
        self.start.set(data[0] & 0x2 > 0)
        self.auto.set(data[0] & 0x4 > 0)
        self.modeling.set(data[0] & 0x8 > 0)
        self.err_reset.set(data[0] & 0x10 > 0)
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
