from peek_client.plugin.ClientPluginLoader import clientPluginLoader
from peek_platform.sw_install.PluginSwInstallManagerABC import PluginSwInstallManagerABC


class PluginSwInstallManager(PluginSwInstallManagerABC):
    def notifyOfPluginVersionUpdate(self, pluginName, targetVersion):
        clientPluginLoader.loadPlugin(pluginName)


pluginSwInstallManager = PluginSwInstallManager()
