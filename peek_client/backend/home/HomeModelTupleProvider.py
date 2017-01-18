import logging

from peek_platform import PeekPlatformConfig
from vortex.Payload import Payload
from vortex.Tuple import addTupleType, Tuple, TupleField
from vortex.TupleSelector import TupleSelector
from vortex.handler.TupleDataObservableHandler import TuplesProviderABC

logger = logging.getLogger(__name__)


@addTupleType
class PluginAppTileTuple(Tuple):
    __tupleType__ = 'peek-client.PluginAppTileTuple'

    name = TupleField(comment="The name of the plugin, EG plugin_noop")
    title = TupleField(comment="The title of the plugin, EG No Op")
    resourcePath = TupleField(comment="The resource path of the plugin")


class HomeAppTileTupleProvider(TuplesProviderABC):

    def makeVortexMsg(self, filt: dict, tupleSelector: TupleSelector) -> bytes:
        tuples = []
        for name, title, path in PeekPlatformConfig.pluginLoader.pluginFrontendTitleUrls:
            tuples.append(PluginAppTileTuple(name=name,
                                             title=title,
                                             resourcePath=path))

        return Payload(filt=filt, tuples=tuples).toVortexMsg()
