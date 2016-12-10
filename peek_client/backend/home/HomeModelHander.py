from vortex.Tuple import addTupleType, Tuple, TupleField

from vortex.handler.ModelHandler import ModelHandler

filt = {'papp': 'peek_client',
        'key': 'home.apps'}


@addTupleType
class PappAppTileTuple(Tuple):
    __tupleType__ = 'peek_client.PappAppTileTuple'

    name = TupleField(comment="The name of the papp, EG papp_noop")
    title = TupleField(comment="The title of the papp, EG No Op")
    resourcePath = TupleField(comment="The resource path of the papp")


class HomeModelHander(ModelHandler):
    def buildModel(self, payload=None, **kwargs):
        from peek_client.papp.PappClientLoader import pappClientLoader
        data = []
        for name, title, path in pappClientLoader.pappFrontendTitleUrls:
            data.append(
                PappAppTileTuple(name=name,
                                 title=title,
                                 resourcePath=path))

        return data


homeModelHandler = HomeModelHander(filt)
