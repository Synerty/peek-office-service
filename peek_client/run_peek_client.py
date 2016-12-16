#!/usr/bin/env python
"""
 * synnova.py
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
from pytmpdir.Directory import DirSettings
from twisted.internet.defer import succeed
from txhttputil.site.FileUploadRequest import FileUploadRequest
from txhttputil.site.SiteUtil import setupSite
from txhttputil.util.DeferUtil import printFailure
from txhttputil.util.LoggingUtil import setupLogging


setupLogging()

from twisted.internet import reactor

import logging

# EXAMPLE LOGGING CONFIG
# Hide messages from vortex
# logging.getLogger('txhttputil.vortex.VortexClient').setLevel(logging.INFO)

# logging.getLogger('peek_client_pof.realtime.RealtimePollerEcomProtocol'
#                   ).setLevel(logging.INFO)

logger = logging.getLogger(__name__)

# ------------------------------------------------------------------------------
# Set the parallelism of the database and reactor
reactor.suggestThreadPoolSize(10)


def setupPlatform():
    from peek_platform import PeekPlatformConfig
    PeekPlatformConfig.componentName = "peek-client"

    # Tell the platform classes about our instance of the PluginSwInstallManager
    from peek_client.sw_install.PluginSwInstallManager import pluginSwInstallManager
    PeekPlatformConfig.pluginSwInstallManager = pluginSwInstallManager

    # Tell the platform classes about our instance of the PeekSwInstallManager
    from peek_client.sw_install.PeekSwInstallManager import peekSwInstallManager
    PeekPlatformConfig.peekSwInstallManager = peekSwInstallManager

    # Tell the platform classes about our instance of the PeekLoaderBase
    from peek_client.plugin.ClientPluginLoader import clientPluginLoader
    PeekPlatformConfig.pluginLoader = clientPluginLoader

    # The config depends on the componentName, order is important
    from peek_client.PeekClientConfig import peekClientConfig
    PeekPlatformConfig.config = peekClientConfig

    # Set default logging level
    logging.root.setLevel(peekClientConfig.loggingLevel)

    # Initialise the txhttputil Directory object
    DirSettings.defaultDirChmod = peekClientConfig.DEFAULT_DIR_CHMOD
    DirSettings.tmpDirPath = peekClientConfig.tmpPath
    FileUploadRequest.tmpFilePath = peekClientConfig.tmpPath


def main():
    # defer.setDebugging(True)
    # sys.argv.remove(DEBUG_ARG)
    # import pydevd
    # pydevd.settrace(suspend=False)

    setupPlatform()

    # Import remaining components
    from peek_client import importPackages
    importPackages()

    # Load server restart handler handler
    from peek_platform import PeekServerRestartWatchHandler
    PeekServerRestartWatchHandler.__unused = False

    # First, setup the Vortex Agent
    from peek_platform.PeekVortexClient import peekVortexClient
    d = peekVortexClient.connect()
    d.addErrback(printFailure)

    # # Start Update Handler,
    # from peek_platform.sw_version.PeekSwVersionPollHandler import peekSwVersionPollHandler
    # # Add both, The peek client might fail to connect, and if it does, the payload
    # # sent from the peekSwUpdater will be queued and sent when it does connect.
    # d.addBoth(lambda _: peekSwVersionPollHandler.start())

    # Load all Plugins
    from peek_client.plugin.ClientPluginLoader import clientPluginLoader
    d.addBoth(lambda _: clientPluginLoader.loadAllPlugins())

    from peek_client.PeekClientConfig import peekClientConfig

    def startSite(_):
        from peek_client.backend.SiteRootResource import root
        sitePort = peekClientConfig.sitePort
        setupSite("Peek Client", root, sitePort, enableLogin=False)
        # setupSite(8000, debug=True, protectedResource=HTTPAuthSessionWrapper())

    d.addCallback(startSite)

    d.addErrback(printFailure)

    # Init the realtime handler

    logger.info('Peek Client is running, version=%s', peekClientConfig.platformVersion)
    reactor.run()


if __name__ == '__main__':
    main()
