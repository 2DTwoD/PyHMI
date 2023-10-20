import di_conf.container as DI
from services.common_service import CommonService
from services.d_actuator_plc_service import DActuatorPLCService
from utils.structures import Area, ValueWithChangeFlag, Coordinate, Dimension
from visu.d_actuator_window import DActuatorWindow
from visu.status_bar import StatusBarType1


class DActuator:
    def __init__(self, name: str):
        self.sc = DI.Container.screen_creator()
        self.da_pars = DI.Container.da_pars()
        self.common = DI.Container.common()
        self.name = name
        self._object_on_screen = False
        self.status_imgs = [self.da_pars.get_name_img(name, 'stop'),
                            self.da_pars.get_name_img(name, 'start'),
                            self.da_pars.get_name_img(name, 'intermediate'),
                            self.da_pars.get_name_img(name, 'alarm')]
        self.location = self.da_pars.get_location(name)
        self.image_dimension = self.da_pars.get_dimension(name)
        self.status_bar_for_screen = StatusBarType1(self.sc.screen, Dimension(15, 15))
        self.plc_data = DActuatorPLCService(self.da_pars.get_start_address(name))
        self.click_area = Area()
        self.window = None
        self.change_screen()

    def update(self, not_update_now: bool = True):
        self.plc_data.receive()
        for par in self.plc_data.iteration:
            self.change_visu(par, not_update_now)

    def change_screen(self):
        self._object_on_screen = self.sc.current_screen in self.location
        self.update(False)
        self.status_bar_for_screen.place_forget()
        if self._object_on_screen:
            x = self.location[self.sc.current_screen].x
            y = self.location[self.sc.current_screen].y
            self.status_bar_for_screen.place(x=x - self.status_bar_for_screen.width() / 2,
                                             y=y + self.image_dimension.height / 2)
            self.click_area.update(y - self.image_dimension.height / 2, y + self.image_dimension.height / 2,
                                   x - self.image_dimension.width / 2, x + self.image_dimension.width / 2)

    def left_click(self, mouse: Coordinate):
        if self.click_area.left < mouse.x < self.click_area.right and \
                self.click_area.down > mouse.y > self.click_area.up:
            if self._window_closed():
                self.window = DActuatorWindow(self.name, self.plc_data)
                self.update(not_update_now=False)
            else:
                self.window.popup()

    def _window_closed(self):
        return self.window is None or len(self.window.children) == 0

    def change_visu(self, par: ValueWithChangeFlag, not_update_now: bool = True):
        if par.is_not_changed() and not_update_now:
            return
        if self._object_on_screen:
            self._change_background_visu(par)
            self.status_bar_for_screen.change_visu(par)
        if not self._window_closed():
            self.window.change_visu(par)

    def _change_background_visu(self, par: ValueWithChangeFlag):
        match par.name:
            case 'status':
                location = self.location[self.sc.current_screen]
                self.sc.screen_add_image(self.status_imgs[par.get()], location, origin='center')
