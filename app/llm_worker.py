from PySide6.QtCore import QObject, Signal, Slot


class LlmWorker(QObject):
    finished = Signal(str, int, int)
    failed = Signal(str)

    def __init__(
        self,
        llm_client,
        mode: str,
        prompt: str,
        insert_position: int,
        selection_end: int | None = None,
        selected_text: str | None = None,
    ):
        super().__init__()
        self.llm_client = llm_client
        self.mode = mode
        self.prompt = prompt
        self.insert_position = insert_position
        self.selection_end = selection_end
        self.selected_text = selected_text

    @Slot()
    def run(self) -> None:
        try:
            if self.mode == "generate":
                result_text = self.llm_client.generate_text(self.prompt)
                end_position = self.insert_position

            elif self.mode == "transform":
                if not self.selected_text:
                    self.failed.emit("Keine Auswahl für KI-Bearbeitung vorhanden.")
                    return

                result_text = self.llm_client.transform_text(
                    self.prompt,
                    self.selected_text,
                )
                end_position = self.selection_end or self.insert_position

            else:
                self.failed.emit(f"Unbekannter KI-Modus: {self.mode}")
                return

            if result_text.strip():
                self.finished.emit(result_text, self.insert_position, end_position)
            else:
                self.failed.emit("Die KI hat keinen Text zurückgegeben.")

        except Exception as error:
            self.failed.emit(f"KI-Fehler: {error}")
