from pathlib import Path
import os
import sys

from app.version import APP_NAME


APP_ID = APP_NAME.lower().replace(" ", "-")


def is_windows() -> bool:
    return sys.platform.startswith("win")


def is_linux() -> bool:
    return sys.platform.startswith("linux")


def get_config_dir() -> Path:
    if is_windows():
        base_dir = os.environ.get("LOCALAPPDATA")

        if base_dir:
            return Path(base_dir) / APP_NAME

        return Path.home() / "AppData" / "Local" / APP_NAME

    base_dir = os.environ.get("XDG_CONFIG_HOME")

    if base_dir:
        return Path(base_dir) / APP_ID

    return Path.home() / ".config" / APP_ID


def get_data_dir() -> Path:
    if is_windows():
        return get_config_dir()

    base_dir = os.environ.get("XDG_DATA_HOME")

    if base_dir:
        return Path(base_dir) / APP_ID

    return Path.home() / ".local" / "share" / APP_ID


def get_state_dir() -> Path:
    if is_windows():
        return get_config_dir()

    base_dir = os.environ.get("XDG_STATE_HOME")

    if base_dir:
        return Path(base_dir) / APP_ID

    return Path.home() / ".local" / "state" / APP_ID


def get_log_dir() -> Path:
    return get_state_dir() / "logs"


def get_settings_path() -> Path:
    return get_config_dir() / "settings.json"


def get_autosave_dir() -> Path:
    return get_state_dir() / "autosave"


def get_autosave_path() -> Path:
    return get_autosave_dir() / "autosave.html"


def ensure_app_dirs() -> None:
    get_config_dir().mkdir(parents=True, exist_ok=True)
    get_data_dir().mkdir(parents=True, exist_ok=True)
    get_state_dir().mkdir(parents=True, exist_ok=True)
    get_log_dir().mkdir(parents=True, exist_ok=True)
    get_autosave_dir().mkdir(parents=True, exist_ok=True)
