from dataclasses import dataclass
from typing import Any
from app.llm_client import LlmClient
import re


@dataclass
class ParsedCommand:
    action: str
    value: Any = None


class CommandRouter:
    def __init__(self, editor_window):
        self.editor_window = editor_window
        self.editor = editor_window.editor
        self.llm_client = LlmClient()

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
            "continue_text": {
                "schreibe weiter",
                "schreib weiter",
                "weiter schreiben",
                "text fortsetzen",
                "fortsetzen",
                "führe fort",
                "fuehre fort",
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
        original_command = command.strip()
        normalized_command = self.normalize_command(original_command)

        if not normalized_command:
            return

        parsed_command = self.parse_command(original_command, normalized_command)

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


    def parse_command(
        self,
        original_command: str,
        normalized_command: str,
    ) -> ParsedCommand | None:
        font_size = self.parse_font_size(normalized_command)

        if font_size is not None:
            return ParsedCommand("font_size", font_size)

        font_family = self.parse_font_family(original_command, normalized_command)

        if font_family is not None:
            return ParsedCommand("font_family", font_family)

        insert_text = self.parse_insert_text(original_command, normalized_command)

        if insert_text is not None:
            return ParsedCommand("insert_text", insert_text)

        replacement_for_selection = self.parse_replace_selection(original_command, normalized_command)

        if replacement_for_selection is not None:
            return ParsedCommand("replace_selection", replacement_for_selection)

        search_replacement = self.parse_replace_text(original_command, normalized_command)

        if search_replacement is not None:
            return ParsedCommand("replace_text", search_replacement)

        search_text = self.parse_search_text(original_command, normalized_command)

        if search_text is not None:
            return ParsedCommand("search_text", search_text)

        transform_instruction = self.parse_transform_selection(
            original_command,
            normalized_command,
        )

        if transform_instruction is not None:
            return ParsedCommand("transform_selection", transform_instruction)

        action = self.get_action(normalized_command)

        if action is not None:
            return ParsedCommand(action)

        generation_prompt = self.parse_generate_text(original_command, normalized_command)

        if generation_prompt is not None:
            return ParsedCommand("generate_text", generation_prompt)

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

        elif action == "search_text":
            self.editor_window.find_text(value)

        elif action == "replace_selection":
            self.editor_window.replace_selection(value)

        elif action == "replace_text":
            search_text, replacement_text = value
            self.editor_window.replace_next_text(search_text, replacement_text)

        elif action == "transform_selection":
            self.editor_window.transform_selection_async(self.llm_client, value)

        elif action == "generate_text":
            self.editor_window.generate_text_async(self.llm_client, value)

        elif action == "continue_text":
            self.editor_window.continue_text_async(self.llm_client)

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


    def parse_font_family(
        self,
        original_command: str,
        normalized_command: str,
    ) -> str | None:
        prefixes = {
            "schriftart",
            "schrift",
            "font",
            "font family",
        }

        family = self.extract_argument_after_prefix(
            original_command,
            normalized_command,
            prefixes,
        )

        if family:
            return family

        return None


    def parse_insert_text(
        self,
        original_command: str,
        normalized_command: str,
    ) -> str | None:
        prefixes = {
            "füge ein",
            "fuege ein",
            "einfügen",
            "einfuegen",
            "text einfügen",
            "text einfuegen",
        }

        text = self.extract_argument_after_prefix(
            original_command,
            normalized_command,
            prefixes,
        )

        if text:
            return text

        return None

    def parse_search_text(
        self,
        original_command: str,
        normalized_command: str,
    ) -> str | None:
        prefixes = {
            "suche nach",
            "suche",
            "finde",
            "find",
            "search",
            "search for",
        }

        text = self.extract_argument_after_prefix(
            original_command,
            normalized_command,
            prefixes,
        )

        if text:
            return text

        return None


    def parse_replace_selection(
        self,
        original_command: str,
        normalized_command: str,
    ) -> str | None:
        prefixes = {
            "ersetze auswahl durch",
            "ersetze markierung durch",
            "ersetze selektion durch",
            "ersetze durch",
            "auswahl ersetzen durch",
            "markierung ersetzen durch",
        }

        text = self.extract_argument_after_prefix(
            original_command,
            normalized_command,
            prefixes,
        )

        if text:
            return text

        return None


    def extract_argument_after_prefix(
        self,
        original_command: str,
        normalized_command: str,
        prefixes: set[str],
    ) -> str | None:
        original_stripped = original_command.strip()

        for prefix in prefixes:
            normalized_prefix = self.normalize_command(prefix)

            if normalized_command == normalized_prefix:
                return ""

            if normalized_command.startswith(normalized_prefix + " "):
                return original_stripped[len(prefix):].strip()

        return None


    def parse_replace_text(
        self,
        original_command: str,
        normalized_command: str,
    ) -> tuple[str, str] | None:
        prefixes = {
            "ersetze",
            "ersetze nächstes",
            "ersetze naechstes",
        }

        for prefix in prefixes:
            argument = self.extract_argument_after_prefix(
                original_command,
                normalized_command,
                {prefix},
            )

            if argument is None:
                continue

            parts = re.split(r"\s+durch\s+", argument, maxsplit=1, flags=re.IGNORECASE)

            if len(parts) != 2:
                return None

            search_text = parts[0].strip()
            replacement_text = parts[1].strip()

            if search_text and replacement_text:
                return search_text, replacement_text

        return None


    def parse_generate_text(
        self,
        original_command: str,
        normalized_command: str,
    ) -> str | None:
        prefixes = {
            "generiere",
            "erzeuge",
            "erstelle",
            "verfasse",
            "schreibe einen text über",
            "schreibe einen absatz über",
            "schreibe eine einleitung zu",
            "schreib einen text über",
            "schreib einen absatz über",
        }

        prompt = self.extract_argument_after_prefix(
            original_command,
            normalized_command,
            prefixes,
        )

        if prompt:
            return prompt

        return None


    def parse_transform_selection(
        self,
        original_command: str,
        normalized_command: str,
    ) -> str | None:
        fixed_instructions = {
            "mach das höflicher": "Formuliere den Text höflicher.",
            "mache das höflicher": "Formuliere den Text höflicher.",
            "höflicher": "Formuliere den Text höflicher.",
            "mach das kürzer": "Kürze den Text deutlich.",
            "mache das kürzer": "Kürze den Text deutlich.",
            "kürzer": "Kürze den Text deutlich.",
            "mach das sachlicher": "Formuliere den Text sachlicher.",
            "mache das sachlicher": "Formuliere den Text sachlicher.",
            "sachlicher": "Formuliere den Text sachlicher.",
            "korrigiere das": "Korrigiere Rechtschreibung und Grammatik.",
            "korrigieren": "Korrigiere Rechtschreibung und Grammatik.",
            "fasse das zusammen": "Fasse den Text knapp zusammen.",
            "zusammenfassen": "Fasse den Text knapp zusammen.",
        }

        if normalized_command in fixed_instructions:
            return fixed_instructions[normalized_command]

        prefixes = {
            "überarbeite auswahl",
            "ueberarbeite auswahl",
            "überarbeite markierung",
            "ueberarbeite markierung",
            "bearbeite auswahl",
            "bearbeite markierung",
        }

        instruction = self.extract_argument_after_prefix(
            original_command,
            normalized_command,
            prefixes,
        )

        if instruction:
            return instruction

        return None
