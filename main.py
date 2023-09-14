import json
import sys
from types import SimpleNamespace

from communication.communication import Communication
from di_conf.container import Container


container = Container()
container.wire(modules=[sys.modules[__name__]])
sc = Container.screen_creator()
sc.start()
