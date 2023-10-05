from utils.structures import ValueWithChangeFlag


class DActuatorData:
    def __init__(self):
        self.changed = ValueWithChangeFlag(value=False, name="changed")
        self.start = ValueWithChangeFlag(value=False, name="start")
        self.auto = ValueWithChangeFlag(value=False, name="auto")
        self.modeling = ValueWithChangeFlag(value=False, name="modeling")
        self.alarm = ValueWithChangeFlag(value=False, name="alarm")
        self.locked = ValueWithChangeFlag(value=False, name="locked")
        self.service = ValueWithChangeFlag(value=False, name="service")
        self.err_reset = ValueWithChangeFlag(value=False, name="err_reset")
        self.status = ValueWithChangeFlag(value=0, name="status")
        self.auto_start = ValueWithChangeFlag(value=0, name="auto_start")
        self.auto_start_mask = ValueWithChangeFlag(value=0, name="auto_start_mask")
        self.auto_stop = ValueWithChangeFlag(value=0, name="auto_stop")
        self.auto_stop_mask = ValueWithChangeFlag(value=0, name="auto_stop_mask")
        self.locks = ValueWithChangeFlag(value=0, name="locks")
        self.locks_mask = ValueWithChangeFlag(value=0, name="locks_mask")
        self.errors = ValueWithChangeFlag(value=0, name="errors")
        self.errors_mask = ValueWithChangeFlag(value=0, name="errors_mask")
        self.fb_on_err_delay = ValueWithChangeFlag(value=0, name="fb_on_err_delay")
        self.fb_off_err_delay = ValueWithChangeFlag(value=0, name="fb_off_err_delay")
    def __str__(self):
        return f"changed: {self.changed}, start: {self.start}, auto: {self.auto}," \
               f"modeling: {self.modeling}, alarm: {self.alarm}, locked: {self.locked}, " \
               f"service: {self.service}, err_reset: {self.err_reset}, " \
               f"status: {self.status},auto_start: {self.auto_start}, auto_start_mask: {self.auto_start_mask}," \
               f"auto_stop: {self.auto_stop}, auto_stop_mask: {self.auto_stop_mask}," \
               f"locks: {self.locks}, locks_mask: {self.locks_mask}," \
               f"errors: {self.errors}, errors_mask: {self.errors_mask}," \
               f"fb_on_err_delay: {self.fb_on_err_delay}, fb_off_err_delay: {self.fb_off_err_delay}"

