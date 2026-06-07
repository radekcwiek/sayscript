from PySide6.QtCore import QObject, Signal, Slot


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
                self.failed.emit("Kein Text erkannt.")

        except Exception as error:
            self.failed.emit(f"Transkriptionsfehler: {error}")
