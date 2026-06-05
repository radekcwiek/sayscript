from PySide6.QtCore import Qt, QThread
from PySide6.QtGui import (
    QAction,
    QTextCharFormat,
    QFont,
    QTextListFormat,
    QTextBlockFormat,
    QFontDatabase,
)
from PySide6.QtWidgets import (
    QMainWindow,
    QTextEdit,
    QFileDialog,
    QMessageBox,
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QLabel,
)

from app.command_router import CommandRouter
from app.llm_worker import LlmWorker
from app.settings import get_settings_path, load_settings


class MiniEditor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Dictator - Mini Editor")
        self.resize(900, 650)

        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        self.editor = QTextEdit()
        self.editor.document().modificationChanged.connect(self.update_window_title)
        layout.addWidget(self.editor)

        self.command_router = CommandRouter(self)

        self.command_label = QLabel("Befehl:")
        layout.addWidget(self.command_label)

        self.command_input = QLineEdit()
        self.command_input.setPlaceholderText("z. B. fett, kursiv, lösche auswahl ...")
        self.command_input.returnPressed.connect(self.execute_command)
        layout.addWidget(self.command_input)

        self.setCentralWidget(central_widget)

        self.current_file = None

        self.llm_thread = None
        self.llm_worker = None

        self._create_actions()
        self._create_menus()

        self.statusBar().showMessage("Bereit")


    def _create_actions(self):
        self.new_action = QAction("Neu", self)
        self.new_action.triggered.connect(self.new_file)

        self.open_action = QAction("Öffnen", self)
        self.open_action.triggered.connect(self.open_file)

        self.save_action = QAction("Speichern", self)
        self.save_action.triggered.connect(self.save_file)

        self.save_as_action = QAction("Speichern unter", self)
        self.save_as_action.triggered.connect(self.save_file_as)

        self.exit_action = QAction("Beenden", self)
        self.exit_action.triggered.connect(self.close)

        self.bold_action = QAction("Fett", self)
        self.bold_action.triggered.connect(self.toggle_bold)

        self.italic_action = QAction("Kursiv", self)
        self.italic_action.triggered.connect(self.toggle_italic)


    def _create_menus(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("Datei")
        file_menu.addAction(self.new_action)
        file_menu.addAction(self.open_action)
        file_menu.addAction(self.save_action)
        file_menu.addAction(self.save_as_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)

        format_menu = menu_bar.addMenu("Format")
        format_menu.addAction(self.bold_action)
        format_menu.addAction(self.italic_action)


    def new_file(self):
        if not self.maybe_save_changes():
            return False

        self.editor.clear()
        self.current_file = None
        self.editor.document().setModified(False)
        self.update_window_title()
        self.show_status_message("Neue Datei erstellt")
        return True


    def open_file(self):
        if not self.maybe_save_changes():
            return False

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Datei öffnen",
            "",
            "HTML-Dateien (*.html);;Textdateien (*.txt);;Alle Dateien (*.*)",
        )

        if not file_path:
            return False

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()

            if file_path.lower().endswith(".html"):
                self.editor.setHtml(content)
            else:
                self.editor.setPlainText(content)

            self.current_file = file_path
            self.editor.document().setModified(False)
            self.update_window_title()
            self.show_status_message("Datei geöffnet")
            return True

        except OSError as error:
            QMessageBox.critical(self, "Fehler", f"Datei konnte nicht geöffnet werden:\n{error}")
            return False


    def save_file(self):
        if self.current_file is None:
            return self.save_file_as()

        return self._write_file(self.current_file)


    def save_file_as(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Datei speichern",
            "",
            "HTML-Dateien (*.html);;Textdateien (*.txt)",
        )

        if not file_path:
            return False

        self.current_file = file_path
        return self._write_file(file_path)


    def _write_file(self, file_path):
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                if file_path.lower().endswith(".txt"):
                    file.write(self.editor.toPlainText())
                else:
                    file.write(self.editor.toHtml())

            self.editor.document().setModified(False)
            self.update_window_title()
            self.show_status_message("Datei gespeichert")
            return True

        except OSError as error:
            QMessageBox.critical(self, "Fehler", f"Datei konnte nicht gespeichert werden:\n{error}")
            return False


    def toggle_bold(self):
        cursor = self.editor.textCursor()

        fmt = QTextCharFormat()
        current_weight = self.editor.fontWeight()

        if current_weight == QFont.Weight.Bold:
            fmt.setFontWeight(QFont.Weight.Normal)
        else:
            fmt.setFontWeight(QFont.Weight.Bold)

        cursor.mergeCharFormat(fmt)
        self.editor.mergeCurrentCharFormat(fmt)


    def toggle_italic(self):
        cursor = self.editor.textCursor()

        fmt = QTextCharFormat()
        fmt.setFontItalic(not self.editor.fontItalic())

        cursor.mergeCharFormat(fmt)
        self.editor.mergeCurrentCharFormat(fmt)


    def execute_command(self):
        command = self.command_input.text()
        self.command_input.clear()
        self.command_router.execute(command)


    def show_status_message(self, message: str, timeout: int = 3000) -> None:
        self.statusBar().showMessage(message, timeout)


    def update_window_title(self):
        title = "Dictator - Mini Editor"

        if self.current_file:
            title = f"Dictator - {self.current_file}"

        if self.editor.document().isModified():
            title += " *"

        self.setWindowTitle(title)


    def maybe_save_changes(self) -> bool:
        if not self.editor.document().isModified():
            return True

        result = QMessageBox.question(
            self,
            "Änderungen speichern?",
            "Das Dokument wurde geändert. Möchtest du die Änderungen speichern?",
            QMessageBox.StandardButton.Save
            | QMessageBox.StandardButton.Discard
            | QMessageBox.StandardButton.Cancel,
        )

        if result == QMessageBox.StandardButton.Save:
            return self.save_file()

        if result == QMessageBox.StandardButton.Discard:
            return True

        return False


    def closeEvent(self, event):
        if self.llm_thread is not None and self.llm_thread.isRunning():
            QMessageBox.information(
                self,
                "KI arbeitet noch",
                "Bitte warte, bis die KI-Aktion abgeschlossen ist.",
            )
            event.ignore()
            return

        if self.maybe_save_changes():
            event.accept()
        else:
            event.ignore()


    def set_heading(self, level: int) -> None:
        fmt = QTextCharFormat()

        if level == 1:
            fmt.setFontPointSize(24)
            fmt.setFontWeight(QFont.Weight.Bold)
        elif level == 2:
            fmt.setFontPointSize(18)
            fmt.setFontWeight(QFont.Weight.Bold)
        else:
            fmt.setFontPointSize(12)
            fmt.setFontWeight(QFont.Weight.Normal)

        cursor = self.editor.textCursor()
        cursor.mergeCharFormat(fmt)
        self.editor.mergeCurrentCharFormat(fmt)


    def set_normal_text(self) -> None:
        fmt = QTextCharFormat()
        fmt.setFontPointSize(12)
        fmt.setFontWeight(QFont.Weight.Normal)
        fmt.setFontItalic(False)

        cursor = self.editor.textCursor()
        cursor.mergeCharFormat(fmt)
        self.editor.mergeCurrentCharFormat(fmt)


    def align_left(self) -> None:
        self.editor.setAlignment(Qt.AlignmentFlag.AlignLeft)


    def align_center(self) -> None:
        self.editor.setAlignment(Qt.AlignmentFlag.AlignCenter)


    def align_right(self) -> None:
        self.editor.setAlignment(Qt.AlignmentFlag.AlignRight)


    def toggle_bullet_list(self) -> None:
        cursor = self.editor.textCursor()

        list_format = QTextListFormat()
        list_format.setStyle(QTextListFormat.Style.ListDisc)

        cursor.createList(list_format)


    def toggle_numbered_list(self) -> None:
        cursor = self.editor.textCursor()

        list_format = QTextListFormat()
        list_format.setStyle(QTextListFormat.Style.ListDecimal)

        cursor.createList(list_format)


    def remove_list_format(self) -> None:
        cursor = self.editor.textCursor()
        document = self.editor.document()

        start = cursor.selectionStart()
        end = cursor.selectionEnd()

        cursor.beginEditBlock()

        block = document.findBlock(start)

        while block.isValid() and block.position() <= end:
            block_cursor = self.editor.textCursor()
            block_cursor.setPosition(block.position())

            text_list = block.textList()
            if text_list is not None:
                text_list.remove(block)

            block_format = block.blockFormat()
            block_format.setIndent(0)

            block_cursor.setBlockFormat(block_format)

            block = block.next()

        cursor.endEditBlock()


    def indent_text(self) -> None:
        cursor = self.editor.textCursor()
        block_format = cursor.blockFormat()
        block_format.setIndent(block_format.indent() + 1)
        cursor.setBlockFormat(block_format)


    def outdent_text(self) -> None:
        cursor = self.editor.textCursor()
        block_format = cursor.blockFormat()
        current_indent = block_format.indent()

        if current_indent > 0:
            block_format.setIndent(current_indent - 1)
            cursor.setBlockFormat(block_format)


    def set_font_size(self, size: int) -> None:
        fmt = QTextCharFormat()
        fmt.setFontPointSize(size)

        cursor = self.editor.textCursor()
        cursor.mergeCharFormat(fmt)
        self.editor.mergeCurrentCharFormat(fmt)


    def set_font_family(self, family: str) -> bool:
        available_families = QFontDatabase.families()

        matching_family = None

        for available_family in available_families:
            if available_family.lower() == family.lower():
                matching_family = available_family
                break

        if matching_family is None:
            self.show_status_message(f"Schriftart nicht gefunden: {family}")
            return False

        fmt = QTextCharFormat()
        fmt.setFontFamilies([matching_family])

        cursor = self.editor.textCursor()
        cursor.mergeCharFormat(fmt)
        self.editor.mergeCurrentCharFormat(fmt)

        return True


    def insert_text(self, text: str) -> None:
        cursor = self.editor.textCursor()
        cursor.insertText(text)


    def find_text(self, search_text: str) -> bool:
        if not search_text:
            self.show_status_message("Kein Suchtext angegeben")
            return False

        found = self.editor.find(search_text)

        if found:
            self.show_status_message(f"Gefunden: {search_text}")
            return True

        # Wenn ab Cursorposition nichts gefunden wurde, von vorne suchen
        cursor = self.editor.textCursor()
        cursor.movePosition(cursor.MoveOperation.Start)
        self.editor.setTextCursor(cursor)

        found = self.editor.find(search_text)

        if found:
            self.show_status_message(f"Gefunden ab Dokumentanfang: {search_text}")
            return True

        self.show_status_message(f"Nicht gefunden: {search_text}")
        return False

    def replace_selection(self, replacement_text: str) -> bool:
        cursor = self.editor.textCursor()

        if not cursor.hasSelection():
            self.show_status_message("Keine Auswahl zum Ersetzen vorhanden")
            return False

        cursor.insertText(replacement_text)
        self.show_status_message("Auswahl ersetzt")
        return True


    def replace_next_text(self, search_text: str, replacement_text: str) -> bool:
        if not search_text:
            self.show_status_message("Kein Suchtext angegeben")
            return False

        found = self.editor.find(search_text)

        if not found:
            cursor = self.editor.textCursor()
            cursor.movePosition(cursor.MoveOperation.Start)
            self.editor.setTextCursor(cursor)

            found = self.editor.find(search_text)

        if not found:
            self.show_status_message(f"Nicht gefunden: {search_text}")
            return False

        cursor = self.editor.textCursor()
        cursor.insertText(replacement_text)

        self.show_status_message(
            f"Ersetzt: {search_text} → {replacement_text}"
        )
        return True


    def insert_generated_text_as_paragraph(self, text: str, position: int) -> None:
        cursor = self.editor.textCursor()

        max_position = self.editor.document().characterCount() - 1
        safe_position = min(position, max_position)

        cursor.setPosition(safe_position)
        self.editor.setTextCursor(cursor)

        if not cursor.atBlockStart():
            cursor.insertText("\n")

        cursor.insertText(text)

        if not text.endswith("\n"):
            cursor.insertText("\n")


    def insert_text_at_position(self, text: str, position: int) -> None:
        cursor = self.editor.textCursor()

        max_position = self.editor.document().characterCount() - 1
        safe_position = min(position, max_position)

        cursor.setPosition(safe_position)

        text_to_insert = self.prepare_inline_insert_text(text, safe_position)

        cursor.insertText(text_to_insert)
        self.editor.setTextCursor(cursor)


    def prepare_inline_insert_text(self, text: str, position: int) -> str:
        if not text:
            return text

        document_text = self.editor.toPlainText()

        if position <= 0:
            return text

        if position > len(document_text):
            return text

        previous_char = document_text[position - 1]
        first_char = text[0]

        if previous_char.isspace():
            return text

        if first_char.isspace():
            return text

        if first_char in ".,;:!?)]}":
            return text

        return " " + text


    def generate_text_async(self, llm_client, prompt: str) -> None:
        if self.llm_thread is not None and self.llm_thread.isRunning():
            self.show_status_message("Die KI arbeitet bereits")
            return

        current_cursor = self.editor.textCursor()
        insert_position = current_cursor.position()

        self.show_status_message("KI generiert Text ...")
        self.set_command_input_enabled(False)

        self.llm_thread = QThread()
        self.llm_worker = LlmWorker(
            llm_client=llm_client,
            mode="generate",
            prompt=prompt,
            insert_position=insert_position,
        )

        self.llm_worker.moveToThread(self.llm_thread)

        self.llm_thread.started.connect(self.llm_worker.run)
        self.llm_worker.finished.connect(self.on_llm_generation_finished)
        self.llm_worker.failed.connect(self.on_llm_generation_failed)

        self.llm_worker.finished.connect(self.llm_thread.quit)
        self.llm_worker.failed.connect(self.llm_thread.quit)

        self.llm_thread.finished.connect(self.llm_worker.deleteLater)
        self.llm_thread.finished.connect(self.llm_thread.deleteLater)
        self.llm_thread.finished.connect(self.clear_llm_worker)

        self.llm_thread.start()


    def on_llm_generation_finished(
        self,
        generated_text: str,
        start_position: int,
        end_position: int,
        mode: str,
    ) -> None:
        self.set_command_input_enabled(True)

        if mode == "generate":
            self.insert_generated_text_as_paragraph(generated_text, start_position)
            self.show_status_message("KI-Text eingefügt")

        elif mode == "continue":
            self.insert_text_at_position(generated_text, start_position)
            self.show_status_message("KI-Fortsetzung eingefügt")

        elif mode == "transform":
            self.replace_text_range(generated_text, start_position, end_position)
            self.show_status_message("KI-Auswahl ersetzt")

        else:
            self.show_status_message(f"Unbekannter KI-Modus: {mode}")


    def on_llm_generation_failed(self, error_message: str) -> None:
        self.set_command_input_enabled(True)

        clean_message = error_message.replace("[Fehler]", "").strip()

        self.show_status_message("KI-Fehler")

        QMessageBox.warning(
            self,
            "KI-Fehler",
            clean_message,
        )


    def clear_llm_worker(self) -> None:
        self.llm_thread = None
        self.llm_worker = None


    def transform_selection_async(self, llm_client, instruction: str) -> None:
        if self.llm_thread is not None and self.llm_thread.isRunning():
            self.show_status_message("Die KI arbeitet bereits")
            return

        cursor = self.editor.textCursor()

        if not cursor.hasSelection():
            self.show_status_message("Bitte zuerst Text markieren")
            return

        selection_start = cursor.selectionStart()
        selection_end = cursor.selectionEnd()
        selected_text = cursor.selectedText().replace("\u2029", "\n")

        self.show_status_message("KI bearbeitet Auswahl ...")
        self.set_command_input_enabled(False)

        self.llm_thread = QThread()
        self.llm_worker = LlmWorker(
            llm_client=llm_client,
            mode="transform",
            prompt=instruction,
            insert_position=selection_start,
            selection_end=selection_end,
            selected_text=selected_text,
        )

        self.llm_worker.moveToThread(self.llm_thread)

        self.llm_thread.started.connect(self.llm_worker.run)
        self.llm_worker.finished.connect(self.on_llm_generation_finished)
        self.llm_worker.failed.connect(self.on_llm_generation_failed)

        self.llm_worker.finished.connect(self.llm_thread.quit)
        self.llm_worker.failed.connect(self.llm_thread.quit)

        self.llm_thread.finished.connect(self.llm_worker.deleteLater)
        self.llm_thread.finished.connect(self.llm_thread.deleteLater)
        self.llm_thread.finished.connect(self.clear_llm_worker)

        self.llm_thread.start()


    def replace_text_range(self, replacement_text: str, start_position: int, end_position: int) -> None:
        cursor = self.editor.textCursor()

        max_position = self.editor.document().characterCount() - 1
        safe_start = min(start_position, max_position)
        safe_end = min(end_position, max_position)

        cursor.setPosition(safe_start)
        cursor.setPosition(safe_end, cursor.MoveMode.KeepAnchor)
        cursor.insertText(replacement_text)

        self.editor.setTextCursor(cursor)


    def get_text_before_cursor(self, max_characters: int = 2000) -> str:
        cursor = self.editor.textCursor()
        position = cursor.position()

        full_text = self.editor.toPlainText()
        context = full_text[:position]

        if len(context) > max_characters:
            context = context[-max_characters:]

        return context.strip()


    def continue_text_async(self, llm_client) -> None:
        if self.llm_thread is not None and self.llm_thread.isRunning():
            self.show_status_message("Die KI arbeitet bereits")
            return

        context_text = self.get_text_before_cursor()

        if not context_text:
            self.show_status_message("Kein Kontext vor dem Cursor vorhanden")
            return

        current_cursor = self.editor.textCursor()
        insert_position = current_cursor.position()

        self.show_status_message("KI schreibt weiter ...")
        self.set_command_input_enabled(False)

        self.llm_thread = QThread()
        self.llm_worker = LlmWorker(
            llm_client=llm_client,
            mode="continue",
            prompt=context_text,
            insert_position=insert_position,
        )

        self.llm_worker.moveToThread(self.llm_thread)

        self.llm_thread.started.connect(self.llm_worker.run)
        self.llm_worker.finished.connect(self.on_llm_generation_finished)
        self.llm_worker.failed.connect(self.on_llm_generation_failed)

        self.llm_worker.finished.connect(self.llm_thread.quit)
        self.llm_worker.failed.connect(self.llm_thread.quit)

        self.llm_thread.finished.connect(self.llm_worker.deleteLater)
        self.llm_thread.finished.connect(self.llm_thread.deleteLater)
        self.llm_thread.finished.connect(self.clear_llm_worker)

        self.llm_thread.start()


    def set_command_input_enabled(self, enabled: bool) -> None:
        self.command_input.setEnabled(enabled)

        if enabled:
            self.command_input.setPlaceholderText(
                "z. B. fett, suche nach ..., generiere ..."
            )
        else:
            self.command_input.setPlaceholderText(
                "KI arbeitet ..."
            )


    def show_ai_status(self) -> None:
        settings = load_settings()
        settings_path = get_settings_path()

        message = (
            f"Modell: {settings['ollama_model_name']}\n"
            f"Ollama-Adresse: {settings['ollama_base_url']}\n"
            f"Settings-Datei:\n{settings_path}\n\n"
            f"Fake-Modus: {settings['use_fake_llm']}\n"
            f"Timeout: {settings['llm_timeout_seconds']} Sekunden\n\n"
            f"Generierung:\n"
            f"  Temperature: {settings['generate_temperature']}\n"
            f"  Num predict: {settings['generate_num_predict']}\n\n"
            f"Transformation:\n"
            f"  Temperature: {settings['transform_temperature']}\n"
            f"  Num predict: {settings['transform_num_predict']}\n\n"
            f"Fortsetzung:\n"
            f"  Temperature: {settings['continue_temperature']}\n"
            f"  Num predict: {settings['continue_num_predict']}"
        )

        QMessageBox.information(
            self,
            "KI-Status",
            message,
        )


    def show_ollama_test(self) -> None:
        status = self.command_router.llm_client.check_ollama_status()

        models_text = "\n".join(status["models"])

        if not models_text:
            models_text = "(keine Modelle gefunden)"

        message = (
            f"{status['message']}\n\n"
            f"Gefundene Modelle:\n"
            f"{models_text}"
        )

        if status["ok"]:
            QMessageBox.information(
                self,
                "Ollama-Test",
                message,
            )
        else:
            QMessageBox.warning(
                self,
                "Ollama-Test",
                message,
            )
