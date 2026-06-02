from PySide6.QtWidgets import QMessageBox


class CommandRouter:
    def __init__(self, editor_window):
        self.editor_window = editor_window
        self.editor = editor_window.editor

    def execute(self, command: str) -> None:
        command = command.strip().lower()

        if not command:
            return

        if command == "fett":
            self.editor_window.toggle_bold()

        elif command == "kursiv":
            self.editor_window.toggle_italic()

        elif command == "lösche auswahl":
            self.delete_selection()

        elif command == "alles markieren":
            self.editor.selectAll()

        elif command == "neue zeile":
            self.insert_new_line()

        else:
            QMessageBox.information(
                self.editor_window,
                "Unbekannter Befehl",
                f"Der Befehl wurde nicht erkannt:\n{command}",
            )

    def delete_selection(self) -> None:
        cursor = self.editor.textCursor()

        if cursor.hasSelection():
            cursor.removeSelectedText()

    def insert_new_line(self) -> None:
        cursor = self.editor.textCursor()
        cursor.insertText("\n")
