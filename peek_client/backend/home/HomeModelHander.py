from vortex.handler.ModelHandler import ModelHandler

filt = {'papp': 'peek_client',
        'key': 'home.apps'}


class HomeModelHander(ModelHandler):
    def buildModel(self, payload=None, **kwargs):
        data = []

        for x in range(5):
            data.append({'title': 'Papp %s' % x,
                         'name': 'papp_x%s' % x})

        return data


homeModelHandler = HomeModelHander(filt)
