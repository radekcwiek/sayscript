# SPDX-License-Identifier: Apache-2.0

"""
Speech-to-text transcription for SayScript.

SpeechTranscriber converts recorded microphone audio into text using
faster-whisper. The recorder provides raw audio samples, this class writes them
to a temporary WAV file, and faster-whisper transcribes that file.

The Whisper language and initial prompt are provided by the localization module
so dictation can follow the selected interface language.
"""

import tempfile
from pathlib import Path

from faster_whisper import WhisperModel
from scipy.io.wavfile import write

from app.logging_setup import get_logger
from app.localization import speech_initial_prompt, speech_language


class SpeechTranscriber:
    """
    Lazy-loading wrapper around faster-whisper.

    The Whisper model is loaded only when the first transcription is requested.
    This keeps SayScript startup faster and avoids loading a large model if the
    user never starts dictation.
    """

    def __init__(
        self,
        model_size: str = "medium",
        sample_rate: int = 16000,
        device: str = "cpu",
        compute_type: str = "int8",
        beam_size: int = 10,
    ):
        self.model_size = model_size
        self.sample_rate = sample_rate
        self.device = device
        self.compute_type = compute_type
        self.beam_size = beam_size
        self.model = None
        self.logger = get_logger()

    def load_model(self) -> None:
        """
        Load the faster-whisper model if it has not been loaded yet.
        """
        if self.model is not None:
            return

        self.logger.info(
            "Loading speech model: size=%s device=%s compute_type=%s",
            self.model_size,
            self.device,
            self.compute_type,
        )

        self.model = WhisperModel(
            self.model_size,
            device=self.device,
            compute_type=self.compute_type,
        )

        self.logger.info("Speech model loaded")

    def transcribe_audio(self, audio_data) -> str:
        """
        Transcribe recorded audio samples and return the recognized text.

        Returns an empty string when no audio data is available.
        """
        if audio_data is None:
            return ""

        self.load_model()

        # faster-whisper expects a file path. The recorded NumPy array is
        # therefore written to a temporary WAV file and removed afterwards.
        with tempfile.NamedTemporaryFile(
            suffix=".wav",
            delete=False,
        ) as temp_file:
            temp_path = Path(temp_file.name)

        try:
            write(temp_path, self.sample_rate, audio_data)

            segments, info = self.model.transcribe(
                str(temp_path),
                language=speech_language(),
                beam_size=self.beam_size,
                initial_prompt=speech_initial_prompt(),
            )

            full_text = ""

            for segment in segments:
                full_text += segment.text

            transcribed_text = full_text.strip()

            self.logger.info(
                "Audio transcribed: language=%s duration=%.2f seconds",
                info.language,
                info.duration,
            )

            return transcribed_text

        finally:
            try:
                temp_path.unlink(missing_ok=True)
            except OSError:
                self.logger.warning(
                    "Could not delete temporary audio file: %s",
                    temp_path,
                )
