import di_conf.container as DI
from services.d_actuator_plc_service import DActuatorPLCService
from utils.structures import Area
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
        self.alarm_tokens = [self.common.alarm_token,
                             self.common.no_service_token]
        self.service_tokens = [self.common.service_token,
                               self.common.no_service_token]
        self.lock_tokens = [self.common.locked_token,
                            self.common.unlocked_token]
        self.location = self.da_pars.get_location(name)
        self._old_img = None
        self.image_dimension = self.da_pars.get_dimension(name)
        self.plc_data = DActuatorPLCService(self.da_pars.get_start_address(name))
        self.click_area = Area()
        self.window = None
        self.change_screen()

    def update(self):
        self.plc_data.receive()
        if self.plc_data.status.is_changed():
            self._change_status()

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
            else:
                self.window.popup()

    def _window_closed(self):
        return self.window is None or len(self.window.children) == 0

    def _change_status(self):
        location = self.location[self.sc.current_screen]
        self.sc.screen_add_image(location.x, location.y, self.status_imgs[self.plc_data.status.get()])
        if not self._window_closed():
            self.window.set_status(self.plc_data.status.get())
