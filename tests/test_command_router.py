# SPDX-License-Identifier: Apache-2.0

"""
Tests for SayScript's command parsing logic.

These tests intentionally avoid the real GUI, Ollama, and microphone input.
They verify that spoken or typed commands are mapped to the correct internal
CommandRouter actions.

Only parsing is tested here. Command execution is deliberately not tested
because execution depends on the real editor window and Qt widgets.
"""

import app.command_router as command_router_module
import app.locales.de as de
import app.locales.en as en

from app.command_router import CommandRouter


class DummyEditor:
    """Minimal editor placeholder for CommandRouter construction."""

    pass


class DummyEditorWindow:
    """
    Minimal main-window placeholder for CommandRouter construction.

    CommandRouter expects an object with an ``editor`` attribute. The parsing
    tests do not call methods that require a real QTextEdit.
    """

    def __init__(self):
        self.editor = DummyEditor()


class DummyLlmClient:
    """
    Lightweight LLM client placeholder.

    CommandRouter creates an LlmClient during initialization. The parser tests
    do not need a real client, so this dummy keeps the tests independent from
    settings files, Ollama, and network state.
    """

    pass


def create_router(monkeypatch, language_module):
    """
    Create a CommandRouter with a controlled language module.

    The language module is monkeypatched so each test can explicitly choose
    German or English aliases without changing persistent application settings.
    """
    monkeypatch.setattr(
        command_router_module,
        "get_command_language_module",
        lambda: language_module,
    )

    monkeypatch.setattr(
        command_router_module,
        "LlmClient",
        DummyLlmClient,
    )

    return CommandRouter(DummyEditorWindow())


def parse(router, command: str):
    """Normalize and parse a command through CommandRouter."""
    normalized_command = router.normalize_command(command)
    return router.parse_command(command, normalized_command)


def test_german_bold_command(monkeypatch):
    router = create_router(monkeypatch, de)

    parsed_command = parse(router, "fett")

    assert parsed_command is not None
    assert parsed_command.action == "bold"


def test_german_generate_text_command(monkeypatch):
    router = create_router(monkeypatch, de)

    parsed_command = parse(router, "generiere einen text über hunde")

    assert parsed_command is not None
    assert parsed_command.action == "generate_text"
    assert parsed_command.value == "einen text über hunde"


def test_german_export_pdf_command(monkeypatch):
    router = create_router(monkeypatch, de)

    parsed_command = parse(router, "exportiere als pdf")

    assert parsed_command is not None
    assert parsed_command.action == "export_pdf"


def test_german_diagnostics_command(monkeypatch):
    router = create_router(monkeypatch, de)

    parsed_command = parse(router, "diagnose")

    assert parsed_command is not None
    assert parsed_command.action == "diagnostics"


def test_german_print_command(monkeypatch):
    router = create_router(monkeypatch, de)

    parsed_command = parse(router, "drucken")

    assert parsed_command is not None
    assert parsed_command.action == "print_document"


def test_german_about_command(monkeypatch):
    router = create_router(monkeypatch, de)

    parsed_command = parse(router, "über sayscript")

    assert parsed_command is not None
    assert parsed_command.action == "about"


def test_german_search_command(monkeypatch):
    router = create_router(monkeypatch, de)

    parsed_command = parse(router, "suche nach hund")

    assert parsed_command is not None
    assert parsed_command.action == "search_text"
    assert parsed_command.value == "hund"


def test_german_replace_text_command(monkeypatch):
    router = create_router(monkeypatch, de)

    parsed_command = parse(router, "ersetze hund durch katze")

    assert parsed_command is not None
    assert parsed_command.action == "replace_text"
    assert parsed_command.value == ("hund", "katze")


def test_german_document_info_command(monkeypatch):
    router = create_router(monkeypatch, de)

    parsed_command = parse(router, "wortzähler")

    assert parsed_command is not None
    assert parsed_command.action == "document_info"


def test_english_bold_command(monkeypatch):
    router = create_router(monkeypatch, en)

    parsed_command = parse(router, "bold")

    assert parsed_command is not None
    assert parsed_command.action == "bold"


def test_english_generate_text_command(monkeypatch):
    router = create_router(monkeypatch, en)

    parsed_command = parse(router, "generate a text about dogs")

    assert parsed_command is not None
    assert parsed_command.action == "generate_text"
    assert parsed_command.value == "a text about dogs"


def test_english_export_pdf_command(monkeypatch):
    router = create_router(monkeypatch, en)

    parsed_command = parse(router, "export as pdf")

    assert parsed_command is not None
    assert parsed_command.action == "export_pdf"


def test_english_diagnostics_command(monkeypatch):
    router = create_router(monkeypatch, en)

    parsed_command = parse(router, "diagnostics")

    assert parsed_command is not None
    assert parsed_command.action == "diagnostics"


def test_english_print_command(monkeypatch):
    router = create_router(monkeypatch, en)

    parsed_command = parse(router, "print")

    assert parsed_command is not None
    assert parsed_command.action == "print_document"


def test_english_about_command(monkeypatch):
    router = create_router(monkeypatch, en)

    parsed_command = parse(router, "about sayscript")

    assert parsed_command is not None
    assert parsed_command.action == "about"


def test_english_search_command(monkeypatch):
    router = create_router(monkeypatch, en)

    parsed_command = parse(router, "search for dog")

    assert parsed_command is not None
    assert parsed_command.action == "search_text"
    assert parsed_command.value == "dog"


def test_english_replace_text_command(monkeypatch):
    router = create_router(monkeypatch, en)

    parsed_command = parse(router, "replace dog with cat")

    assert parsed_command is not None
    assert parsed_command.action == "replace_text"
    assert parsed_command.value == ("dog", "cat")


def test_english_transform_selection_is_not_bold(monkeypatch):
    router = create_router(monkeypatch, en)

    parsed_command = parse(router, "make selection shorter")

    assert parsed_command is not None
    assert parsed_command.action == "transform_selection"
    assert parsed_command.value == "make selection shorter"


def test_english_document_info_command(monkeypatch):
    router = create_router(monkeypatch, en)

    parsed_command = parse(router, "word count")

    assert parsed_command is not None
    assert parsed_command.action == "document_info"
