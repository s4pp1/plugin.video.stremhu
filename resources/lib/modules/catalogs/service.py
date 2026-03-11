import xbmc

from lib.common import log
from lib.integrations.catalog import catalog_api


def get_catalogs():
    try:
        response = catalog_api.get_catalogs()
        return response
    except Exception as error:
        error_message = str(error)
        log(error_message, xbmc.LOGERROR)
        raise error
