'''
 *
 *  Copyright Synerty Pty Ltd 2013
 *
 *  This software is proprietary, you are not free to copy
 *  or redistribute this code in any format.
 *
 *  All rights to this software are reserved by 
 *  Synerty Pty Ltd
 *
 * Website : http://www.synerty.com
 * Support : support@synerty.com
 *
'''
import logging

from jsoncfg.value_mappers import require_integer
from peek_platform import PeekFileConfigBase
from peek_platform import \
    PeekFileConfigFrontendDirMixin
from peek_platform import \
    PeekFileConfigPeekServerClientMixin
from peek_platform import \
    PeekFileConfigPlatformMixin

logger = logging.getLogger(__name__)


class PeekClientConfig(PeekFileConfigBase,
                       PeekFileConfigPeekServerClientMixin,
                       PeekFileConfigPlatformMixin,
                       PeekFileConfigFrontendDirMixin):
    """
    This class creates a basic client configuration
    """

    _frontendProjectDir = "/home/peek/project/peek_client_fe"

    ### SERVER SECTION ###
    @property
    def sitePort(self) -> int:
        with self._cfg as c:
            return c.server.port(8000, require_integer)


peekClientConfig = PeekClientConfig()
