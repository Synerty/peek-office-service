#!/usr/bin/env python
"""
 * run_peek_office_service_build_only.py
 *
 *  Copyright Synerty Pty Ltd 2013
 *
 *  This software is proprietary, you are not free to copy
 *  or redistribute this code in any format.
 *
 *  All rights to this software are reserved by
 *  Synerty Pty Ltd
 *
"""
from pytmpdir.dir_setting import DirSetting
from setproctitle import setproctitle

from peek_plugin_base.PeekVortexUtil import peekOfficeName
from txhttputil.site.FileUploadRequest import FileUploadRequest
from peek_platform.util.LogUtil import setupPeekLogger
from vortex.DeferUtil import vortexLogFailure

setupPeekLogger(peekOfficeName)

from twisted.internet import reactor, defer

import logging

# EXAMPLE LOGGING CONFIG
# Hide messages from vortex
# logging.getLogger('txhttputil.vortex.VortexClient').setLevel(logging.INFO)

# logging.getLogger('peek_office_service_pof.realtime.RealtimePollerEcomProtocol'
#                   ).setLevel(logging.INFO)

logger = logging.getLogger(__name__)

# ------------------------------------------------------------------------------
# Set the parallelism of the database and reactor
reactor.suggestThreadPoolSize(10)

from peek_platform import PeekPlatformConfig


def setupPlatform():
    PeekPlatformConfig.componentName = peekOfficeName
    setproctitle(PeekPlatformConfig.componentName + " build_only")

    # Tell the platform classes about our instance of the PluginSwInstallManager
    from peek_office_service.sw_install.PluginSwInstallManager import (
        PluginSwInstallManager,
    )

    PeekPlatformConfig.pluginSwInstallManager = PluginSwInstallManager()

    # Tell the platform classes about our instance of the PeekSwInstallManager
    from peek_office_service.sw_install.PeekSwInstallManager import (
        PeekSwInstallManager,
    )

    PeekPlatformConfig.peekSwInstallManager = PeekSwInstallManager()

    # Tell the platform classes about our instance of the PeekLoaderBase
    from peek_office_service.plugin.ClientPluginLoader import ClientPluginLoader

    PeekPlatformConfig.pluginLoader = ClientPluginLoader()

    # The config depends on the componentName, order is important
    from peek_office_service.PeekClientConfig import PeekClientConfig

    PeekPlatformConfig.config = PeekClientConfig()

    # Update the version in the config file
    from peek_office_service import __version__

    PeekPlatformConfig.config.platformVersion = __version__

    # Set default logging level
    logging.root.setLevel(PeekPlatformConfig.config.loggingLevel)

    # Initialise the txhttputil Directory object
    DirSetting.defaultDirChmod = PeekPlatformConfig.config.DEFAULT_DIR_CHMOD
    DirSetting.tmpDirPath = PeekPlatformConfig.config.tmpPath
    FileUploadRequest.tmpFilePath = PeekPlatformConfig.config.tmpPath


def main():
    # defer.setDebugging(True)
    # sys.argv.remove(DEBUG_ARG)
    # import pydevd
    # pydevd.settrace(suspend=False)

    setupPlatform()

    # Import remaining components
    from peek_office_service import importPackages

    importPackages()

    # Start client main data observer, this is not used by the plugins
    # (Initialised now, not as a callback)

    # Load all Plugins
    d = defer.succeed(True)
    d.addCallback(lambda _: PeekPlatformConfig.pluginLoader.loadCorePlugins())
    d.addCallback(
        lambda _: PeekPlatformConfig.pluginLoader.loadOptionalPlugins()
    )

    def startedSuccessfully(_):
        logger.info(
            "Peek Office is running, version=%s",
            PeekPlatformConfig.config.platformVersion,
        )
        return _

    d.addErrback(vortexLogFailure, logger, consumeError=True)
    d.addCallback(startedSuccessfully)

    reactor.addSystemEventTrigger(
        "before",
        "shutdown",
        PeekPlatformConfig.pluginLoader.unloadOptionalPlugins,
    )
    reactor.addSystemEventTrigger(
        "before", "shutdown", PeekPlatformConfig.pluginLoader.unloadCorePlugins
    )

    reactor.run()


if __name__ == "__main__":
    main()
