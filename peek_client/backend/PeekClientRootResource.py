from txhttputil.site.FileUnderlayResource import FileUnderlayResource
from vortex.VortexResource import VortexResource

rootResource = FileUnderlayResource()
# rootResource.addFileSystemRoot()

rootResource.putChild(b'vortex', VortexResource())
