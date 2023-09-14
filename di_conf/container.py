from dependency_injector import containers, providers

from visu.screen_creator import ScreenCreator


class Container(containers.DeclarativeContainer):

    screen_creator = providers.Singleton(ScreenCreator)
