from dependency_injector import containers, providers

from communication.communication import Communication
from models.com_pars_model import CommParsData
from models.main_pars_model import MainParsData
from models.d_actuators_pars_model import UnitsParsData
from visu.screen_creator import ScreenCreator


class Container(containers.DeclarativeContainer):
    communication = providers.Singleton(Communication)
    screen_creator = providers.Singleton(ScreenCreator)
    comm_pars = providers.Singleton(CommParsData)
    main_pars = providers.Singleton(MainParsData)
    units_pars = providers.Singleton(UnitsParsData)
