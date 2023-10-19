from utils.structures import NameImage, Dimension


class CommonService:
    ALARM = 0
    NO_ALARM = 1
    SERVICE = 2
    NO_SERVICE = 3
    LOCKED = 4
    UNLOCKED = 5

    def get_token(self, token: int, dimension: Dimension = Dimension(0, 0)):
        match token:
            case CommonService.ALARM:
                return NameImage(name="alarm_token", image_path='res/pics/common/alarm.png', dimension=dimension)
            case CommonService.NO_ALARM:
                return NameImage(name="alarm_token", image_path='res/pics/common/no_alarm.png', dimension=dimension)
            case CommonService.SERVICE:
                return NameImage(name="service_token", image_path='res/pics/common/service.png', dimension=dimension)
            case CommonService.NO_SERVICE:
                return NameImage(name="service_token", image_path='res/pics/common/no_service.png', dimension=dimension)
            case CommonService.LOCKED:
                return NameImage(name="locked_token", image_path='res/pics/common/locked.png', dimension=dimension)
            case CommonService.UNLOCKED:
                return NameImage(name="locked_token", image_path='res/pics/common/unlocked.png', dimension=dimension)



