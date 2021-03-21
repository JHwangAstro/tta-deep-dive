""" Create transformed dataframes from input data sources.
"""

import importlib
from typing import Dict, Tuple
import uuid

import attr
import pandas as pd
import yaml

from data_source import get_data_source


ConfigType = Dict[str, str]


@attr.s(auto_attribs=True, repr=False)
class ViewConfig(object):
    """ Load configuration from yaml file.
    """
    filename: str = "../views.yaml"

    def __repr__(self) -> str:
        return f"ViewConfig({self.filename})"

    @property
    def views(self) -> Dict[str, Dict[str, str]]:
        """ Returns a dictioanry defining the views in the configuration.
        """
        with open(self.filename, "r") as f:
            views = yaml.safe_load(f)

        return views


@attr.s(auto_attribs=True, repr=False)
class View(object):
    """ Template class loading data from a configuration.
    """
    node: str
    inputs: Tuple[str, ...]
    config: ConfigType

    def __repr__(self) -> str:
        node = self.node

        return f"ViewConfig({node}, inputs={self.inputs})"

    @classmethod
    def from_config(cls, node: str, config: ConfigType):
        """ Create a View class from a config.
        """
        return cls(node=node, inputs=config.get("inputs", ()), config=config)

    @classmethod
    def from_config_file(cls, node: str, filename: str = "../views.yaml"):
        """ Create a View class from a configuration file.
        """
        views = ViewConfig(filename=filename).views

        assert node in views, f"{node} not found in config."

        return cls.from_config(node=node, config=views.get(node))

    def as_pandas(self, views_dir: str = "../views") -> pd.DataFrame:
        """ Return the view as a pandas dataframe.
        """
        view_name = self.node

        uuid_str = str(uuid.uuid4())[:4]

        spec = importlib.util.spec_from_file_location(
            f"{view_name}_{uuid_str}",
            f"{views_dir}/{view_name}.py"
        )

        task_module = importlib.util.module_from_spec(spec)

        spec.loader.exec_module(task_module)

        input_dataframes = {
            node: get_data_source(node=node).as_pandas()
            for node in self.inputs
        }

        return task_module.view(input_dataframes=input_dataframes)
