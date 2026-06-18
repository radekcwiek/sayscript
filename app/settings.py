import json

from app import config
from app.platform_paths import ensure_app_dirs, get_settings_path
from app.logging_setup import get_logger


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
    ensure_app_dirs()

    logger = get_logger()
    settings_path = get_settings_path()

    with open(settings_path, "w", encoding="utf-8") as file:
        json.dump(settings, file, indent=4, ensure_ascii=False)

    logger.info("Settings saved: %s", settings_path)
