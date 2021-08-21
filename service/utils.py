import hashlib
import pkgutil
import yaml
from yaml import CLoader as Loader

def hash_id(salt, text):
    text = ((salt or '') + (text or '')).encode()
    sha = hashlib.sha3_512(text)
    return sha.hexdigest()[:24]

def get_yaml_config():
    config_data = pkgutil.get_data(__package__,'config.yaml')
    return yaml.load(config_data,Loader)