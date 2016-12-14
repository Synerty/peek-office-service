from peek_client.plugin.ClientPluginLoader import clientPluginLoader
from peek_platform.sw_install.PluginSwInstallManagerBase import PluginSwInstallManagerBase


class PluginSwInstallManager(PluginSwInstallManagerBase):
    def notifyOfPluginVersionUpdate(self, pluginName, targetVersion):
        clientPluginLoader.loadPlugin(pluginName)


pluginSwInstallManager = PluginSwInstallManager()
