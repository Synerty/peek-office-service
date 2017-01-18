import logging

from peek_client.backend.home.HomeModelTupleProvider import HomeAppTileTupleProvider, \
    PluginAppTileTuple
from vortex.handler.TupleDataObservableHandler import TupleDataObservableHandler

logger = logging.getLogger(__name__)

peekClientObservableName = "peek_client"

observable = TupleDataObservableHandler(
    observableName=peekClientObservableName,
    additionalFilt={"plugin": "peek_client"},
    subscriptionsEnabled=True)

observable.addTupleProvider(PluginAppTileTuple.tupleName(), HomeAppTileTupleProvider())
