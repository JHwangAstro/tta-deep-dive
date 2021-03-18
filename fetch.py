""" Load data sources in a ergonomic way.
"""

from typing import Dict

import attr
import pandas as pd
import yaml


Config = Dict[str, str]


@attr.s(auto_attribs=True, repr=False)
class Config(object):
    """ Load configuration from yaml file.
    """
    filename: str = "./data_sources.yaml"

    def __repr__(self) -> str:
        return f"Config({self.filename})"

    @property
    def data_sources(self) -> Dict[str, Dict[str, str]]:
        """ Returns a dictioanry defining the data sources in the configuration.
        """
        with open(self.filename, "r") as f:
            data_sources = yaml.safe_load(f)

        return data_sources


# make an abstract class?
@attr.s(auto_attribs=True, repr=False)
class DataSource(object):
    """ Template class loading data from a configuration.
    """
    @classmethod
    def from_config(cls, config: Config, node: str = None):
        """ Create a GoogleSheets class from a config.
        """
        return cls(**config.get("kwargs"))

    @classmethod
    def from_config_file(
        cls,
        node: str,
        filename: str = "./data_sources.yaml"
    ):
        """ Create a GoogleSheets class from a configuration file.
        """
        data_sources = Config(filename=filename).data_sources

        assert node in data_sources, f"{node} not found in config."

        return cls.from_config(config=data_sources.get(node), node=node)


@attr.s(auto_attribs=True, repr=False)
class GoogleSheets(DataSource):
    """ Load data from a google sheets configuration.
    """
    key: str
    gid: str
    host: str = "docs.google.com"
    base_path: str = "spreadsheets/d"
    node: str = None

    def __repr__(self) -> str:
        name = (self.url if self.node is None else self.node)
        return f"GoogleSheets({name})"

    @property
    def url(self) -> str:
        """ Constructs full url from key and gid.
        """
        host = self.host
        base_path = self.base_path
        key = self.key
        gid = self.gid

        return f"https://{host}/{base_path}/{key}/export?format=csv&gid={gid}"

    def as_pandas(self, sep: str = ",") -> pd.DataFrame:
        """ Return the csv as pandas.
        """
        return pd.read_csv(self.url, sep=sep)


data_source_map = {
    "googlesheet": GoogleSheets
}


def data_source(
    node: str,
    filename: str = "./data_sources.yaml"
) -> DataSource:
    """ Return a data source object
    """
    data_sources = Config(filename=filename).data_sources

    assert node in data_sources, f"{node} not found in config."

    node_config = data_sources.get(node)
    data_source_type = node_config.get("type").lower()
    data_source = data_source_map.get(data_source_type)

    return data_source.from_config(config=node_config)