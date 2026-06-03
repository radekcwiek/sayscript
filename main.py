import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import (
    QAction,
    QTextCharFormat,
    QFont,
    QTextListFormat,
    QTextBlockFormat,
    QFontDatabase,
    QTextDocument,
)
from PySide6.QtWidgets import (
    QApplication,
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


def main():
    app = QApplication(sys.argv)
    window = MiniEditor()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
