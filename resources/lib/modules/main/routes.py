from lib.context import PLUGIN
from lib.modules.main.presenter import render_main_menu, root_info, open_settings


@PLUGIN.route("/")
def index():
    render_main_menu()


@PLUGIN.route("/main/info")
def main_info():
    root_info()


@PLUGIN.route("/main/settings")
def main_settings():
    open_settings()
