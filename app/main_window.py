from PySide6.QtCore import Qt, QThread, QTimer
from PySide6.QtPrintSupport import QPrinter, QPrintDialog
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
    QSizePolicy,
    QFrame,
)

from app.command_router import CommandRouter
from app.llm_worker import LlmWorker
from app.settings import get_settings_path, load_settings
from app.llm_client import LlmClient
from app.settings_dialog import SettingsDialog
from app.speech.recorder import AudioRecorder
from app.speech.transcriber import SpeechTranscriber
from app.speech.speech_worker import SpeechWorker
from app.localization import tr, voice_command_corrections
from app.version import APP_NAME, APP_VERSION
from app.logging_setup import get_logger

import os
import re


class MiniEditor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.logger = get_logger()
        self.logger.info("MainWindow initialized")

        self.setWindowTitle(tr("window_title_default"))
        self.resize(900, 650)

        paper_min_width = 451
        editor_area_margin = 24
        window_extra_margin = 40

        self.setMinimumWidth(
            paper_min_width
            + editor_area_margin * 2
            + window_extra_margin
        )

        self.setStyleSheet("""
            QWidget#editorArea {
                background-color: #d7ecff;
            }

            QTextEdit#paperEditor {
                background-color: white;
                color: black;
                border: 1px solid #d7ecff;
                padding: 48px;
                font-size: 12pt;
            }
            QFrame#separator {
                background-color: #8ac8ff;
                border: none;
                min-height: 1px;
                max-height: 1px;
            }
        """)

        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        editor_area = QWidget()
        editor_area.setObjectName("editorArea")

        editor_area_layout = QHBoxLayout(editor_area)
        editor_area_layout.setContentsMargins(
            editor_area_margin,
            editor_area_margin,
            editor_area_margin,
            editor_area_margin
        )

        self.editor = QTextEdit()
        self.editor.setObjectName("paperEditor")

        self.editor.setMinimumWidth(paper_min_width)
        self.editor.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )

        self.editor.document().modificationChanged.connect(self.update_window_title)

        editor_area_layout.addWidget(self.editor)

        layout.addWidget(editor_area)

        self.command_router = CommandRouter(self)

        speech_button_layout = QHBoxLayout()

        self.dictation_button = QPushButton(tr("button_dictation_start"))
        self.dictation_button.setCheckable(True)
        self.dictation_button.toggled.connect(self.toggle_dictation)
        self.dictation_button.setToolTip(tr("tooltip_dictation"))
        speech_button_layout.addWidget(self.dictation_button)

        self.voice_command_button = QPushButton(tr("button_voice_command_start"))
        self.voice_command_button.setCheckable(True)
        self.voice_command_button.toggled.connect(self.toggle_voice_command)
        self.voice_command_button.setToolTip(tr("tooltip_voice_command"))
        speech_button_layout.addWidget(self.voice_command_button)
        self.speech_buttons_top_separator = self.create_separator()
        layout.addWidget(self.speech_buttons_top_separator)

        layout.addLayout(speech_button_layout)

        self.speech_buttons_bottom_separator = self.create_separator()
        layout.addWidget(self.speech_buttons_bottom_separator)

        self.speech_top_separator = self.create_separator()
        layout.addWidget(self.speech_top_separator)

        self.speech_result_label = QLabel(tr("speech_result_empty"))
        self.speech_result_label.setWordWrap(True)
        layout.addWidget(self.speech_result_label)

        self.command_top_separator = self.create_separator()
        layout.addWidget(self.command_top_separator)

        self.command_row_layout = QHBoxLayout()

        self.command_label = QLabel(tr("command_label"))
        self.command_row_layout.addWidget(self.command_label)

        self.command_input = QLineEdit()
        self.command_input.setPlaceholderText(tr("command_placeholder"))
        self.command_input.returnPressed.connect(self.execute_command)
        self.command_row_layout.addWidget(self.command_input, 1)

        layout.addLayout(self.command_row_layout)

        self.status_top_separator = self.create_separator()
        layout.addWidget(self.status_top_separator)

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

        self.status_label = QLabel(tr("status_ready"))
        self.status_label.setContentsMargins(
            layout.contentsMargins().left(),
            0,
            0,
            6
        )

        self.statusBar().addWidget(self.status_label, 1)


    def create_separator(self) -> QFrame:
        separator = QFrame()
        separator.setObjectName("separator")
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFixedHeight(1)
        return separator


    def _create_actions(self):
        self.new_action = QAction(tr("action_new"), self)
        self.new_action.triggered.connect(self.new_file)

        self.open_action = QAction(tr("action_open"), self)
        self.open_action.triggered.connect(self.open_file)

        self.save_action = QAction(tr("action_save"), self)
        self.save_action.triggered.connect(self.save_file)

        self.save_as_action = QAction(tr("action_save_as"), self)
        self.save_as_action.triggered.connect(self.save_file_as)

        self.exit_action = QAction(tr("action_exit"), self)
        self.exit_action.triggered.connect(self.close)

        self.settings_action = QAction(tr("action_settings"), self)
        self.settings_action.triggered.connect(self.open_settings_dialog)

        self.about_action = QAction(tr("action_about"), self)
        self.about_action.triggered.connect(self.show_about_dialog)

        self.export_pdf_action = QAction(tr("action_export_pdf"), self)
        self.export_pdf_action.triggered.connect(self.export_pdf)

        self.print_action = QAction(tr("action_print"), self)
        self.print_action.triggered.connect(self.print_document)


    def _create_menus(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu(tr("menu_file"))
        file_menu.addAction(self.new_action)
        file_menu.addAction(self.open_action)
        file_menu.addAction(self.save_action)
        file_menu.addAction(self.save_as_action)
        file_menu.addSeparator()
        file_menu.addAction(self.export_pdf_action)
        file_menu.addAction(self.print_action)
        file_menu.addSeparator()
        file_menu.addAction(self.settings_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)

        help_menu = menu_bar.addMenu(tr("menu_help"))
        help_menu.addAction(self.about_action)


    def new_file(self):
        if not self.maybe_save_changes():
            return False

        self.editor.clear()
        self.current_file = None
        self.editor.document().setModified(False)
        self.update_window_title()
        self.show_status_message(tr("status_new_file_created"))
        return True


    def open_file(self):
        if not self.maybe_save_changes():
            return False

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            tr("dialog_open_file_title"),
            "",
            tr("file_filter_open"),
        )

        if not file_path:
            return False

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()

            lower_file_path = file_path.lower()

            if lower_file_path.endswith(".html"):
                self.editor.setHtml(content)

            elif lower_file_path.endswith((".md", ".markdown")):
                self.editor.setMarkdown(content)

            else:
                self.editor.setPlainText(content)

            self.current_file = file_path
            self.editor.document().setModified(False)
            self.update_window_title()
            self.show_status_message(tr("status_file_opened"))
            self.logger.info("File opened: %s", file_path)
            return True

        except OSError as error:
            self.logger.exception("Opening file failed: %s", file_path)
            QMessageBox.critical(
                self,
                tr("error_title"),
                tr("error_file_open", error=error),
            )
            return False


    def save_file(self):
        if self.current_file is None:
            return self.save_file_as()

        return self._write_file(self.current_file)


    def save_file_as(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            tr("dialog_save_file_title"),
            "",
            tr("file_filter_save"),
        )

        if not file_path:
            return False

        self.current_file = file_path
        return self._write_file(file_path)


    def _write_file(self, file_path):
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                lower_file_path = file_path.lower()

                if lower_file_path.endswith(".txt"):
                    file.write(self.editor.toPlainText())

                elif lower_file_path.endswith((".md", ".markdown")):
                    file.write(self.editor.document().toMarkdown())

                else:
                    file.write(self.editor.toHtml())

            self.editor.document().setModified(False)
            self.update_window_title()
            self.show_status_message(tr("status_file_saved"))
            self.logger.info("File saved: %s", file_path)
            return True

        except OSError as error:
            self.logger.exception("Writing file failed: %s", file_path)
            QMessageBox.critical(
                self,
                tr("error_title"),
                tr("error_file_save", error=error),
            )
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
                self.voice_command_button.setText(tr("button_voice_command_start"))

            self.dictation_button.setText(tr("button_dictation_stop"))
            self.show_status_message(tr("status_dictation_started"))
            self.start_dictation()
        else:
            self.dictation_button.setText(tr("button_dictation_start"))
            self.show_status_message(tr("status_dictation_stopped"))
            self.stop_dictation()


    def toggle_voice_command(self, checked: bool) -> None:
        if checked:
            if self.dictation_button.isChecked():
                self.dictation_button.blockSignals(True)
                self.dictation_button.setChecked(False)
                self.dictation_button.blockSignals(False)
                self.dictation_button.setText(tr("button_dictation_start"))

            self.voice_command_button.setText(tr("button_voice_command_stop"))
            self.show_status_message(tr("status_voice_command_started"))
            self.start_voice_command()
        else:
            self.voice_command_button.setText(tr("button_voice_command_start"))
            self.show_status_message(tr("status_voice_command_stopped"))
            self.stop_voice_command()


    def start_dictation(self) -> None:
        try:
            self.audio_recorder.start()
            self.show_status_message(tr("status_dictation_recording"))
        except Exception as error:
            self.dictation_button.setChecked(False)
            QMessageBox.warning(
                self,
                tr("dialog_dictation_title"),
                tr("error_recording_start", error=error),
            )


    def stop_dictation(self) -> None:
        try:
            audio_data = self.audio_recorder.stop()

            if audio_data is None:
                self.show_status_message(tr("status_no_recording"))
                return

            self.transcribe_dictation_async(audio_data)

        except Exception as error:
            QMessageBox.warning(
                self,
                tr("dialog_dictation_title"),
                tr("error_dictation_process", error=error),
            )


    def transcribe_dictation_async(self, audio_data) -> None:
        if self.speech_thread is not None and self.speech_thread.isRunning():
            self.show_status_message(tr("status_speech_already_running"))
            return

        self.show_status_message(tr("status_transcribing_dictation"))
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
        self.show_status_message(tr("status_dictation_inserted"))

    def on_speech_transcription_failed(self, error_message: str) -> None:
        self.set_speech_buttons_enabled(True)
        self.set_command_input_enabled(True)

        self.show_speech_result("")

        QMessageBox.warning(
            self,
            tr("dialog_speech_title"),
            error_message,
        )


    def clear_speech_worker(self) -> None:
        self.speech_thread = None
        self.speech_worker = None


    def start_voice_command(self) -> None:
        try:
            self.audio_recorder.start()
            self.show_status_message(tr("status_voice_command_recording"))
        except Exception as error:
            self.voice_command_button.setChecked(False)
            QMessageBox.warning(
                self,
                tr("dialog_voice_command_title"),
                tr("error_recording_start", error=error),
            )


    def stop_voice_command(self) -> None:
        try:
            audio_data = self.audio_recorder.stop()

            if audio_data is None:
                self.show_status_message(tr("status_no_recording"))
                return

            self.transcribe_voice_command_async(audio_data)

        except Exception as error:
            QMessageBox.warning(
                self,
                tr("dialog_voice_command_title"),
                tr("error_voice_command_process", error=error),
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
            self.show_status_message(tr("status_speech_already_running"))
            return

        self.show_status_message(tr("status_transcribing_voice_command"))
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
            self.show_status_message(tr("status_no_voice_command"))
            return

        self.command_input.setText(command)
        if command != text.strip():
            self.show_status_message(
                tr(
                    "status_voice_command_corrected",
                    original=text.strip(),
                    command=command,
                )
            )
        else:
            self.show_status_message(
                tr("status_voice_command_recognized", command=command)
            )

        self.command_router.execute(command)
        self.command_input.clear()


    def apply_voice_command_corrections(self, command: str) -> str:
        normalized = command.strip().lower()
        corrections = voice_command_corrections()

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
            self.speech_result_label.setText(
                tr("speech_result_text", text=text)
            )
        else:
            self.speech_result_label.setText(
                tr("speech_result_empty")
            )


    def show_status_message(self, message: str, timeout: int = 3000) -> None:
        self.status_label.setText(message)

        if timeout > 0:
            QTimer.singleShot(
                timeout,
                lambda: self.status_label.setText(tr("status_ready"))
            )


    def update_window_title(self):
        title = "SayScript - Editor"

        if self.current_file:
            title = f"SayScript - {self.current_file}"

        if self.editor.document().isModified():
            title += " *"

        self.setWindowTitle(title)


    def maybe_save_changes(self) -> bool:
        if not self.editor.document().isModified():
            return True

        result = QMessageBox.question(
            self,
            tr("dialog_save_changes_title"),
            tr("dialog_save_changes_text"),
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
                tr("dialog_ai_busy_title"),
                tr("dialog_ai_busy_text"),
            )
            event.ignore()
            return

        if self.speech_thread is not None and self.speech_thread.isRunning():
            QMessageBox.information(
                self,
                tr("dialog_speech_busy_title"),
                tr("dialog_speech_busy_text"),
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
            self.show_status_message(
                tr("status_font_not_found", family=family)
            )
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
            self.show_status_message(tr("status_no_search_text"))
            return False

        found = self.editor.find(search_text)

        if found:
            self.show_status_message(
                tr("status_found_text", text=search_text)
            )
            return True

        cursor = self.editor.textCursor()
        cursor.movePosition(cursor.MoveOperation.Start)
        self.editor.setTextCursor(cursor)

        found = self.editor.find(search_text)

        if found:
            self.show_status_message(
                tr("status_found_text_from_start", text=search_text)
            )
            return True

        self.show_status_message(
            tr("status_text_not_found", text=search_text)
        )
        return False


    def replace_selection(self, replacement_text: str) -> bool:
        cursor = self.editor.textCursor()

        if not cursor.hasSelection():
            self.show_status_message(tr("status_no_selection_to_replace"))
            return False

        cursor.insertText(replacement_text)
        self.show_status_message(tr("status_selection_replaced"))
        return True


    def replace_next_text(self, search_text: str, replacement_text: str) -> bool:
        if not search_text:
            self.show_status_message(tr("status_no_search_text"))

        found = self.editor.find(search_text)

        if not found:
            cursor = self.editor.textCursor()
            cursor.movePosition(cursor.MoveOperation.Start)
            self.editor.setTextCursor(cursor)

            found = self.editor.find(search_text)

        if not found:
            self.show_status_message(
                tr("status_text_not_found", text=search_text)
            )
            return False

        cursor = self.editor.textCursor()
        cursor.insertText(replacement_text)

        self.show_status_message(
            tr(
                "status_replaced_text",
                search_text=search_text,
                replacement_text=replacement_text,
            )
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
            self.show_status_message(tr("status_ai_already_working"))
            return

        current_cursor = self.editor.textCursor()
        insert_position = current_cursor.position()

        self.show_status_message(tr("status_ai_generating"))
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
            self.show_status_message(tr("status_ai_text_inserted"))

        elif mode == "continue":
            self.insert_text_at_position(generated_text, start_position)
            self.show_status_message(tr("status_ai_continuation_inserted"))

        elif mode == "transform":
            self.replace_text_range(generated_text, start_position, end_position)
            self.show_status_message(tr("status_ai_selection_replaced"))

        else:
            self.show_status_message(
                tr("status_unknown_ai_mode", mode=mode)
            )


    def on_llm_generation_failed(self, error_message: str) -> None:
        self.set_command_input_enabled(True)

        clean_message = (
            error_message
            .replace("[Fehler]", "")
            .replace("[Error]", "")
            .strip()
        )

        self.show_status_message(tr("status_ai_error"))

        QMessageBox.warning(
            self,
            tr("dialog_ai_error_title"),
            clean_message,
        )


    def clear_llm_worker(self) -> None:
        self.llm_thread = None
        self.llm_worker = None


    def transform_selection_async(self, llm_client, instruction: str) -> None:
        if self.llm_thread is not None and self.llm_thread.isRunning():
            self.show_status_message(tr("status_ai_already_working"))
            return

        cursor = self.editor.textCursor()

        if not cursor.hasSelection():
            self.show_status_message(tr("status_no_selection_for_ai"))
            return

        selection_start = cursor.selectionStart()
        selection_end = cursor.selectionEnd()
        selected_text = cursor.selectedText().replace("\u2029", "\n")

        self.show_status_message(tr("status_ai_transforming_selection"))
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
            self.show_status_message(tr("status_ai_already_working"))
            return

        context_text = self.get_text_before_cursor()

        if not context_text:
            self.show_status_message(tr("context_missing"))
            return

        current_cursor = self.editor.textCursor()
        insert_position = current_cursor.position()

        self.show_status_message(tr("status_ai_continuing"))
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

        fake_mode_text = (
            tr("ai_status_yes")
            if settings["use_fake_llm"]
            else tr("ai_status_no")
        )

        message = (
            f"{tr('ai_status_settings_path')}:\n"
            f"{get_settings_path()}\n\n"

            f"{tr('ai_status_ollama')}:\n"
            f"{tr('ai_status_base_url')}: {settings['ollama_base_url']}\n"
            f"{tr('ai_status_model')}: {settings['ollama_model_name']}\n"
            f"{tr('ai_status_timeout')}: {settings['llm_timeout_seconds']} s\n"
            f"{tr('ai_status_fake_mode')}: {fake_mode_text}\n\n"

            f"{tr('ai_status_generation')}:\n"
            f"{tr('ai_status_temperature')}: {settings['generate_temperature']}\n"
            f"{tr('ai_status_num_predict')}: {settings['generate_num_predict']} {tr('unit_tokens')}\n\n"

            f"{tr('ai_status_transform')}:\n"
            f"{tr('ai_status_temperature')}: {settings['transform_temperature']}\n"
            f"{tr('ai_status_num_predict')}: {settings['transform_num_predict']} {tr('unit_tokens')}\n\n"

            f"{tr('ai_status_continue')}:\n"
            f"{tr('ai_status_temperature')}: {settings['continue_temperature']}\n"
            f"{tr('ai_status_num_predict')}: {settings['continue_num_predict']} {tr('unit_tokens')}\n\n"

            f"{tr('ai_status_speech')}:\n"
            f"{tr('ai_status_speech_model')}: {settings['speech_model_size']}\n"
            f"{tr('ai_status_sample_rate')}: {settings['speech_sample_rate']} Hz\n"
            f"{tr('ai_status_device')}: {settings['speech_device']}\n"
            f"{tr('ai_status_compute_type')}: {settings['speech_compute_type']}\n"
            f"{tr('ai_status_beam_size')}: {settings['speech_beam_size']}\n\n"

            f"{tr('ai_status_interface_language')}: {settings['interface_language']}\n"
            f"{tr('ai_status_text_language')}: {settings['text_generation_language']}"
        )

        QMessageBox.information(
            self,
            tr("dialog_ai_status_title"),
            message,
        )


    def show_ollama_test(self) -> None:
        status = self.command_router.llm_client.check_ollama_status()

        models_text = "\n".join(status["models"])

        if not models_text:
            models_text = tr("ollama_test_no_models")

        availability_text = (
            tr("ollama_test_success_status")
            if status["ok"]
            else tr("ollama_test_failure_status")
        )

        message = (
            f"{availability_text}\n\n"
            f"{status['message']}\n\n"
            f"{tr('ollama_test_models')}:\n"
            f"{models_text}"
        )

        if status["ok"]:
            QMessageBox.information(
                self,
                tr("dialog_ollama_test_title"),
                message,
            )
        else:
            QMessageBox.warning(
                self,
                tr("dialog_ollama_test_title"),
                message,
            )


    def open_settings_dialog(self) -> None:
        dialog = SettingsDialog(self)
        self.logger.info("Settings dialog opened")

        if dialog.exec() == dialog.DialogCode.Accepted:
            self.command_router = CommandRouter(self)
            self.reload_speech_settings()
            self.refresh_translations()
            self.apply_ui_settings()
            self.show_status_message(tr("status_settings_saved"))
            self.logger.info("Settings changed via settings dialog")


    def apply_ui_settings(self) -> None:
        settings = load_settings()

        show_command_input = bool(settings["show_command_input"])
        show_speech_result = bool(settings["show_speech_result"])

        self.speech_buttons_bottom_separator.setVisible(True)

        self.speech_result_label.setVisible(show_speech_result)

        self.speech_top_separator.setVisible(False)

        self.command_label.setVisible(show_command_input)
        self.command_input.setVisible(show_command_input)

        self.command_top_separator.setVisible(
            show_speech_result and show_command_input
        )

        self.status_top_separator.setVisible(
            show_speech_result or show_command_input
        )


    def refresh_translations(self) -> None:
        self.update_window_title()

        self.new_action.setText(tr("action_new"))
        self.open_action.setText(tr("action_open"))
        self.save_action.setText(tr("action_save"))
        self.save_as_action.setText(tr("action_save_as"))
        self.print_action.setText(tr("action_print"))
        self.exit_action.setText(tr("action_exit"))
        self.export_pdf_action.setText(tr("action_export_pdf"))
        self.settings_action.setText(tr("action_settings"))
        self.about_action.setText(tr("action_about"))

        self.menuBar().clear()
        self._create_menus()

        if self.dictation_button.isChecked():
            self.dictation_button.setText(tr("button_dictation_stop"))
        else:
            self.dictation_button.setText(tr("button_dictation_start"))

        if self.voice_command_button.isChecked():
            self.voice_command_button.setText(tr("button_voice_command_stop"))
        else:
            self.voice_command_button.setText(tr("button_voice_command_start"))

        self.dictation_button.setToolTip(tr("tooltip_dictation"))
        self.voice_command_button.setToolTip(tr("tooltip_voice_command"))

        self.command_label.setText(tr("command_label"))
        self.command_input.setPlaceholderText(tr("command_placeholder"))

        self.show_speech_result("")

        self.status_label.setText(tr("status_ready"))


    def export_pdf(self) -> bool:
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            tr("dialog_export_pdf_title"),
            "",
            tr("file_filter_pdf"),
        )

        if not file_path:
            return False

        if not file_path.lower().endswith(".pdf"):
            file_path += ".pdf"

        try:
            printer = QPrinter(QPrinter.PrinterMode.HighResolution)
            printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
            printer.setOutputFileName(file_path)

            self.editor.document().print_(printer)

            self.show_status_message(tr("status_pdf_exported"))
            self.logger.info("PDF exported: %s", file_path)
            return True

        except Exception as error:
            self.logger.exception("PDF export failed")
            QMessageBox.critical(
                self,
                tr("error_title"),
                tr("error_pdf_export", error=error),
            )
            return False



    def print_document(self) -> bool:
        try:
            printer = QPrinter(QPrinter.PrinterMode.HighResolution)

            dialog = QPrintDialog(printer, self)
            dialog.setWindowTitle(tr("dialog_print_title"))

            if dialog.exec() != QPrintDialog.DialogCode.Accepted:
                return False

            self.editor.document().print_(printer)

            self.show_status_message(tr("status_printed"))
            self.logger.info("Document sent to printer")

            return True

        except Exception as error:
            self.logger.exception("Printing failed")
            QMessageBox.critical(
                self,
                tr("error_title"),
                tr("error_print", error=error),
            )
            return False


    def show_about_dialog(self) -> None:
        QMessageBox.information(
            self,
            tr("dialog_about_title"),
            tr(
                "about_text",
                app_name=APP_NAME,
                app_version=APP_VERSION,
            ),
        )
