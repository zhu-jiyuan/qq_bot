import yaml
from logging import error
config_dict = None

def _load_config()->dict:
    global config_dict
    with open('config.yaml', 'r') as f:
        config_dict = yaml.safe_load(f)
    return config_dict

def config(env_name: str):
    global config_dict

    if config_dict is None:
        _load_config()

    if config_dict is None:
        error("config_dict is None")
        exit(1)

    if env_name not in config_dict:
        error(f"{env_name} not found in config.yaml")
        exit(1)
    
    return config_dict[env_name]

