import yaml
from yaml import CLoader as Loader
import pkgutil


def get_yaml_config(key):
    conf_data = pkgutil.get_data(__package__, "config.yaml")
    return yaml.load(conf_data, Loader)[key]
