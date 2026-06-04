from PySide6.QtCore import QObject, Signal, Slot


class LlmWorker(QObject):
    finished = Signal(str, int)
    failed = Signal(str)

    def __init__(self, llm_client, prompt: str, insert_position: int):
        super().__init__()
        self.llm_client = llm_client
        self.prompt = prompt
        self.insert_position = insert_position

    @Slot()
    def run(self) -> None:
        try:
            generated_text = self.llm_client.generate_text(self.prompt)

            if generated_text.strip():
                self.finished.emit(generated_text, self.insert_position)
            else:
                self.failed.emit("Die KI hat keinen Text zurückgegeben.")

        except Exception as error:
            self.failed.emit(f"KI-Fehler: {error}")
