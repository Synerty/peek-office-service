from peek_client.papp.PappClientLoader import pappClientLoader
from peek_platform import PappSwInstallManagerBase


class PappSwInstallManager(PappSwInstallManagerBase):
    def notifyOfPappVersionUpdate(self, pappName, targetVersion):
        pappClientLoader.loadPapp(pappName)


pappSwInstallManager = PappSwInstallManager()
