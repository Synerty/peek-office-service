from peek_client.papp.PappClientLoader import pappClientLoader
from peek_platform.sw_install.PeekSwInstallManagerBase import PeekSwInstallManagerBase

__author__ = 'synerty'


class PeekSwInstallManager(PeekSwInstallManagerBase):

    def _stopCode(self):
        pappClientLoader.unloadAllPapps()

    def _upgradeCode(self):
        pass

    def _startCode(self):
        pappClientLoader.loadAllPapps()


peekSwInstallManager = PeekSwInstallManager()
