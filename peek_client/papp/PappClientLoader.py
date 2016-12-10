import logging
from typing import Type

from papp_base.PappCommonEntryHookABC import PappCommonEntryHookABC
from papp_base.client.PappClientEntryHookABC import PappClientEntryHookABC
from peek_client.papp.PeekClientPlatformHook import PeekClientPlatformHook
from peek_platform.papp import PappLoaderABC
from peek_platform.papp.PappFrontendInstallerABC import PappFrontendInstallerABC

logger = logging.getLogger(__name__)


class PappClientLoader(PappLoaderABC, PappFrontendInstallerABC):
    _instance = None

    def __new__(cls, *args, **kwargs):
        assert cls._instance is None, "PappClientLoader is a singleton, don't construct it"
        cls._instance = PappLoaderABC.__new__(cls)
        return cls._instance

    def __init__(self, *args, **kwargs):
        PappLoaderABC.__init__(self, *args, **kwargs)
        PappFrontendInstallerABC.__init__(self, *args, platformService="client", **kwargs)

    def loadAllPapps(self):
        PappLoaderABC.loadAllPapps(self)
        self.buildFrontend()

    @property
    def _entryHookFuncName(self) -> str:
        return "peekClientEntryHook"

    @property
    def _entryHookClassType(self):
        return PappClientEntryHookABC

    @property
    def _platformServiceNames(self) -> [str]:
        return ["client"]

    def _loadPappThrows(self, pappName: str, EntryHookClass: Type[PappCommonEntryHookABC],
                        pappRootDir: str) -> None:
        # Everyone gets their own instance of the papp API
        platformApi = PeekClientPlatformHook()

        pappMain = EntryHookClass(pappName=pappName,
                                  pappRootDir=pappRootDir,
                                  platform=platformApi)

        # Load the papp
        pappMain.load()

        # Start the Papp
        pappMain.start()

        # Add all the resources required to serve the backend site
        # And all the papp custom resources it may create
        from peek_client.backend.SiteRootResource import root as siteRootResource
        siteRootResource.putChild(pappName.encode(), platformApi.rootResource)

        self._loadedPapps[pappName] = pappMain


pappClientLoader = PappClientLoader()
