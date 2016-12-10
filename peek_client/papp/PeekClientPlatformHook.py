from typing import Optional

from papp_base.client.PeekClientPlatformHookABC import PeekClientPlatformHookABC


class PeekClientPlatformHook(PeekClientPlatformHookABC):

    def getOtherPappApi(self, pappName:str) -> Optional[object]:
        return None
