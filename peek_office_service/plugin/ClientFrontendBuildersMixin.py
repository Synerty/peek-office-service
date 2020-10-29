import logging

import os

from peek_platform.build_doc.DocBuilder import DocBuilder
from peek_platform.build_frontend.WebBuilder import WebBuilder

logger = logging.getLogger(__name__)


class ClientFrontendBuildersMixin:

    def _buildMobile(self, loadedPlugins):
        # --------------------
        # Prepare the Peek Mobile

        from peek_platform import PeekPlatformConfig

        try:
            import peek_field_app
            mobileProjectDir = os.path.dirname(peek_field_app.__file__)

        except:
            logger.warning("Skipping builds of peek-field-app"
                           ", the package can not be imported")
            return

        mobileWebBuilder = WebBuilder(mobileProjectDir,
                                      "peek-field-app",
                                      PeekPlatformConfig.config,
                                      loadedPlugins)
        yield mobileWebBuilder.build()

    def _buildDesktop(self, loadedPlugins):
        # --------------------
        # Prepare the Peek Desktop
        from peek_platform import PeekPlatformConfig

        try:
            import peek_office_app
            desktopProjectDir = os.path.dirname(peek_office_app.__file__)

        except:
            logger.warning("Skipping builds of peek-office-app"
                           ", the package can not be imported")
            return

        desktopWebBuilder = WebBuilder(desktopProjectDir,
                                       "peek-office-app",
                                       PeekPlatformConfig.config,
                                       loadedPlugins)
        yield desktopWebBuilder.build()

    def _buildDocs(self, loadedPlugins):
        # --------------------
        # Prepare the User Docs
        from peek_platform import PeekPlatformConfig

        try:
            import peek_doc_user
            docProjectDir = os.path.dirname(peek_doc_user.__file__)

        except:
            logger.warning("Skipping builds of peek_doc_user"
                           ", the package can not be imported")
            return

        docBuilder = DocBuilder(docProjectDir,
                                "peek-doc-user",
                                PeekPlatformConfig.config,
                                loadedPlugins)
        yield docBuilder.build()