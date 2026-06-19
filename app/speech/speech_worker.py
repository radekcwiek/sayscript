# SPDX-License-Identifier: Apache-2.0

"""
Worker object for speech transcription outside the Qt UI thread.

Speech recognition can take noticeable time, especially with larger Whisper
models. SayScript runs transcription in a worker so the main editor window stays
responsive while audio is being processed.
"""

from PySide6.QtCore import QObject, Signal, Slot

from app.localization import speech_message


class SpeechWorker(QObject):
    """
    Execute one speech-to-text task and report the result through Qt signals.

    The worker receives recorded audio data and a SpeechTranscriber instance.
    It emits finished(text) when transcription succeeds and failed(message) when
    no text was recognized or an error occurred.
    """

    # Recognized text
    finished = Signal(str)

    # Localized error message
    failed = Signal(str)

    def __init__(self, transcriber, audio_data):
        super().__init__()

        self.transcriber = transcriber
        self.audio_data = audio_data

    @Slot()
    def run(self) -> None:
        """
        Transcribe the provided audio data.

        This method is intended to run inside a QThread. It must not access or
        modify Qt widgets directly.
        """
        try:
            text = self.transcriber.transcribe_audio(self.audio_data)

            if text.strip():
                self.finished.emit(text)
            else:
                self.failed.emit(speech_message("no_text_recognized"))

        except Exception as error:
            self.failed.emit(
                speech_message("transcription_error", error=error)
            )
