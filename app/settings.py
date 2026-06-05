import json
from pathlib import Path

from app import config


def get_app_dir() -> Path:
    return Path.cwd()


def get_settings_path() -> Path:
    return get_app_dir() / "settings.json"


def get_default_settings() -> dict:
    return {
        "ollama_base_url": config.OLLAMA_BASE_URL,
        "ollama_model_name": config.OLLAMA_MODEL_NAME,
        "use_fake_llm": config.USE_FAKE_LLM,
        "llm_timeout_seconds": config.LLM_TIMEOUT_SECONDS,
        "generate_temperature": config.GENERATE_TEMPERATURE,
        "generate_num_predict": config.GENERATE_NUM_PREDICT,
        "transform_temperature": config.TRANSFORM_TEMPERATURE,
        "transform_num_predict": config.TRANSFORM_NUM_PREDICT,
        "continue_temperature": config.CONTINUE_TEMPERATURE,
        "continue_num_predict": config.CONTINUE_NUM_PREDICT,
    }


def load_settings() -> dict:
    settings_path = get_settings_path()
    default_settings = get_default_settings()

    if not settings_path.exists():
        save_settings(default_settings)
        return default_settings

    try:
        with open(settings_path, "r", encoding="utf-8") as file:
            loaded_settings = json.load(file)

    except (OSError, json.JSONDecodeError):
        return default_settings

    return default_settings | loaded_settings


def save_settings(settings: dict) -> None:
    settings_path = get_settings_path()

    with open(settings_path, "w", encoding="utf-8") as file:
        json.dump(settings, file, indent=4, ensure_ascii=False)
