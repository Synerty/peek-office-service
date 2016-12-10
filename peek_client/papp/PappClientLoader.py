import imp
import logging
import os
import sys
from _collections import defaultdict

from peek_client.PeekClientConfig import peekClientConfig
from peek_client.papp.ClientPlatformApi import ClientPlatformApi
from peek_platform.papp import PappLoaderABC
from vortex.PayloadIO import PayloadIO

logger = logging.getLogger(__name__)

class PappClientLoader(PappLoaderABC):
    _instance = None

    def __new__(cls, *args, **kwargs):
        assert cls._instance is None, "PappClientLoader is a singleton, don't construct it"
        cls._instance = PappLoaderABC.__new__(cls)
        return cls._instance

    def __init__(self):
        PappLoaderABC.__init__(self)

        self._pappPath = peekClientConfig.pappSoftwarePath

        self._rapuiEndpointInstancesByPappName = defaultdict(list)
        self._rapuiResourcePathsByPappName = defaultdict(list)
        self._rapuiTupleNamesByPappName = defaultdict(list)


    def unloadPapp(self, pappName):
        oldLoadedPapp = self._loadedPapps.get(pappName)

        if not oldLoadedPapp:
            return

        # Remove the registered endpoints
        for endpoint in self._rapuiEndpointInstancesByPappName[pappName]:
            PayloadIO().remove(endpoint)
        del self._rapuiEndpointInstancesByPappName[pappName]


        # Remove the registered tuples
        removeTuplesForTupleNames(self._rapuiTupleNamesByPappName[pappName])
        del self._rapuiTupleNamesByPappName[pappName]

        self._unloadPappPackage(pappName, oldLoadedPapp)


    def _loadPappThrows(self, pappName):
        self.unloadPapp(pappName)

        pappDirName = peekClientConfig.pappDevelDir(pappName)

        if not pappDirName:
            logger.warning("Papp dir name for %s is missing, loading skipped",
                           pappName)
            return

        # Make note of the initial registrations for this papp
        endpointInstancesBefore = set(PayloadIO().endpoints)
        tupleNamesBefore = set(registeredTupleNames())

        # Everyone gets their own instance of the papp API
        agentPlatformApi = ClientPlatformApi()

        srcDir = os.path.join(self._pappPath, pappDirName, 'cpython')
        modPath = os.path.join(srcDir, pappName, "PappAgentMain.py")
        if not os.path.exists(modPath) and os.path.exists(modPath + "c"): # .pyc
            PappAgentMainMod = imp.load_compiled('%s.PappAgentMain' % pappName,
                                                modPath + 'c')
        else:
            PappAgentMainMod = imp.load_source('%s.PappAgentMain' % pappName,
                                                modPath)

        peekClient = PappAgentMainMod.PappAgentMain(agentPlatformApi)

        sys.path.append(srcDir)

        self._loadedPapps[pappName] = peekClient
        peekClient.start()
        sys.path.pop()

        # Make note of the final registrations for this papp
        self._rapuiEndpointInstancesByPappName[pappName] = list(
            set(PayloadIO().endpoints) - endpointInstancesBefore)

        # self._rapuiResourcePathsByPappName[pappName] = list(
        #     set(registeredResourcePaths()) - resourcePathsBefore)
        #
        self._rapuiTupleNamesByPappName[pappName] = list(
            set(registeredTupleNames()) - tupleNamesBefore)

        self.sanityCheckAgentPapp(pappName)

    def sanityCheckAgentPapp(self, pappName):
        ''' Sanity Check Papp

        This method ensures that all the things registed for this papp are
        prefixed by it's pappName, EG papp_noop
        '''

        # All endpoint filters must have the 'papp' : 'papp_name' in them
        for endpoint in self._rapuiEndpointInstancesByPappName[pappName]:
            filt = endpoint.filt
            if 'papp' not in filt and filt['papp'] != pappName:
                raise Exception("Payload endpoint does not contan 'papp':'%s'\n%s"
                                % (pappName, filt))

        # all tuple names must start with their pappName
        for tupleName in self._rapuiTupleNamesByPappName[pappName]:
            TupleCls = tupleForTupleName(tupleName)
            if not tupleName.startswith(pappName):
                raise Exception("Tuple name does not start with '%s', %s (%s)"
                                % (pappName, tupleName, TupleCls.__name__))

    def notifyOfPappVersionUpdate(self, pappName, pappVersion):
        logger.info("Received PAPP update for %s version %s", pappName, pappVersion)
        return self.loadPapp(pappName)


pappClientLoader = PappClientLoader()
