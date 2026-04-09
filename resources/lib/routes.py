from .context import PLUGIN
from .modules import catalogs, main, provisioning, source


def register_routes():
    main.register_routes()
    catalogs.register_routes()
    source.register_routes()
    provisioning.register_routes()


register_routes()


def run():
    PLUGIN.run()
