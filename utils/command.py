import commands

def is_command(msg: str)->tuple:
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
