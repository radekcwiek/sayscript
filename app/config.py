# SPDX-License-Identifier: Apache-2.0

"""
Default configuration values for SayScript.

These constants define the application's initial behavior. User-specific
settings are stored separately in settings.json and are loaded through
app.settings.

When a new setting is added here, it should usually also be added to
get_default_settings() in app.settings.
"""


# Ollama connection ---------------------------------------------------------

# Default local Ollama endpoint.
OLLAMA_BASE_URL = "http://localhost:11434"

# Default model used for local text generation and transformation.
OLLAMA_MODEL_NAME = "qwen3:8b"

# Development/testing switch. When True, SayScript can return fake LLM
# responses without contacting Ollama.
USE_FAKE_LLM = False

# Timeout for longer local LLM responses.
LLM_TIMEOUT_SECONDS = 240


# Text generation defaults -------------------------------------------------

GENERATE_TEMPERATURE = 0.7
GENERATE_NUM_PREDICT = 500

TRANSFORM_TEMPERATURE = 0.4
TRANSFORM_NUM_PREDICT = 500

CONTINUE_TEMPERATURE = 0.7
CONTINUE_NUM_PREDICT = 500


# Speech recognition defaults ----------------------------------------------

# faster-whisper model size. "medium" is a quality-oriented default.
SPEECH_MODEL_SIZE = "medium"

# Speech input sample rate in Hz.
SPEECH_SAMPLE_RATE = 16000

# Default inference device for speech recognition.
SPEECH_DEVICE = "cpu"

# Default compute type for CPU inference.
SPEECH_COMPUTE_TYPE = "int8"

# Beam size used by faster-whisper. Higher values may improve quality but can
# make transcription slower.
SPEECH_BEAM_SIZE = 10


# User interface defaults --------------------------------------------------

SHOW_COMMAND_INPUT = False
SHOW_SPEECH_RESULT = False

INTERFACE_LANGUAGE = "de"
TEXT_GENERATION_LANGUAGE = "de"


# Auto-save defaults -------------------------------------------------------

ENABLE_AUTOSAVE = True
AUTOSAVE_INTERVAL_SECONDS = 60
