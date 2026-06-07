from PySide6.QtCore import Qt, QThread, QTimer
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
    QHBoxLayout,
    QPushButton,
)

from app.command_router import CommandRouter
from app.llm_worker import LlmWorker
from app.settings import get_settings_path, load_settings
from app.llm_client import LlmClient
from app.settings_dialog import SettingsDialog
from app.speech.recorder import AudioRecorder
from app.speech.transcriber import SpeechTranscriber
from app.speech.speech_worker import SpeechWorker
import os
import re


class MiniEditor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Dictator - Mini Editor")
        self.resize(900, 650)

        self.setStyleSheet("""
            QWidget#editorArea {
                background-color: #d8d8d8;
            }

            QTextEdit#paperEditor {
                background-color: white;
                color: black;
                border: 1px solid #b8b8b8;
                padding: 48px;
                font-size: 12pt;
            }
        """)

        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        editor_area = QWidget()
        editor_area.setObjectName("editorArea")

        editor_area_layout = QHBoxLayout(editor_area)
        editor_area_layout.setContentsMargins(24, 24, 24, 24)

        self.editor = QTextEdit()
        self.editor.setObjectName("paperEditor")
        self.editor.setFixedWidth(794)
        self.editor.setMinimumHeight(900)
        self.editor.document().modificationChanged.connect(self.update_window_title)

        editor_area_layout.addStretch()
        editor_area_layout.addWidget(self.editor)
        editor_area_layout.addStretch()

        layout.addWidget(editor_area)

        self.command_router = CommandRouter(self)

        speech_button_layout = QHBoxLayout()

        self.dictation_button = QPushButton("Diktieren")
        self.dictation_button.setCheckable(True)
        self.dictation_button.toggled.connect(self.toggle_dictation)
        self.dictation_button.setToolTip(
            "Diktat starten oder stoppen. Transkribierter Text wird in den Editor eingefügt."
        )
        speech_button_layout.addWidget(self.dictation_button)

        self.voice_command_button = QPushButton("Sprachbefehl")
        self.voice_command_button.setCheckable(True)
        self.voice_command_button.toggled.connect(self.toggle_voice_command)
        self.voice_command_button.setToolTip(
            "Sprachbefehl starten oder stoppen. Transkribierter Text wird als Befehl ausgeführt."
        )
        speech_button_layout.addWidget(self.voice_command_button)

        layout.addLayout(speech_button_layout)

        self.speech_result_label = QLabel("Erkannte Sprache: -")
        self.speech_result_label.setWordWrap(True)
        layout.addWidget(self.speech_result_label)

        self.command_label = QLabel("Befehl:")
        layout.addWidget(self.command_label)

        self.command_input = QLineEdit()
        self.command_input.setPlaceholderText("z. B. fett, suche nach ..., generiere ...")
        self.command_input.returnPressed.connect(self.execute_command)
        layout.addWidget(self.command_input)

        self.apply_ui_settings()

        self.setCentralWidget(central_widget)

        self.current_file = None

        self.llm_thread = None
        self.llm_worker = None

        self.speech_thread = None
        self.speech_worker = None

        settings = load_settings()

        self.audio_recorder = AudioRecorder(
            sample_rate=int(settings["speech_sample_rate"])
        )

        self.speech_transcriber = SpeechTranscriber(
            model_size=settings["speech_model_size"],
            sample_rate=int(settings["speech_sample_rate"]),
            device=settings["speech_device"],
            compute_type=settings["speech_compute_type"],
            beam_size=int(settings["speech_beam_size"]),
        )

        self._create_actions()
        self._create_menus()

        self.statusBar().setStyleSheet("""
            QStatusBar {
                padding-left: 24px;
            }
        """)

        self.status_label = QLabel("Bereit")
        self.status_label.setContentsMargins(
            layout.contentsMargins().left(),
            0,
            0,
            0
        )

        self.statusBar().addWidget(self.status_label, 1)


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

        self.settings_action = QAction("Einstellungen", self)
        self.settings_action.triggered.connect(self.open_settings_dialog)


    def _create_menus(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("Datei")
        file_menu.addAction(self.new_action)
        file_menu.addAction(self.open_action)
        file_menu.addAction(self.save_action)
        file_menu.addAction(self.save_as_action)
        file_menu.addSeparator()
        file_menu.addAction(self.settings_action)
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


    def toggle_dictation(self, checked: bool) -> None:
        if checked:
            if self.voice_command_button.isChecked():
                self.voice_command_button.blockSignals(True)
                self.voice_command_button.setChecked(False)
                self.voice_command_button.blockSignals(False)
                self.voice_command_button.setText("Sprachbefehl")

            self.dictation_button.setText("Diktieren stoppen")
            self.show_status_message("Diktat gestartet")
            self.start_dictation()
        else:
            self.dictation_button.setText("Diktieren")
            self.show_status_message("Diktat gestoppt")
            self.stop_dictation()


    def toggle_voice_command(self, checked: bool) -> None:
        if checked:
            if self.dictation_button.isChecked():
                self.dictation_button.blockSignals(True)
                self.dictation_button.setChecked(False)
                self.dictation_button.blockSignals(False)
                self.dictation_button.setText("Diktieren")

            self.voice_command_button.setText("Sprachbefehl stoppen")
            self.show_status_message("Sprachbefehl gestartet")
            self.start_voice_command()
        else:
            self.voice_command_button.setText("Sprachbefehl")
            self.show_status_message("Sprachbefehl gestoppt")
            self.stop_voice_command()


    def start_dictation(self) -> None:
        try:
            self.audio_recorder.start()
            self.show_status_message("Diktataufnahme läuft ...")
        except Exception as error:
            self.dictation_button.setChecked(False)
            QMessageBox.warning(
                self,
                "Diktieren",
                f"Die Aufnahme konnte nicht gestartet werden:\n{error}",
            )


    def stop_dictation(self) -> None:
        try:
            audio_data = self.audio_recorder.stop()

            if audio_data is None:
                self.show_status_message("Keine Aufnahme vorhanden")
                return

            self.transcribe_dictation_async(audio_data)

        except Exception as error:
            QMessageBox.warning(
                self,
                "Diktieren",
                f"Das Diktat konnte nicht verarbeitet werden:\n{error}",
            )


    def transcribe_dictation_async(self, audio_data) -> None:
        if self.speech_thread is not None and self.speech_thread.isRunning():
            self.show_status_message("Spracherkennung arbeitet bereits")
            return

        self.show_status_message("Transkribiere Diktat ...")
        self.set_speech_buttons_enabled(False)
        self.set_command_input_enabled(False)

        self.speech_thread = QThread()
        self.speech_worker = SpeechWorker(
            self.speech_transcriber,
            audio_data,
        )

        self.speech_worker.moveToThread(self.speech_thread)

        self.speech_thread.started.connect(self.speech_worker.run)
        self.speech_worker.finished.connect(self.on_dictation_transcription_finished)
        self.speech_worker.failed.connect(self.on_speech_transcription_failed)

        self.speech_worker.finished.connect(self.speech_thread.quit)
        self.speech_worker.failed.connect(self.speech_thread.quit)

        self.speech_thread.finished.connect(self.speech_worker.deleteLater)
        self.speech_thread.finished.connect(self.speech_thread.deleteLater)
        self.speech_thread.finished.connect(self.clear_speech_worker)

        self.speech_thread.start()


    def on_dictation_transcription_finished(self, text: str) -> None:
        self.set_speech_buttons_enabled(True)
        self.set_command_input_enabled(True)

        self.show_speech_result(text)
        self.insert_text_at_position(text, self.editor.textCursor().position())
        self.show_status_message("Diktat eingefügt")

    def on_speech_transcription_failed(self, error_message: str) -> None:
        self.set_speech_buttons_enabled(True)
        self.set_command_input_enabled(True)

        self.show_speech_result("")

        QMessageBox.warning(
            self,
            "Spracherkennung",
            error_message,
        )


    def clear_speech_worker(self) -> None:
        self.speech_thread = None
        self.speech_worker = None


    def start_voice_command(self) -> None:
        try:
            self.audio_recorder.start()
            self.show_status_message("Sprachbefehl-Aufnahme läuft ...")
        except Exception as error:
            self.voice_command_button.setChecked(False)
            QMessageBox.warning(
                self,
                "Sprachbefehl",
                f"Die Aufnahme konnte nicht gestartet werden:\n{error}",
            )


    def stop_voice_command(self) -> None:
        try:
            audio_data = self.audio_recorder.stop()

            if audio_data is None:
                self.show_status_message("Keine Aufnahme vorhanden")
                return

            self.transcribe_voice_command_async(audio_data)

        except Exception as error:
            QMessageBox.warning(
                self,
                "Sprachbefehl",
                f"Der Sprachbefehl konnte nicht verarbeitet werden:\n{error}",
            )


    def clean_voice_command_text(self, text: str) -> str:
        command = text.strip()

        # Typische Anführungszeichen entfernen
        command = command.strip("\"'„“‚‘")

        # Mehrfache Leerzeichen normalisieren
        command = re.sub(r"\s+", " ", command)

        # Satzzeichen am Ende entfernen, die Whisper gerne ergänzt
        command = command.rstrip(".,;:!?")

        # Danach nochmal Leerzeichen/Anführungszeichen entfernen
        command = command.strip().strip("\"'„“‚‘")

        # Häufige Transkriptionsvarianten korrigieren
        command = self.apply_voice_command_corrections(command)

        return command


    def transcribe_voice_command_async(self, audio_data) -> None:
        if self.speech_thread is not None and self.speech_thread.isRunning():
            self.show_status_message("Spracherkennung arbeitet bereits")
            return

        self.show_status_message("Transkribiere Sprachbefehl ...")
        self.set_speech_buttons_enabled(False)
        self.set_command_input_enabled(False)

        self.speech_thread = QThread()
        self.speech_worker = SpeechWorker(
            self.speech_transcriber,
            audio_data,
        )

        self.speech_worker.moveToThread(self.speech_thread)

        self.speech_thread.started.connect(self.speech_worker.run)
        self.speech_worker.finished.connect(self.on_voice_command_transcription_finished)
        self.speech_worker.failed.connect(self.on_speech_transcription_failed)

        self.speech_worker.finished.connect(self.speech_thread.quit)
        self.speech_worker.failed.connect(self.speech_thread.quit)

        self.speech_thread.finished.connect(self.speech_worker.deleteLater)
        self.speech_thread.finished.connect(self.speech_thread.deleteLater)
        self.speech_thread.finished.connect(self.clear_speech_worker)

        self.speech_thread.start()


    def on_voice_command_transcription_finished(self, text: str) -> None:
        self.set_speech_buttons_enabled(True)
        self.set_command_input_enabled(True)

        self.show_speech_result(text)

        command = self.clean_voice_command_text(text)

        if not command:
            self.show_status_message("Kein Sprachbefehl erkannt")
            return

        self.command_input.setText(command)
        if command != text.strip():
            self.show_status_message(f"Sprachbefehl erkannt: {text.strip()} → {command}")
        else:
            self.show_status_message(f"Sprachbefehl erkannt: {command}")

        self.command_router.execute(command)
        self.command_input.clear()


    def apply_voice_command_corrections(self, command: str) -> str:
        normalized = command.strip().lower()

        corrections = {
            "fett punkt": "fett",
            "fett ausrufezeichen": "fett",
            "kursiv punkt": "kursiv",
            "speichern punkt": "speichern",
            "öffnen punkt": "öffnen",
            "oeffnen": "öffnen",
            "rückgängig punkt": "rückgängig",
            "rueckgängig": "rückgängig",
            "rueckgaengig": "rückgängig",
            "wiederholen punkt": "wiederholen",
            "alles markieren punkt": "alles markieren",
            "neue zeile punkt": "neue zeile",
            "ki status punkt": "ki status",
            "ollama test punkt": "ollama test",
        }

        return corrections.get(normalized, command)


    def set_speech_buttons_enabled(self, enabled: bool) -> None:
        self.dictation_button.setEnabled(enabled)
        self.voice_command_button.setEnabled(enabled)


    def reload_speech_settings(self) -> None:
        settings = load_settings()

        self.audio_recorder = AudioRecorder(
            sample_rate=int(settings["speech_sample_rate"])
        )

        self.speech_transcriber = SpeechTranscriber(
            model_size=settings["speech_model_size"],
            sample_rate=int(settings["speech_sample_rate"]),
            device=settings["speech_device"],
            compute_type=settings["speech_compute_type"],
            beam_size=int(settings["speech_beam_size"]),
        )


    def show_speech_result(self, text: str) -> None:
        if text:
            self.speech_result_label.setText(f"Erkannte Sprache: {text}")
        else:
            self.speech_result_label.setText("Erkannte Sprache: -")


    def show_status_message(self, message: str, timeout: int = 3000) -> None:
        self.status_label.setText(message)

        if timeout > 0:
            QTimer.singleShot(
                timeout,
                lambda: self.status_label.setText("Bereit")
            )


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

        if self.speech_thread is not None and self.speech_thread.isRunning():
            QMessageBox.information(
                self,
                "Spracherkennung arbeitet noch",
                "Bitte warte, bis die Transkription abgeschlossen ist.",
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
            f"Settings-Datei:\n{settings_path}\n\n"

            f"Ollama / Qwen:\n"
            f"  Modell: {settings['ollama_model_name']}\n"
            f"  Ollama-Adresse: {settings['ollama_base_url']}\n"
            f"  Fake-Modus: {settings['use_fake_llm']}\n"
            f"  Timeout: {settings['llm_timeout_seconds']} Sekunden\n\n"

            f"Generierung:\n"
            f"  Temperature: {settings['generate_temperature']}\n"
            f"  Num predict: {settings['generate_num_predict']}\n\n"

            f"Transformation:\n"
            f"  Temperature: {settings['transform_temperature']}\n"
            f"  Num predict: {settings['transform_num_predict']}\n\n"

            f"Fortsetzung:\n"
            f"  Temperature: {settings['continue_temperature']}\n"
            f"  Num predict: {settings['continue_num_predict']}\n\n"

            f"Spracherkennung / Whisper:\n"
            f"  Modell: {settings['speech_model_size']}\n"
            f"  Sample Rate: {settings['speech_sample_rate']} Hz\n"
            f"  Device: {settings['speech_device']}\n"
            f"  Compute Type: {settings['speech_compute_type']}\n"
            f"  Beam Size: {settings['speech_beam_size']}"
        )

        QMessageBox.information(
            self,
            "Systemstatus",
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


    def open_settings_dialog(self) -> None:
        dialog = SettingsDialog(self)

        if dialog.exec() == dialog.DialogCode.Accepted:
            self.command_router.llm_client = LlmClient()
            self.reload_speech_settings()
            self.apply_ui_settings()
            self.show_status_message("Einstellungen gespeichert")


    def apply_ui_settings(self) -> None:
        settings = load_settings()
        show_command_input = bool(settings["show_command_input"])

        self.command_label.setVisible(show_command_input)
        self.command_input.setVisible(show_command_input)
