from dependency_injector import containers, providers

from communication.communication import Communication
from visu.screen_creator import ScreenCreator


class Container(containers.DeclarativeContainer):
    communication = providers.Singleton(Communication)
    screen_creator = providers.Singleton(ScreenCreator)
