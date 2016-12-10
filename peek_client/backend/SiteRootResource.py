import os

from txhttputil.site.FileUnderlayResource import FileUnderlayResource
from vortex.VortexResource import VortexResource

from peek_client.PeekClientConfig import peekClientConfig

root = FileUnderlayResource()

# Setup properties for serving the site
root.enableSinglePageApplication()

# This dist dir is automatically generated, but check it's parent
distDir = peekClientConfig.feDistDir
distDirParent = os.path.dirname(distDir)
if not os.path.isdir(distDirParent):
    raise NotADirectoryError(distDirParent)

# Make the dist dir, otherwise addFileSystemRoot throws an exception.
# It rebuilds at a later date
os.makedirs(distDir, exist_ok=True)

root.addFileSystemRoot(distDir)

root.putChild(b'vortex', VortexResource())
