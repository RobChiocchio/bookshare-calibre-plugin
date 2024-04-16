#!/usr/bin/env python
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai

__license__   = "GPL v3"
__copyright__ = "2024, Rob Chiocchio <rmchiocchio@wpi.edu>"
__docformat__ = "restructuredtext en"
__version__ = (0, 1, 0)

import os

from calibre.customize import FileTypePlugin

USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko"


class HelloWorld(FileTypePlugin):

    name                = "Hello World Plugin" # Name of the plugin
    description         = "Set the publisher to Hello World for all new conversions"
    supported_platforms = ["windows", "osx", "linux"] # Platforms this plugin will run on
    author              = "Rob Chiocchio" # The author of this plugin
    version             = __version__   # The version number of this plugin
    file_types          = {"epub", "zip"} # The file types that this plugin will be applied to
    on_postprocess      = True # Run this plugin after conversion is complete
    minimum_calibre_version = (5, 0, 0)

    def run(self, path_to_ebook):
        from calibre.ebooks.metadata.meta import get_metadata, set_metadata
        with open(path_to_ebook, "r+b") as file:
            ext  = os.path.splitext(path_to_ebook)[-1][1:].lower()
            mi = get_metadata(file, ext)
            mi.publisher = "Hello World"
            set_metadata(file, mi, ext)
        return path_to_ebook
