# SPDX-License-Identifier: Apache-2.0

"""
Command parsing and dispatching for SayScript.

CommandRouter translates typed or spoken commands into internal editor actions.
It does not own the GUI itself. Instead, it calls methods on the main editor
window, for example toggle_bold(), save_file(), or generate_text_async().

The command aliases are language-dependent and come from app.locales.de or
app.locales.en through the localization module.
"""

from dataclasses import dataclass
from difflib import SequenceMatcher
import re
from typing import Any

from app.llm_client import LlmClient
from app.localization import command_message, get_command_language_module


@dataclass
class ParsedCommand:
    """
    Parsed representation of a command.

    action:
        Internal action name, for example "bold", "save", or "generate_text".

    value:
        Optional payload for the action. Examples:
        - font size as int
        - text to insert as str
        - search/replace pair as tuple[str, str]
        - fuzzy-match metadata as dict
    """

    action: str
    value: Any = None


class CommandRouter:
    """
    Convert user commands into editor operations.

    The router accepts both manual command-line input and cleaned voice command
    text. It first parses commands into ParsedCommand objects and then executes
    them against the main editor window.
    """

    def __init__(self, editor_window):
        self.editor_window = editor_window
        self.editor = editor_window.editor
        self.llm_client = LlmClient()

        self.language = get_command_language_module()
        self.command_aliases = self.language.COMMAND_ALIASES

    # Public entry point ----------------------------------------------------

    def execute(self, command: str) -> None:
        """
        Parse and execute a command string.

        Empty commands are ignored. Unknown commands are reported through the
        main window's status message system.
        """
        original_command = command.strip()
        normalized_command = self.normalize_command(original_command)

        if not normalized_command:
            return

        parsed_command = self.parse_command(original_command, normalized_command)

        if parsed_command is None:
            self.show_unknown_command(normalized_command)
            return

        self.run_command(parsed_command)

    # Parsing ---------------------------------------------------------------

    def parse_command(
        self,
        original_command: str,
        normalized_command: str,
    ) -> ParsedCommand | None:
        """
        Convert a normalized command into a ParsedCommand.

        Parsing order matters. More specific commands with arguments are tested
        before simple alias commands and fuzzy matching.
        """
        font_size = self.parse_font_size(normalized_command)

        if font_size is not None:
            return ParsedCommand("font_size", font_size)

        font_family = self.parse_font_family(
            original_command,
            normalized_command,
        )

        if font_family is not None:
            return ParsedCommand("font_family", font_family)

        insert_text = self.parse_insert_text(
            original_command,
            normalized_command,
        )

        if insert_text is not None:
            return ParsedCommand("insert_text", insert_text)

        replacement_for_selection = self.parse_replace_selection(
            original_command,
            normalized_command,
        )

        if replacement_for_selection is not None:
            return ParsedCommand(
                "replace_selection",
                replacement_for_selection,
            )

        search_replacement = self.parse_replace_text(
            original_command,
            normalized_command,
        )

        if search_replacement is not None:
            return ParsedCommand("replace_text", search_replacement)

        search_text = self.parse_search_text(
            original_command,
            normalized_command,
        )

        if search_text is not None:
            return ParsedCommand("search_text", search_text)

        transform_instruction = self.parse_transform_selection(
            original_command,
            normalized_command,
        )

        if transform_instruction is not None:
            return ParsedCommand(
                "transform_selection",
                transform_instruction,
            )

        action = self.get_action(normalized_command)

        if action is not None:
            return ParsedCommand(action)

        fuzzy_match = self.get_fuzzy_action(normalized_command)

        if fuzzy_match is not None:
            fuzzy_action, fuzzy_alias, fuzzy_score = fuzzy_match

            return ParsedCommand(
                "fuzzy_action",
                {
                    "action": fuzzy_action,
                    "alias": fuzzy_alias,
                    "score": fuzzy_score,
                    "original": normalized_command,
                },
            )

        generation_prompt = self.parse_generate_text(
            original_command,
            normalized_command,
        )

        if generation_prompt is not None:
            return ParsedCommand("generate_text", generation_prompt)

        return None

    def normalize_command(self, command: str) -> str:
        """
        Normalize command text for matching.

        This removes duplicate whitespace and makes matching case-insensitive.
        """
        return " ".join(command.strip().lower().split())

    def get_action(self, command: str) -> str | None:
        """
        Return the action for an exact alias match.

        Aliases are language-specific and loaded during initialization.
        """
        for action, aliases in self.command_aliases.items():
            if command in aliases:
                return action

        return None

    def parse_font_size(self, command: str) -> int | None:
        """
        Parse font size commands.

        Returns an integer size if the command contains a valid size.
        """
        prefixes = self.language.FONT_SIZE_PREFIXES

        for prefix in prefixes:
            if command.startswith(prefix + " "):
                value = command.removeprefix(prefix).strip()

                if value.isdigit():
                    size = int(value)

                    if 6 <= size <= 96:
                        return size

                    self.editor_window.show_status_message(
                        self.msg("font_size_out_of_range")
                    )
                    return None

        return None

    def parse_font_family(
        self,
        original_command: str,
        normalized_command: str,
    ) -> str | None:
        """Parse commands that change the font family."""
        prefixes = self.language.FONT_FAMILY_PREFIXES

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
        """Parse commands that insert literal text into the editor."""
        prefixes = self.language.INSERT_TEXT_PREFIXES

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
        """Parse commands that replace the currently selected text."""
        prefixes = self.language.REPLACE_SELECTION_PREFIXES

        text = self.extract_argument_after_prefix(
            original_command,
            normalized_command,
            prefixes,
        )

        if text:
            return text

        return None

    def parse_replace_text(
        self,
        original_command: str,
        normalized_command: str,
    ) -> tuple[str, str] | None:
        """
        Parse search-and-replace commands.

        Examples:
            German:  "ersetze Hund durch Katze"
            English: "replace dog with cat"
        """
        prefixes = self.language.REPLACE_TEXT_PREFIXES

        for prefix in prefixes:
            argument = self.extract_argument_after_prefix(
                original_command,
                normalized_command,
                {prefix},
            )

            if argument is None:
                continue

            separators = "|".join(
                re.escape(separator)
                for separator in self.language.REPLACE_TEXT_SEPARATORS
            )

            parts = re.split(
                rf"\s+({separators})\s+",
                argument,
                maxsplit=1,
                flags=re.IGNORECASE,
            )

            if len(parts) != 3:
                return None

            search_text = parts[0].strip()
            replacement_text = parts[2].strip()

            if search_text and replacement_text:
                return search_text, replacement_text

        return None

    def parse_search_text(
        self,
        original_command: str,
        normalized_command: str,
    ) -> str | None:
        """Parse commands that search for text in the editor."""
        prefixes = self.language.SEARCH_TEXT_PREFIXES

        text = self.extract_argument_after_prefix(
            original_command,
            normalized_command,
            prefixes,
        )

        if text:
            return text

        return None

    def parse_transform_selection(
        self,
        original_command: str,
        normalized_command: str,
    ) -> str | None:
        """
        Parse AI transformation commands for selected text.

        If the command only matches the transformation prefix without an
        additional instruction, the full original command is used as fallback.
        """
        prefixes = self.language.TRANSFORM_SELECTION_PREFIXES

        instruction = self.extract_argument_after_prefix(
            original_command,
            normalized_command,
            prefixes,
        )

        if instruction is None:
            return None

        if instruction.strip():
            return instruction.strip()

        return original_command.strip()

    def parse_generate_text(
        self,
        original_command: str,
        normalized_command: str,
    ) -> str | None:
        """
        Parse AI generation commands.

        The returned prompt is passed to the LLM as the user's generation task.
        """
        prefixes = self.language.GENERATE_TEXT_PREFIXES

        prompt = self.extract_argument_after_prefix(
            original_command,
            normalized_command,
            prefixes,
        )

        if prompt:
            return prompt

        return None

    def extract_argument_after_prefix(
        self,
        original_command: str,
        normalized_command: str,
        prefixes,
    ) -> str | None:
        """
        Extract text after the first matching command prefix.

        Prefixes are sorted from longest to shortest so specific phrases win
        over shorter prefixes that might also match.
        """
        original_stripped = original_command.strip()

        sorted_prefixes = sorted(
            prefixes,
            key=lambda prefix: len(self.normalize_command(prefix)),
            reverse=True,
        )

        for prefix in sorted_prefixes:
            normalized_prefix = self.normalize_command(prefix)

            if normalized_command == normalized_prefix:
                return ""

            if normalized_command.startswith(normalized_prefix + " "):
                return original_stripped[len(prefix):].strip()

        return None

    def get_fuzzy_action(self, command: str) -> tuple[str, str, float] | None:
        """
        Return the best fuzzy alias match if it is confident enough.

        Fuzzy matching is useful for voice commands, where speech recognition
        may produce small mistakes. Short commands use a stricter threshold
        because accidental matches are more likely.
        """
        best_action = None
        best_alias = None
        best_score = 0.0

        for action, aliases in self.command_aliases.items():
            for alias in aliases:
                score = SequenceMatcher(None, command, alias).ratio()

                if score > best_score:
                    best_score = score
                    best_action = action
                    best_alias = alias

        if best_action is None or best_alias is None:
            return None

        if len(command) <= 6:
            threshold = 0.82
        else:
            threshold = 0.78

        if best_score >= threshold:
            return best_action, best_alias, best_score

        return None

    # Command execution -----------------------------------------------------

    def run_command(self, parsed_command: ParsedCommand) -> None:
        """
        Execute a parsed command by calling the matching editor-window method.

        Most actions are delegated to MainWindow because MainWindow owns the
        QTextEdit, dialogues, file handling, and asynchronous workers.
        """
        action = parsed_command.action
        value = parsed_command.value

        if action == "fuzzy_action":
            corrected_action = value["action"]
            corrected_alias = value["alias"]
            original = value["original"]

            self.editor_window.show_status_message(
                self.msg(
                    "command_corrected",
                    original=original,
                    alias=corrected_alias,
                )
            )

            self.run_command(ParsedCommand(corrected_action))
            return

        if action == "bold":
            self.editor_window.toggle_bold()
            self.editor_window.show_status_message(self.msg("executed_bold"))

        elif action == "italic":
            self.editor_window.toggle_italic()
            self.editor_window.show_status_message(self.msg("executed_italic"))

        elif action == "delete_selection":
            self.delete_selection()
            self.editor_window.show_status_message(
                self.msg("executed_delete_selection")
            )

        elif action == "select_all":
            self.editor.selectAll()
            self.editor_window.show_status_message(
                self.msg("executed_select_all")
            )

        elif action == "new_line":
            self.insert_new_line()
            self.editor_window.show_status_message(
                self.msg("executed_new_line")
            )

        elif action == "undo":
            self.editor.undo()
            self.editor_window.show_status_message(self.msg("executed_undo"))

        elif action == "redo":
            self.editor.redo()
            self.editor_window.show_status_message(self.msg("executed_redo"))

        elif action == "cut":
            self.editor.cut()
            self.editor_window.show_status_message(self.msg("executed_cut"))

        elif action == "copy":
            self.editor.copy()
            self.editor_window.show_status_message(self.msg("executed_copy"))

        elif action == "paste":
            self.editor.paste()
            self.editor_window.show_status_message(self.msg("executed_paste"))

        elif action == "save":
            if self.editor_window.save_file():
                self.editor_window.show_status_message(self.msg("executed_save"))
            else:
                self.editor_window.show_status_message(self.msg("save_cancelled"))

        elif action == "open":
            if self.editor_window.open_file():
                self.editor_window.show_status_message(self.msg("executed_open"))
            else:
                self.editor_window.show_status_message(self.msg("open_cancelled"))

        elif action == "new_file":
            if self.editor_window.new_file():
                self.editor_window.show_status_message(
                    self.msg("executed_new_file")
                )
            else:
                self.editor_window.show_status_message(
                    self.msg("new_file_cancelled")
                )

        elif action == "export_pdf":
            if self.editor_window.export_pdf():
                self.editor_window.show_status_message(
                    self.msg("executed_export_pdf")
                )
            else:
                self.editor_window.show_status_message(
                    self.msg("export_pdf_cancelled")
                )

        elif action == "print_document":
            if self.editor_window.print_document():
                self.editor_window.show_status_message(self.msg("executed_print"))
            else:
                self.editor_window.show_status_message(self.msg("print_cancelled"))

        elif action == "heading_1":
            self.editor_window.set_heading(1)
            self.editor_window.show_status_message(
                self.msg("executed_heading_1")
            )

        elif action == "heading_2":
            self.editor_window.set_heading(2)
            self.editor_window.show_status_message(
                self.msg("executed_heading_2")
            )

        elif action == "normal_text":
            self.editor_window.set_normal_text()
            self.editor_window.show_status_message(
                self.msg("executed_normal_text")
            )

        elif action == "align_left":
            self.editor_window.align_left()
            self.editor_window.show_status_message(
                self.msg("executed_align_left")
            )

        elif action == "align_center":
            self.editor_window.align_center()
            self.editor_window.show_status_message(
                self.msg("executed_align_center")
            )

        elif action == "align_right":
            self.editor_window.align_right()
            self.editor_window.show_status_message(
                self.msg("executed_align_right")
            )

        elif action == "bullet_list":
            self.editor_window.toggle_bullet_list()
            self.editor_window.show_status_message(
                self.msg("executed_bullet_list")
            )

        elif action == "numbered_list":
            self.editor_window.toggle_numbered_list()
            self.editor_window.show_status_message(
                self.msg("executed_numbered_list")
            )

        elif action == "remove_list":
            self.editor_window.remove_list_format()
            self.editor_window.show_status_message(
                self.msg("executed_remove_list")
            )

        elif action == "indent":
            self.editor_window.indent_text()
            self.editor_window.show_status_message(self.msg("executed_indent"))

        elif action == "outdent":
            self.editor_window.outdent_text()
            self.editor_window.show_status_message(self.msg("executed_outdent"))

        elif action == "font_size":
            self.editor_window.set_font_size(value)
            self.editor_window.show_status_message(
                self.msg("executed_font_size", value=value)
            )

        elif action == "font_family":
            if self.editor_window.set_font_family(value):
                self.editor_window.show_status_message(
                    self.msg("executed_font_family", value=value)
                )

        elif action == "insert_text":
            self.editor_window.insert_text(value)
            self.editor_window.show_status_message(
                self.msg("executed_insert_text")
            )

        elif action == "search_text":
            self.editor_window.find_text(value)

        elif action == "replace_selection":
            self.editor_window.replace_selection(value)

        elif action == "replace_text":
            search_text, replacement_text = value
            self.editor_window.replace_next_text(
                search_text,
                replacement_text,
            )

        elif action == "transform_selection":
            self.editor_window.transform_selection_async(
                self.llm_client,
                value,
            )

        elif action == "generate_text":
            self.editor_window.generate_text_async(self.llm_client, value)

        elif action == "continue_text":
            self.editor_window.continue_text_async(self.llm_client)

        elif action == "ai_status":
            self.editor_window.show_ai_status()

        elif action == "ollama_test":
            self.editor_window.show_ollama_test()

        elif action == "open_settings_dialog":
            self.editor_window.open_settings_dialog()

        elif action == "about":
            self.editor_window.show_about_dialog()
            self.editor_window.show_status_message(self.msg("executed_about"))

        elif action == "diagnostics":
            self.editor_window.show_diagnostics_dialog()
            self.editor_window.show_status_message(
                self.msg("executed_diagnostics")
            )

        elif action == "document_info":
            self.editor_window.show_document_info_dialog()
            self.editor_window.show_status_message(
                self.msg("executed_document_info")
            )

        else:
            self.show_unknown_command(action)

    # Small editor helpers --------------------------------------------------

    def delete_selection(self) -> None:
        """Remove the current editor selection if there is one."""
        cursor = self.editor.textCursor()

        if cursor.hasSelection():
            cursor.removeSelectedText()

    def insert_new_line(self) -> None:
        """Insert a single newline at the current cursor position."""
        cursor = self.editor.textCursor()
        cursor.insertText("\n")

    # Messages --------------------------------------------------------------

    def msg(self, key: str, **kwargs) -> str:
        """Return a localized command-router message."""
        return command_message(key, **kwargs)

    def show_unknown_command(self, command: str) -> None:
        """Display a localized status message for an unknown command."""
        self.editor_window.show_status_message(
            self.msg("unknown_command", command=command)
        )
