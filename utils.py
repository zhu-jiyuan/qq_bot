from logging import error
import yaml
import commands

config_dict = None


def _load_config()->dict:
    global config_dict
    with open('config.yaml', 'r') as f:
        config_dict = yaml.safe_load(f)
    return config_dict

def config(env_name: str)->str|None:
    global config_dict

    if config_dict is None:
        _load_config()

    if config_dict is None:
        error("config_dict is None")
        exit(1)

    return config_dict[env_name]

def is_command(msg: str):
    if not msg.startswith('/'):
        return False, None, None

    if len(msg) == 1:
        return False, None, None

    command_parts = msg[1:].split(maxsplit=1, sep=' ')
    if not command_parts[0]:
        return False, None, None
    
    if hasattr(commands, command_parts[0]):
        return True, getattr(commands, command_parts[0]), command_parts[1] if len(command_parts) > 1 else None

    return False, None, None
