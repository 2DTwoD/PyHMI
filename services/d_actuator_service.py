from models.d_actuator_model import DActuatorData
import di_conf.container as DI


class DActuatorService(DActuatorData):
    def __init__(self, start_address: int, end_address: int):
        super().__init__()
        self.comm = DI.Container.communication()
        assert end_address - start_address == 7, "address length must be 7 words"
        self.start_address = start_address
        self.end_address = end_address

    def update(self):
        data = self.comm.get_data(self.start_address, self.end_address)
        self.changed = data[0] and 0x1 > 0
        self.start = data[0] and 0x2 > 0
        self.auto = data[0] and 0x4 > 0
        self.modeling = data[0] and 0x8 > 0
        self.err_reset = data[0] and 0x10 > 0
        self.status = data[0] >> 8
        self.auto_start = data[1] and 0xff
        self.auto_start_mask = data[1] >> 8
        self.auto_stop = data[2] and 0xff
        self.auto_stop_mask = data[2] >> 8
        self.locks = data[3] and 0xff
        self.locks_mask = data[3] >> 8
        self.errors = data[4] and 0xff
        self.errors_mask = data[4] >> 8
        self.fb_on_err_delay = data[5]
        self.fb_off_err_delay = data[6]
