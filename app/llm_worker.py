# SPDX-License-Identifier: Apache-2.0

"""
Worker object for running LLM tasks outside the Qt UI thread.

SayScript uses this worker together with QThread so long-running local LLM
requests do not freeze the editor window.

The worker supports three modes:

- generate: insert newly generated text at a cursor position
- continue: continue the current document at a cursor position
- transform: replace selected text with transformed text
"""

from PySide6.QtCore import QObject, Signal, Slot

from app.localization import llm_worker_message


class LlmWorker(QObject):
    """
    Execute one LLM task and report the result through Qt signals.

    The worker does not directly modify the editor. Instead, it emits either
    finished(...) or failed(...). The main window receives those signals and
    updates the GUI safely in the UI thread.
    """

    # result_text, insert_position, end_position, mode
    finished = Signal(str, int, int, str)

    # localized error message
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
        """
        Return True if the LLM client returned a localized error string.

        LlmClient returns some connection or timeout errors as displayable text.
        The worker turns those into failed(...) signals so the main window can
        treat them like proper task failures.
        """
        stripped_text = text.strip()

        return (
            stripped_text.startswith("[Fehler]")
            or stripped_text.startswith("[Error]")
        )

    @Slot()
    def run(self) -> None:
        """
        Execute the configured LLM operation.

        This method is connected to QThread.started. It must not touch Qt
        widgets directly because it runs outside the main UI thread.
        """
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
