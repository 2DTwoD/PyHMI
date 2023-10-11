import di_conf.container as DI
from services.d_actuator_plc_service import DActuatorPLCService
from utils.structures import Area, ValueWithChangeFlag
from visu.d_actuator_window import DActuatorWindow


class DActuator:
    def __init__(self, name: str):
        self.sc = DI.Container.screen_creator()
        self.da_pars = DI.Container.da_pars()
        self.common = DI.Container.common()
        self.name = name
        self.status_imgs = [self.da_pars.get_name_img(name, 'stop'),
                            self.da_pars.get_name_img(name, 'start'),
                            self.da_pars.get_name_img(name, 'intermediate'),
                            self.da_pars.get_name_img(name, 'alarm')]
        self.alarm_tokens = [self.common.no_alarm_token,
                             self.common.alarm_token]
        self.lock_tokens = [self.common.unlocked_token,
                            self.common.locked_token]
        self.service_tokens = [self.common.no_service_token,
                               self.common.service_token]
        self.location = self.da_pars.get_location(name)
        self.image_dimension = self.da_pars.get_dimension(name)
        self.plc_data = DActuatorPLCService(self.da_pars.get_start_address(name))
        self.click_area = Area()
        self.window = None
        self.change_screen()

    def update(self, not_update_now: bool = True):
        self.plc_data.receive()
        for par in self.plc_data.iteration:
            self.change_visu(par, not_update_now)

    def change_screen(self):
        if self.sc.current_screen in self.location:
            x = self.location[self.sc.current_screen].x
            y = self.location[self.sc.current_screen].y
            self.sc.screen_add_image(x, y, self.status_imgs[self.plc_data.status.get()])
            self.click_area.update(y - self.image_dimension.height / 2, y + self.image_dimension.height / 2,
                                   x - self.image_dimension.width / 2, x + self.image_dimension.width / 2)

    def left_click(self, mouse_x, mouse_y):
        if self.click_area.left < mouse_x < self.click_area.right and \
                self.click_area.down > mouse_y > self.click_area.up:
            if self._window_closed():
                self.window = DActuatorWindow(self.name, self)
                self.update(not_update_now=False)
            else:
                self.window.popup()

    def _window_closed(self):
        return self.window is None or len(self.window.children) == 0

    def change_visu(self, par: ValueWithChangeFlag, not_update_now: bool = True):
        if par.is_not_changed() and not_update_now:
            return
        self._change_background_visu(par)
        if not self._window_closed():
            self.window.change_visu(par)

    def _change_background_visu(self, par: ValueWithChangeFlag):
        match par.name:
            case 'status':
                location = self.location[self.sc.current_screen]
                self.sc.screen_add_image(location.x, location.y, self.status_imgs[par.get()])
