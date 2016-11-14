from peek_client.papp.PappClientLoader import pappClientLoader
from peek_platform.sw_install.PappSwInstallManagerBase import PappSwInstallManagerBase


class PappSwInstallManager(PappSwInstallManagerBase):
    def notifyOfPappVersionUpdate(self, pappName, targetVersion):
        pappClientLoader.loadPapp(pappName)


pappSwInstallManager = PappSwInstallManager()
