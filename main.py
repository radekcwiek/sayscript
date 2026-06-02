import sys

from PySide6.QtGui import QAction, QTextCharFormat, QFont
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTextEdit,
    QFileDialog,
    QMessageBox,
)


class MiniEditor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Dictator - Mini Editor")
        self.resize(900, 650)

        self.editor = QTextEdit()
        self.setCentralWidget(self.editor)

        self.current_file = None

        self._create_actions()
        self._create_menus()

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
        self.editor.clear()
        self.current_file = None
        self.setWindowTitle("Voice Writer - Mini Editor")

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Datei öffnen",
            "",
            "HTML-Dateien (*.html);;Textdateien (*.txt);;Alle Dateien (*.*)",
        )

        if not file_path:
            return

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()

            if file_path.lower().endswith(".html"):
                self.editor.setHtml(content)
            else:
                self.editor.setPlainText(content)

            self.current_file = file_path
            self.setWindowTitle(f"Voice Writer - {file_path}")

        except OSError as error:
            QMessageBox.critical(self, "Fehler", f"Datei konnte nicht geöffnet werden:\n{error}")

    def save_file(self):
        if self.current_file is None:
            self.save_file_as()
            return

        self._write_file(self.current_file)

    def save_file_as(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Datei speichern",
            "",
            "HTML-Dateien (*.html);;Textdateien (*.txt)",
        )

        if not file_path:
            return

        self.current_file = file_path
        self._write_file(file_path)
        self.setWindowTitle(f"Voice Writer - {file_path}")

    def _write_file(self, file_path):
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                if file_path.lower().endswith(".txt"):
                    file.write(self.editor.toPlainText())
                else:
                    file.write(self.editor.toHtml())

        except OSError as error:
            QMessageBox.critical(self, "Fehler", f"Datei konnte nicht gespeichert werden:\n{error}")

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


def main():
    app = QApplication(sys.argv)
    window = MiniEditor()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
