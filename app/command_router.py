from dataclasses import dataclass
from typing import Any


@dataclass
class ParsedCommand:
    action: str
    value: Any = None


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
            "heading_1": {
                "überschrift 1",
                "überschrift eins",
                "hauptüberschrift",
                "titel",
                "mache überschrift 1",
                "mach überschrift 1",
            },
            "heading_2": {
                "überschrift 2",
                "überschrift zwei",
                "unterüberschrift",
                "mache überschrift 2",
                "mach überschrift 2",
            },
            "normal_text": {
                "normaler text",
                "normaltext",
                "standard text",
                "standardtext",
                "text normal",
                "normale schrift",
            },
            "align_left": {
                "linksbündig",
                "links ausrichten",
                "text links",
                "linke ausrichtung",
            },
            "align_center": {
                "zentrieren",
                "zentriert",
                "mittig",
                "text zentrieren",
                "zentriert ausrichten",
            },
            "align_right": {
                "rechtsbündig",
                "rechts ausrichten",
                "text rechts",
                "rechte ausrichtung",
            },
            "bullet_list": {
                "liste",
                "aufzählung",
                "aufzählungsliste",
                "punktliste",
                "liste mit punkten",
            },
            "numbered_list": {
                "nummerierte liste",
                "nummerierung",
                "zahlenliste",
                "liste mit zahlen",
            },
            "indent": {
                "einrücken",
                "text einrücken",
                "absatz einrücken",
                "rücke ein",
            },
            "outdent": {
                "ausrücken",
                "text ausrücken",
                "absatz ausrücken",
                "rücke aus",
            },
            "remove_list": {
                "liste entfernen",
                "liste löschen",
                "keine liste",
                "aufzählung entfernen",
                "nummerierung entfernen",
                "listenformat entfernen",
                "zurück zu text",
            },
        }


    def execute(self, command: str) -> None:
        normalized_command = self.normalize_command(command)

        if not normalized_command:
            return

        parsed_command = self.parse_command(normalized_command)

        if parsed_command is None:
            self.show_unknown_command(normalized_command)
            return

        self.run_command(parsed_command)


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


    def parse_command(self, command: str) -> ParsedCommand | None:
        font_size = self.parse_font_size(command)

        if font_size is not None:
            return ParsedCommand("font_size", font_size)

        font_family = self.parse_font_family(command)

        if font_family is not None:
            return ParsedCommand("font_family", font_family)

        insert_text = self.parse_insert_text(command)

        if insert_text is not None:
            return ParsedCommand("insert_text", insert_text)

        action = self.get_action(command)

        if action is not None:
            return ParsedCommand(action)

        return None


    def run_command(self, parsed_command: ParsedCommand) -> None:
        action = parsed_command.action
        value = parsed_command.value

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
            if self.editor_window.save_file():
                self.editor_window.show_status_message("Befehl ausgeführt: speichern")
            else:
                self.editor_window.show_status_message("Speichern abgebrochen")

        elif action == "open":
            if self.editor_window.open_file():
                self.editor_window.show_status_message("Befehl ausgeführt: öffnen")
            else:
                self.editor_window.show_status_message("Öffnen abgebrochen")

        elif action == "new_file":
            if self.editor_window.new_file():
                self.editor_window.show_status_message("Befehl ausgeführt: neue Datei")
            else:
                self.editor_window.show_status_message("Neue Datei abgebrochen")

        elif action == "heading_1":
            self.editor_window.set_heading(1)
            self.editor_window.show_status_message("Befehl ausgeführt: Überschrift 1")

        elif action == "heading_2":
            self.editor_window.set_heading(2)
            self.editor_window.show_status_message("Befehl ausgeführt: Überschrift 2")

        elif action == "normal_text":
            self.editor_window.set_normal_text()
            self.editor_window.show_status_message("Befehl ausgeführt: normaler Text")

        elif action == "align_left":
            self.editor_window.align_left()
            self.editor_window.show_status_message("Befehl ausgeführt: linksbündig")

        elif action == "align_center":
            self.editor_window.align_center()
            self.editor_window.show_status_message("Befehl ausgeführt: zentriert")

        elif action == "align_right":
            self.editor_window.align_right()
            self.editor_window.show_status_message("Befehl ausgeführt: rechtsbündig")

        elif action == "bullet_list":
            self.editor_window.toggle_bullet_list()
            self.editor_window.show_status_message("Befehl ausgeführt: Liste")

        elif action == "numbered_list":
            self.editor_window.toggle_numbered_list()
            self.editor_window.show_status_message("Befehl ausgeführt: nummerierte Liste")

        elif action == "remove_list":
            self.editor_window.remove_list_format()
            self.editor_window.show_status_message("Befehl ausgeführt: Liste entfernt")

        elif action == "indent":
            self.editor_window.indent_text()
            self.editor_window.show_status_message("Befehl ausgeführt: einrücken")

        elif action == "outdent":
            self.editor_window.outdent_text()
            self.editor_window.show_status_message("Befehl ausgeführt: ausrücken")

        elif action == "font_size":
            self.editor_window.set_font_size(value)
            self.editor_window.show_status_message(
                f"Befehl ausgeführt: Schriftgröße {value}"
            )

        elif action == "font_family":
            if self.editor_window.set_font_family(value):
                self.editor_window.show_status_message(
                    f"Befehl ausgeführt: Schriftart {value}"
                )

        elif action == "insert_text":
            self.editor_window.insert_text(value)
            self.editor_window.show_status_message("Befehl ausgeführt: Text eingefügt")

        else:
            self.show_unknown_command(action)


    def parse_font_size(self, command: str) -> int | None:
        prefixes = {
            "schriftgröße",
            "schriftgroesse",
            "schrift größe",
            "schrift groesse",
            "größe",
            "groesse",
        }

        for prefix in prefixes:
            if command.startswith(prefix + " "):
                value = command.removeprefix(prefix).strip()

                if value.isdigit():
                    size = int(value)

                    if 6 <= size <= 96:
                        return size

                    self.editor_window.show_status_message(
                        "Schriftgröße muss zwischen 6 und 96 liegen"
                    )
                    return None

        return None


    def parse_font_family(self, command: str) -> str | None:
        prefixes = {
            "schriftart",
            "schrift",
            "font",
            "font family",
        }

        for prefix in prefixes:
            if command.startswith(prefix + " "):
                family = command.removeprefix(prefix).strip()

                if family:
                    return family

        return None


    def parse_insert_text(self, command: str) -> str | None:
        prefixes = {
            "füge ein",
            "fuege ein",
            "einfügen",
            "einfuegen",
            "schreibe",
            "schreib",
            "text einfügen",
            "text einfuegen",
        }

        for prefix in prefixes:
            if command.startswith(prefix + " "):
                text = command.removeprefix(prefix).strip()

                if text:
                    return text

        return None

