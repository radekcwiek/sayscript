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
            "undo": {
                "rückgängig",
                "mach rückgängig",
                "letzte aktion rückgängig",
                "undo",
            },
            "redo": {
                "wiederholen",
                "wiederherstellen",
                "redo",
            },
            "cut": {
                "ausschneiden",
                "auswahl ausschneiden",
                "markierung ausschneiden",
            },
            "copy": {
                "kopieren",
                "auswahl kopieren",
                "markierung kopieren",
            },
            "paste": {
                "einfügen",
                "aus zwischenablage einfügen",
                "text einfügen",
            },
            "save": {
                "speichern",
                "datei speichern",
                "dokument speichern",
            },
            "open": {
                "öffnen",
                "datei öffnen",
                "dokument öffnen",
            },
            "new_file": {
                "neu",
                "neue datei",
                "neues dokument",
                "dokument neu",
            },
        }

    def execute(self, command: str) -> None:
        normalized_command = self.normalize_command(command)

        if not normalized_command:
            return

        action = self.get_action(normalized_command)

        if action == "bold":
            self.editor_window.toggle_bold()
            self.editor_window.show_status_message("Befehl ausgeführt: fett")

        elif action == "italic":
            self.editor_window.toggle_italic()
            self.editor_window.show_status_message("Befehl ausgeführt: kursiv")

        elif action == "delete_selection":
            self.delete_selection()
            self.editor_window.show_status_message("Befehl ausgeführt: Auswahl gelöscht")

        elif action == "select_all":
            self.editor.selectAll()
            self.editor_window.show_status_message("Befehl ausgeführt: alles markiert")

        elif action == "new_line":
            self.insert_new_line()
            self.editor_window.show_status_message("Befehl ausgeführt: neue Zeile")

        elif action == "undo":
            self.editor.undo()
            self.editor_window.show_status_message("Befehl ausgeführt: rückgängig")

        elif action == "redo":
            self.editor.redo()
            self.editor_window.show_status_message("Befehl ausgeführt: wiederholen")

        elif action == "cut":
            self.editor.cut()
            self.editor_window.show_status_message("Befehl ausgeführt: ausschneiden")

        elif action == "copy":
            self.editor.copy()
            self.editor_window.show_status_message("Befehl ausgeführt: kopieren")

        elif action == "paste":
            self.editor.paste()
            self.editor_window.show_status_message("Befehl ausgeführt: einfügen")

        elif action == "save":
            self.editor_window.save_file()
            self.editor_window.show_status_message("Befehl ausgeführt: speichern")

        elif action == "open":
            self.editor_window.open_file()
            self.editor_window.show_status_message("Befehl ausgeführt: öffnen")

        elif action == "new_file":
            self.editor_window.new_file()
            self.editor_window.show_status_message("Befehl ausgeführt: neue Datei")

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
        self.editor_window.show_status_message(
            f"Unbekannter Befehl: {command}"
        )
