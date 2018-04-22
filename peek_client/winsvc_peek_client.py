import logging

import win32service
import win32serviceutil
from twisted.internet import reactor

logger = logging.getLogger(__name__)


class PeekSvc(win32serviceutil.ServiceFramework):
    _svc_name_ = "peek_client"
    _svc_display_name_ = "Peek Client "  # + peek_client.__version__

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)

        reactor.addSystemEventTrigger('after', 'shutdown', self._notifyOfStop)

    def _notifyOfStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)

    def _notifyOfStart(self):
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        reactor.callFromThread(reactor.stop)

    def SvcDoRun(self):
        self.ReportServiceStatus(win32service.SERVICE_START_PENDING)
        try:

            # Patch the restart method for windows services
            class _Restart:
                def _restartProcess(self):
                    reactor.callFromThread(reactor.stop)

            # Patch the restart call for windows
            from peek_platform.sw_install.PeekSwInstallManagerABC import \
                PeekSwInstallManagerABC
            PeekSwInstallManagerABC.restartProcess = _Restart._restartProcess

            reactor.callLater(1, self._notifyOfStart)

            from peek_client import run_peek_client
            run_peek_client.main()

        except Exception as e:
            logger.exception(e)
            raise


def main():
    win32serviceutil.HandleCommandLine(PeekSvc)


if __name__ == '__main__':
    main()
