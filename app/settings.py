# SPDX-License-Identifier: Apache-2.0

"""
Settings handling for SayScript.

This module is responsible for building the default settings dictionary,
loading user settings from disk, and saving changed settings.

The settings file path itself is provided by app.platform_paths so this module
does not need to know whether it is running on Windows or Linux.
"""

import json

from app import config
from app.logging_setup import get_logger
from app.platform_paths import ensure_app_dirs, get_settings_path


def get_default_settings() -> dict:
    """
    Return SayScript's default settings.

    Defaults are read from app.config. Keeping the defaults in config.py makes
    it easy to see the application's baseline behavior in one place, while this
    module handles persistence.
    """
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
        "speech_model_size": config.SPEECH_MODEL_SIZE,
        "speech_sample_rate": config.SPEECH_SAMPLE_RATE,
        "speech_device": config.SPEECH_DEVICE,
        "speech_compute_type": config.SPEECH_COMPUTE_TYPE,
        "speech_beam_size": config.SPEECH_BEAM_SIZE,
        "show_command_input": config.SHOW_COMMAND_INPUT,
        "show_speech_result": config.SHOW_SPEECH_RESULT,
        "interface_language": config.INTERFACE_LANGUAGE,
        "text_generation_language": config.TEXT_GENERATION_LANGUAGE,
        "enable_autosave": config.ENABLE_AUTOSAVE,
        "autosave_interval_seconds": config.AUTOSAVE_INTERVAL_SECONDS,
    }


def load_settings() -> dict:
    """
    Load settings from disk and merge them with the current defaults.

    If the settings file does not exist yet, it is created with default values.
    If loading fails, defaults are returned so the application can still start.

    Returning ``default_settings | loaded_settings`` keeps SayScript compatible
    with older settings files: new keys from config.py are automatically added,
    while user-defined values still override the defaults.
    """
    ensure_app_dirs()

    logger = get_logger()
    settings_path = get_settings_path()
    default_settings = get_default_settings()

    if not settings_path.exists():
        save_settings(default_settings)
        logger.info("Settings file created: %s", settings_path)
        return default_settings

    try:
        with open(settings_path, "r", encoding="utf-8") as file:
            loaded_settings = json.load(file)

    except (OSError, json.JSONDecodeError) as error:
        logger.warning(
            "Could not load settings file %s: %s",
            settings_path,
            error,
        )
        return default_settings

    logger.debug("Settings loaded: %s", settings_path)
    return default_settings | loaded_settings


def save_settings(settings: dict) -> None:
    """
    Save settings to disk as UTF-8 encoded JSON.

    ``ensure_ascii=False`` keeps German text and other non-ASCII characters
    readable in the settings file.
    """
    ensure_app_dirs()

    logger = get_logger()
    settings_path = get_settings_path()

    with open(settings_path, "w", encoding="utf-8") as file:
        json.dump(settings, file, indent=4, ensure_ascii=False)

    logger.info("Settings saved: %s", settings_path)
