from txhttputil.site.FileUnderlayResource import FileUnderlayResource
from vortex.VortexResource import VortexResource

from peek_client.PeekClientConfig import peekClientConfig

root = FileUnderlayResource()

# Setup properties for serving the site
root.enableSinglePageApplication()
root.addFileSystemRoot(peekClientConfig.feDistDir)

root.putChild(b'vortex', VortexResource())
