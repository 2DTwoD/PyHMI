from utils.structures import ValueWithChangeFlag


class DActuatorData:
    def __init__(self):
        self.changed = ValueWithChangeFlag(False)
        self.start = ValueWithChangeFlag(False)
        self.auto = ValueWithChangeFlag(False)
        self.modeling = ValueWithChangeFlag(False)
        self.service = ValueWithChangeFlag(False)
        self.err_reset = ValueWithChangeFlag(False)
        self.status = ValueWithChangeFlag(0)
        self.auto_start = ValueWithChangeFlag(0)
        self.auto_start_mask = ValueWithChangeFlag(0)
        self.auto_stop = ValueWithChangeFlag(0)
        self.auto_stop_mask = ValueWithChangeFlag(0)
        self.locks = ValueWithChangeFlag(0)
        self.locks_mask = ValueWithChangeFlag(0)
        self.errors = ValueWithChangeFlag(0)
        self.errors_mask = ValueWithChangeFlag(0)
        self.fb_on_err_delay = ValueWithChangeFlag(0)
        self.fb_off_err_delay = ValueWithChangeFlag(0)
    def __str__(self):
        return f"changed: {self.changed}, start: {self.start}, auto: {self.auto}," \
               f"modeling: {self.modeling}, service: {self.service}, err_reset: {self.err_reset}, " \
               f"status: {self.status},auto_start: {self.auto_start}, auto_start_mask: {self.auto_start_mask}," \
               f"auto_stop: {self.auto_stop}, auto_stop_mask: {self.auto_stop_mask}," \
               f"locks: {self.locks}, locks_mask: {self.locks_mask}," \
               f"errors: {self.errors}, errors_mask: {self.errors_mask}," \
               f"fb_on_err_delay: {self.fb_on_err_delay}, fb_off_err_delay: {self.fb_off_err_delay}"


 # Comm structure:
 # WORD0:
     # Byte0:
         # Bit0: CHANGED
         # Bit1: START
         # Bit2: AUTO
         # Bit3: MODELING
         # Bit4: ERR_RESET
     # Byte1: STATUS
 # WORD1:
     # Byte0: AUTO_START
     # Byte1: AUTO_START_MASK
 # WORD2:
     # Byte0: AUTO_STOP
     # Byte1: AUTO_STOP_MASK
 # WORD3:
     # Byte0: LOCKS
     # Byte1: LOCKS_MASK
 # WORD4:
     # Byte0: ERRORS
     # Byte1: ERRORS_MASK
 # WORD5: FB_ON_ERR_DELAY
 # WORD6: FB_OFF_ERR_DELAY
