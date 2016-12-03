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
from twisted.internet.defer import succeed

from pytmpdir.Directory import DirSettings
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


def main():
    # defer.setDebugging(True)
    # sys.argv.remove(DEBUG_ARG)
    # import pydevd
    # pydevd.settrace(suspend=False)

    from peek_platform import PeekPlatformConfig
    PeekPlatformConfig.componentName = "peek_client"

    # Tell the platform classes about our instance of the PappSwInstallManager
    from peek_client.sw_install.PappSwInstallManager import pappSwInstallManager
    PeekPlatformConfig.pappSwInstallManager = pappSwInstallManager

    # Tell the platform classes about our instance of the PeekSwInstallManager
    from peek_client.sw_install.PeekSwInstallManager import peekSwInstallManager
    PeekPlatformConfig.peekSwInstallManager = peekSwInstallManager

    # Tell the platform classes about our instance of the PeekLoaderBase
    from peek_client.papp.PappClientLoader import pappClientLoader
    PeekPlatformConfig.pappLoader = pappClientLoader

    # The config depends on the componentName, order is important
    from peek_client.PeekClientConfig import peekClientConfig
    PeekPlatformConfig.config = peekClientConfig

    # Set default logging level
    logging.root.setLevel(peekClientConfig.loggingLevel)

    # Initialise the txhttputil Directory object
    DirSettings.defaultDirChmod = peekClientConfig.DEFAULT_DIR_CHMOD
    DirSettings.tmpDirPath = peekClientConfig.tmpPath

    # Load server restart handler handler
    from peek_platform.PeekServerRestartWatchHandler import PeekServerRestartWatchHandler
    PeekServerRestartWatchHandler.__unused = False

    # First, setup the Vortex Agent
    # from peek_platform.PeekVortexClient import peekVortexClient
    # d = peekVortexClient.connect()
    # d.addErrback(printFailure)
    d = succeed(True)

    # # Start Update Handler,
    # from peek_platform.sw_version.PeekSwVersionPollHandler import peekSwVersionPollHandler
    # # Add both, The peek client might fail to connect, and if it does, the payload
    # # sent from the peekSwUpdater will be queued and sent when it does connect.
    # d.addBoth(lambda _: peekSwVersionPollHandler.start())
    #
    # # Load all Papps
    # d.addBoth(lambda _: pappClientLoader.loadAllPapps())

    def startSite(_):
        from peek_client.backend.PeekClientRootResource import rootResource
        sitePort = peekClientConfig.sitePort
        setupSite("Peek Client", rootResource, sitePort, enableLogin=False)
        # setupSite(8000, debug=True, protectedResource=HTTPAuthSessionWrapper())

    d.addCallback(startSite)

    d.addErrback(printFailure)

    # Init the realtime handler

    logger.info('Peek Client is running, version=%s', peekClientConfig.platformVersion)
    reactor.run()


if __name__ == '__main__':
    main()
