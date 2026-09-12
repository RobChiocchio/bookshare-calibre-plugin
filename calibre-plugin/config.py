import os

from qt.core import QWidget

from calibre.constants import config_dir as abs_config_dir
from calibre.gui2.store.basic_config import BasicStoreConfig
from calibre.utils.config import JSONConfig

from . import PLUGIN_NAME
from .config_widget_ui import Ui_Form

CONFIG_DIR = os.path.join("plugins", "robchio")
JSON_PATH = os.path.join(CONFIG_DIR, PLUGIN_NAME + ".json")
COOKIEJAR_PATH = os.path.join(abs_config_dir, CONFIG_DIR, PLUGIN_NAME + ".cookiejar")

CONFIG = JSONConfig(JSON_PATH)

CONFIG.defaults = {
        "username": "",
        "password": "",
        "cookie": "",
        "open_external": True,
        "tags": "Bookshare",
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

    def save_settings(self):
        CONFIG.set("username", self.username.text())
        CONFIG.set("password", self.password.text())
        CONFIG.set("cookie", self.cookie.text().strip())
        CONFIG.set("open_external", self.open_external.isChecked())
        CONFIG.set("tags", self.tags.text())

    def load_settings(self):
        self.username.setText(self.config.get("username", "")) # TODO: get username automatically when signed in with cookie
        #self.password.setText(self.config.get("password", ""))
        self.password.setText("")
        self.cookie.setText(self.config.get("cookie", ""))
        #self.login_status.setText(self.plugin.logged_in) TODO: how do I do this?
        self.open_external.setChecked(self.config.get("open_external", False))
        self.tags.setText(self.config.get("tags", ""))

class BookshareStorePluginConfig(BasicStoreConfig):
    def customization_help(self, gui=False):
        return "HELP TEXT HERE"
    
    def config_widget(self):
        return BookshareConfigWidget(self)