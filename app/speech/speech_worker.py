from PySide6.QtCore import QObject, Signal, Slot
from app.localization import speech_message


class SpeechWorker(QObject):
    finished = Signal(str)
    failed = Signal(str)

    def __init__(self, transcriber, audio_data):
        super().__init__()
        self.transcriber = transcriber
        self.audio_data = audio_data

    @Slot()
    def run(self) -> None:
        try:
            text = self.transcriber.transcribe_audio(self.audio_data)

            if text.strip():
                self.finished.emit(text)
            else:
                self.failed.emit(speech_message("no_text_recognized"))

        except Exception as error:
            self.failed.emit(speech_message("transcription_error", error=error))
