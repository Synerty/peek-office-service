from peek_client.plugin.ClientPluginLoader import clientPluginLoader
from peek_platform.sw_install.PeekSwInstallManagerBase import PeekSwInstallManagerBase

__author__ = 'synerty'


class PeekSwInstallManager(PeekSwInstallManagerBase):

    def _stopCode(self):
        clientPluginLoader.unloadAllPlugins()

    def _upgradeCode(self):
        pass

    def _startCode(self):
        clientPluginLoader.loadAllPlugins()


peekSwInstallManager = PeekSwInstallManager()
