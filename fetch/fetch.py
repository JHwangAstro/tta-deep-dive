""" Ergonomically load data sources and views.
"""

from data_source import DataSourceType, get_data_source
from view import View


def data_source(
    node: str,
    filename: str = "../data_sources.yaml"
) -> DataSourceType:
    """ Return a data source object
    """
    return get_data_source(node=node, filename=filename)


def view(node: str, filename: str = "../views.yaml") -> View:
    """
    """
    return View.from_config_file(node=node, filename=filename)
