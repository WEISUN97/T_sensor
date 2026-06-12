from pathlib import Path
from platform import platform


def if_windows():
    current_system = platform.system()
    if current_system == "Windows":
        return True
    return False
