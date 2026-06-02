from PySide6.QtWidgets import QMessageBox


class CommandRouter:
    def __init__(self, editor_window):
        self.editor_window = editor_window
        self.editor = editor_window.editor

        self.command_aliases = {
            "bold": {
                "fett",
                "mach fett",
                "text fett",
                "markierung fett",
                "fett formatieren",
                "auswahl fett",
            },
            "italic": {
                "kursiv",
                "mach kursiv",
                "text kursiv",
                "markierung kursiv",
                "kursiv formatieren",
                "auswahl kursiv",
            },
            "delete_selection": {
                "lösche auswahl",
                "auswahl löschen",
                "markierung löschen",
                "lösche markierung",
                "entferne auswahl",
                "entferne markierung",
            },
            "select_all": {
                "alles markieren",
                "gesamten text markieren",
                "markiere alles",
                "alles auswählen",
            },
            "new_line": {
                "neue zeile",
                "zeilenumbruch",
                "neuen absatz",
                "absatz",
            },
        }

    def execute(self, command: str) -> None:
        normalized_command = self.normalize_command(command)

        if not normalized_command:
            return

        action = self.get_action(normalized_command)

        if action == "bold":
            self.editor_window.toggle_bold()

        elif action == "italic":
            self.editor_window.toggle_italic()

        elif action == "delete_selection":
            self.delete_selection()

        elif action == "select_all":
            self.editor.selectAll()

        elif action == "new_line":
            self.insert_new_line()

        else:
            self.show_unknown_command(normalized_command)

    def normalize_command(self, command: str) -> str:
        return " ".join(command.strip().lower().split())

    def get_action(self, command: str) -> str | None:
        for action, aliases in self.command_aliases.items():
            if command in aliases:
                return action

        return None

    def delete_selection(self) -> None:
        cursor = self.editor.textCursor()

        if cursor.hasSelection():
            cursor.removeSelectedText()

    def insert_new_line(self) -> None:
        cursor = self.editor.textCursor()
        cursor.insertText("\n")

    def show_unknown_command(self, command: str) -> None:
        QMessageBox.information(
            self.editor_window,
            "Unbekannter Befehl",
            f"Der Befehl wurde nicht erkannt:\n{command}",
        )
