from dependency_injector import containers, providers

from communication.communication import Communication
from services.com_pars_service import CommParsService
from services.common_service import CommonService
from services.d_actuators_pars_service import DActuatorsParsService
from services.main_pars_service import MainParsService
from visu.screen_creator import ScreenCreator


class Container(containers.DeclarativeContainer):
    main_pars = providers.Singleton(MainParsService)
    comm_pars = providers.Singleton(CommParsService)
    da_pars = providers.Singleton(DActuatorsParsService)
    common = providers.Singleton(CommonService)
    communication = providers.Singleton(Communication)
    screen_creator = providers.Singleton(ScreenCreator)
