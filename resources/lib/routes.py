from .context import PLUGIN
from .modules import catalogs, source


def register_routes():
    catalogs.register_routes()
    source.register_routes()
    # tmdb_helper.register_routes()


register_routes()


def run():
    PLUGIN.run()
