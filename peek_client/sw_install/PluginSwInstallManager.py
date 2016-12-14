from peek_client.plugin.PluginClientLoader import pluginClientLoader
from peek_platform.sw_install.PluginSwInstallManagerBase import PluginSwInstallManagerBase


class PluginSwInstallManager(PluginSwInstallManagerBase):
    def notifyOfPluginVersionUpdate(self, pluginName, targetVersion):
        pluginClientLoader.loadPlugin(pluginName)


pluginSwInstallManager = PluginSwInstallManager()
