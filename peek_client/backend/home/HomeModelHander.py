from vortex.Tuple import addTupleType, Tuple, TupleField

from vortex.handler.ModelHandler import ModelHandler

filt = {'plugin': 'peek_client',
        'key': 'home.apps'}


@addTupleType
class PluginAppTileTuple(Tuple):
    __tupleType__ = 'peek_client.PluginAppTileTuple'

    name = TupleField(comment="The name of the plugin, EG plugin_noop")
    title = TupleField(comment="The title of the plugin, EG No Op")
    resourcePath = TupleField(comment="The resource path of the plugin")


class HomeModelHander(ModelHandler):
    def buildModel(self, payload=None, **kwargs):
        from peek_client.plugin.PluginClientLoader import pluginClientLoader
        data = []
        for name, title, path in pluginClientLoader.pluginFrontendTitleUrls:
            data.append(
                PluginAppTileTuple(name=name,
                                 title=title,
                                 resourcePath=path))

        return data


homeModelHandler = HomeModelHander(filt)
