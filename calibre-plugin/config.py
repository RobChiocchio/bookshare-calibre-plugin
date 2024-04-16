import os

from . import PLUGIN_NAME

from calibre.utils.config import JSONConfig
from calibre.constants import config_dir as abs_config_dir

CONFIG_DIR = os.path.join("plugins", "robchio")
JSON_PATH = os.path.join(CONFIG_DIR, PLUGIN_NAME + ".json")
COOKIEJAR_PATH = os.path.join(abs_config_dir, CONFIG_DIR, PLUGIN_NAME + ".cookiejar")

class BookshareConfig(JSONConfig):
    def __init__(self):
        super().__init__(JSON_PATH)

        self.defaults = {
            "username": "partnerdemo@bookshare.org",
            "password": "partner",
        }

        self.cookiejar_path = COOKIEJAR_PATH