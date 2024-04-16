#!/usr/bin/env python3

__license__   = "GPL v3"
__copyright__ = "2024, Rob Chiocchio <rmchiocchio@wpi.edu>"
__docformat__ = "restructuredtext en"
__version__ = (0, 1, 0)

PLUGIN_NAME = "Bookshare"

from calibre.customize import StoreBase

from .bookshare import BookshareStore


class BooksharePlugin(StoreBase):
    name                = PLUGIN_NAME # Name of the plugin
    description         = "Set the publisher to Hello World for all new conversions"
    supported_platforms = ["windows", "osx", "linux"] # Platforms this plugin will run on
    author              = "Rob Chiocchio" # The author of this plugin
    version             = __version__   # The version number of this plugin
    file_types          = {"epub", "zip"} # The file types that this plugin will be applied to
    on_import           = True # Run this plugin when a new book is imported
    #on_preprocess       = True # Run this plugin before conversion is started
    on_postprocess      = True # Run this plugin after conversion is complete
    minimum_calibre_version = (5, 0, 0)

    def load_actual_plugin(self, gui):
        """This method must return the actual interface action plugin object.
        """
        self.actual_plugin_object  = BookshareStore(gui, self.name)
        return self.actual_plugin_object
