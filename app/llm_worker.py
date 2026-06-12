from PySide6.QtCore import QObject, Signal, Slot
from app.localization import llm_worker_message


class LlmWorker(QObject):
    finished = Signal(str, int, int, str)
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


    def is_error_text(self, text: str) -> bool:
        stripped_text = text.strip()
        return (
            stripped_text.startswith("[Fehler]")
            or stripped_text.startswith("[Error]")
        )


    @Slot()
    def run(self) -> None:
        try:
            if self.mode == "generate":
                result_text = self.llm_client.generate_text(self.prompt)
                end_position = self.insert_position

            elif self.mode == "continue":
                result_text = self.llm_client.continue_text(self.prompt)
                end_position = self.insert_position

            elif self.mode == "transform":
                if not self.selected_text:
                    self.failed.emit(llm_worker_message("no_selection"))
                    return

                result_text = self.llm_client.transform_text(
                    self.prompt,
                    self.selected_text,
                )
                end_position = self.selection_end or self.insert_position

            else:
                self.failed.emit(
                    llm_worker_message("unknown_mode", mode=self.mode)
                )
                return

            if not result_text.strip():
                self.failed.emit(llm_worker_message("empty_response"))
                return

            if self.is_error_text(result_text):
                self.failed.emit(result_text)
                return

            self.finished.emit(
                result_text,
                self.insert_position,
                end_position,
                self.mode,
            )

        except Exception as error:
            self.failed.emit(
                llm_worker_message("worker_error", error=error)
            )
