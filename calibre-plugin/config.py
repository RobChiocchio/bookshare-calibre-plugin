import os

from . import PLUGIN_NAME
from .config_widget_ui import Ui_Form

from calibre.utils.config import JSONConfig
from calibre.constants import config_dir as abs_config_dir
from calibre.gui2.store.basic_config import BasicStoreConfig

from qt.core import QWidget

CONFIG_DIR = os.path.join("plugins", "robchio")
JSON_PATH = os.path.join(CONFIG_DIR, PLUGIN_NAME + ".json")
COOKIEJAR_PATH = os.path.join(abs_config_dir, CONFIG_DIR, PLUGIN_NAME + ".cookiejar")

CONFIG = JSONConfig(JSON_PATH)

CONFIG.defaults = {
        "username": "partnerdemo@bookshare.org",
        "password": "partner",
        "open_external": False,
        "tags": "",
    }

class BookshareConfig(JSONConfig):
    def __init__(self):
        raise NotImplementedError("Use the CONFIG object instead")
        super().__init__(JSON_PATH)

        self.defaults = {
            "username": "partnerdemo@bookshare.org",
            "password": "partner",
        }

        self.cookiejar_path = COOKIEJAR_PATH

class BookshareConfigWidget(QWidget, Ui_Form):
    def __init__(self, plugin):
        QWidget.__init__(self)
        self.setupUi(self)
        self.plugin = plugin
        self.config = CONFIG
        self.load_settings()

    # def save_settings(self):
    #     self.config.set("username", self.username.text())
    #     self.config.set("password", self.password.text())
    #     self.config.save()

    def load_settings(self):
        self.username.setText(self.config.get("username", ""))
        self.password.setText(self.config.get("password", ""))
        self.open_external.setChecked(self.config.get("open_external", False))
        self.tags.setText(self.config.get("tags", ""))

class BookshareStorePluginConfig(BasicStoreConfig):
    def customization_help(self, gui=False):
        return "HELP TEXT HERE"
    
    def config_widget(self):
        return BookshareConfigWidget(self)
    
    def save_settings(self, config_widget):
        CONFIG.set("username", config_widget.username.text())
        CONFIG.set("password", config_widget.password.text())
        CONFIG.set("open_external", config_widget.open_external.isChecked())
        CONFIG.set("tags", config_widget.tags.text())