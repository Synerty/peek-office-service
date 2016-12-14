from peek_client.plugin.PluginClientLoader import pluginClientLoader
from peek_platform.sw_install.PeekSwInstallManagerBase import PeekSwInstallManagerBase

__author__ = 'synerty'


class PeekSwInstallManager(PeekSwInstallManagerBase):

    def _stopCode(self):
        pluginClientLoader.unloadAllPlugins()

    def _upgradeCode(self):
        pass

    def _startCode(self):
        pluginClientLoader.loadAllPlugins()


peekSwInstallManager = PeekSwInstallManager()
