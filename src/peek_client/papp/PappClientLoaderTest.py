import logging

import sys
from twisted.internet import reactor
from twisted.internet.defer import Deferred
from twisted.trial import unittest

from PappClientLoader import pappClientLoader

logger = logging.getLogger(__name__)

PAPP_NOOP = "papp_noop"


class PappClientLoaderTest(unittest.TestCase):
    def testLoadAll(self):
        pappClientLoader.loadAllPapps()

        logger.info(pappClientLoader.listPapps())

        for papp in pappClientLoader._loadedPapps.values():
            logger.info("configUrl = %s", papp.configUrl())

        d = Deferred()
        reactor.callLater(5.0, d.callback, True)
        return d

    def testUnregister(self):
        loadedModuleBefore = set(sys.modules)

        pappClientLoader.loadPapp(PAPP_NOOP)
        self.assertTrue(PAPP_NOOP in sys.modules)

        pappClientLoader.unloadPapp(PAPP_NOOP)

        loadedModuleNow = set(sys.modules) - loadedModuleBefore

        # Ensure that none of the modules contain the papp_name
        for modName in loadedModuleNow:
            self.assertFalse(PAPP_NOOP in modName)

    def testReRegister(self):
        pappClientLoader.loadPapp(PAPP_NOOP)
        pappClientLoader.loadPapp(PAPP_NOOP)

        for papp in pappClientLoader._loadedPapps.values():
            logger.info("configUrl = %s", papp.configUrl())

        d = Deferred()
        reactor.callLater(5.0, d.callback, True)
        return d
