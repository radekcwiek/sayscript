from app.settings import load_settings


TRANSLATIONS = {
    "de": {
        "window_title_default": "SayScript - Editor",

        "menu_file": "Datei",

        "action_new": "Neu",
        "action_open": "Öffnen",
        "action_save": "Speichern",
        "action_save_as": "Speichern unter",
        "action_settings": "Einstellungen",
        "action_exit": "Beenden",

        "action_print": "Drucken",
        "dialog_print_title": "Drucken",
        "status_printed": "Dokument gedruckt",
        "error_print": "Dokument konnte nicht gedruckt werden:\n{error}",

        "button_dictation_start": "Diktieren",
        "button_dictation_stop": "Diktieren stoppen",
        "button_voice_command_start": "Sprachbefehl",
        "button_voice_command_stop": "Sprachbefehl stoppen",

        "tooltip_dictation": (
            "Diktat starten oder stoppen. "
            "Transkribierter Text wird in den Editor eingefügt."
        ),
        "tooltip_voice_command": (
            "Sprachbefehl starten oder stoppen. "
            "Transkribierter Text wird als Befehl ausgeführt."
        ),

        "speech_result_empty": "Erkannte Sprache: -",
        "speech_result_text": "Erkannte Sprache: {text}",

        "command_label": "Befehl:",
        "command_placeholder": "z. B. fett, suche nach ..., generiere ...",

        "status_ready": "Bereit",
        "status_new_file_created": "Neue Datei erstellt",
        "status_file_opened": "Datei geöffnet",
        "status_file_saved": "Datei gespeichert",

        "dialog_open_file_title": "Datei öffnen",
        "dialog_save_file_title": "Datei speichern",
        "file_filter_open": "HTML-Dateien (*.html);;Markdown-Dateien (*.md *.markdown);;Textdateien (*.txt);;Alle Dateien (*.*)",
        "file_filter_save": "HTML-Dateien (*.html);;Markdown-Dateien (*.md *.markdown);;Textdateien (*.txt)",

        "error_title": "Fehler",
        "error_file_open": "Datei konnte nicht geöffnet werden:\n{error}",
        "error_file_save": "Datei konnte nicht gespeichert werden:\n{error}",

        "dialog_save_changes_title": "Änderungen speichern?",
        "dialog_save_changes_text": "Das Dokument wurde geändert. Möchtest du die Änderungen speichern?",

        "dialog_ai_busy_title": "KI arbeitet noch",
        "dialog_ai_busy_text": "Bitte warte, bis die KI-Aktion abgeschlossen ist.",
        "dialog_speech_busy_title": "Spracherkennung arbeitet noch",
        "dialog_speech_busy_text": "Bitte warte, bis die Transkription abgeschlossen ist.",

        "dialog_dictation_title": "Diktieren",
        "dialog_voice_command_title": "Sprachbefehl",
        "dialog_speech_title": "Spracherkennung",

        "dialog_export_pdf_title": "Als PDF exportieren",
        "file_filter_pdf": "PDF-Dateien (*.pdf)",
        "status_pdf_exported": "PDF exportiert",
        "error_pdf_export": "PDF konnte nicht exportiert werden:\n{error}",
        "action_export_pdf": "Als PDF exportieren",

        "error_recording_start": "Die Aufnahme konnte nicht gestartet werden:\n{error}",
        "error_dictation_process": "Das Diktat konnte nicht verarbeitet werden:\n{error}",
        "error_voice_command_process": "Der Sprachbefehl konnte nicht verarbeitet werden:\n{error}",

        "status_dictation_started": "Diktat gestartet",
        "status_dictation_stopped": "Diktat gestoppt",
        "status_dictation_recording": "Diktataufnahme läuft ...",
        "status_no_recording": "Keine Aufnahme vorhanden",
        "status_transcribing_dictation": "Transkribiere Diktat ...",
        "status_dictation_inserted": "Diktat eingefügt",

        "status_voice_command_started": "Sprachbefehl gestartet",
        "status_voice_command_stopped": "Sprachbefehl gestoppt",
        "status_voice_command_recording": "Sprachbefehl-Aufnahme läuft ...",
        "status_transcribing_voice_command": "Transkribiere Sprachbefehl ...",
        "status_no_voice_command": "Kein Sprachbefehl erkannt",
        "status_voice_command_recognized": "Sprachbefehl erkannt: {command}",
        "status_voice_command_corrected": "Sprachbefehl erkannt: {original} → {command}",

        "status_speech_already_running": "Spracherkennung arbeitet bereits",
        "status_settings_saved": "Einstellungen gespeichert",
        "status_font_not_found": "Schriftart nicht gefunden: {family}",

        "status_no_search_text": "Kein Suchtext angegeben",
        "status_found_text": "Gefunden: {text}",
        "status_found_text_from_start": "Gefunden ab Dokumentanfang: {text}",
        "status_text_not_found": "Nicht gefunden: {text}",

        "status_no_selection_to_replace": "Keine Auswahl zum Ersetzen vorhanden",
        "status_selection_replaced": "Auswahl ersetzt",
        "status_replaced_text": "Ersetzt: {search_text} → {replacement_text}",

        "status_ai_already_working": "Die KI arbeitet bereits",
        "status_ai_generating": "KI generiert Text ...",
        "status_ai_text_inserted": "KI-Text eingefügt",
        "status_ai_continuation_inserted": "KI-Fortsetzung eingefügt",
        "status_ai_selection_replaced": "KI-Auswahl ersetzt",
        "status_unknown_ai_mode": "Unbekannter KI-Modus: {mode}",
        "status_ai_error": "KI-Fehler",
        "dialog_ai_error_title": "KI-Fehler",

        "status_no_selection_for_ai": "Bitte zuerst Text markieren",
        "status_ai_transforming_selection": "KI bearbeitet Auswahl ...",
        "status_ai_continuing": "KI schreibt weiter ...",
        "context_missing": "Kein Kontext vor dem Cursor vorhanden",
        "dialog_ai_status_title": "KI-Status",
        "dialog_ollama_test_title": "Ollama-Test",

        "ai_status_settings_path": "Einstellungsdatei",
        "ai_status_ollama": "Ollama",
        "ai_status_base_url": "Adresse",
        "ai_status_model": "Modell",
        "ai_status_timeout": "Timeout",
        "ai_status_fake_mode": "Fake-Modus",
        "ai_status_generation": "Generierung",
        "ai_status_transform": "Transformation",
        "ai_status_continue": "Fortsetzung",
        "ai_status_temperature": "Temperature",
        "ai_status_num_predict": "Max. Antwortlänge",
        "ai_status_speech": "Spracherkennung",
        "ai_status_speech_model": "Whisper-Modell",
        "ai_status_sample_rate": "Sample Rate",
        "ai_status_device": "Device",
        "ai_status_compute_type": "Compute Type",
        "ai_status_beam_size": "Beam Size",
        "ai_status_interface_language": "Bedienungssprache",
        "ai_status_text_language": "Textsprache",
        "ai_status_yes": "Ja",
        "ai_status_no": "Nein",

        "ollama_test_models": "Gefundene Modelle",
        "ollama_test_no_models": "(keine Modelle gefunden)",
        "ollama_test_success_status": "Ollama ist erreichbar.",
        "ollama_test_failure_status": "Ollama ist nicht vollständig verfügbar.",
        "unit_tokens": "Tokens",
        "file_type_html": "HTML-Dateien (*.html)",
        "file_type_text": "Textdateien (*.txt)",
        "file_type_all": "Alle Dateien (*.*)",

        "status_open_cancelled": "Öffnen abgebrochen",
        "status_save_cancelled": "Speichern abgebrochen",
        "status_new_file_cancelled": "Neue Datei abgebrochen",
    },

    "en": {
        "window_title_default": "SayScript - Editor",

        "menu_file": "File",

        "action_new": "New",
        "action_open": "Open",
        "action_save": "Save",
        "action_save_as": "Save As",
        "action_settings": "Settings",
        "action_exit": "Exit",
        "action_print": "Print",
        "dialog_print_title": "Print",
        "status_printed": "Document printed",
        "error_print": "The document could not be printed:\n{error}",

        "button_dictation_start": "Dictate",
        "button_dictation_stop": "Stop dictation",
        "button_voice_command_start": "Voice command",
        "button_voice_command_stop": "Stop voice command",

        "tooltip_dictation": (
            "Start or stop dictation. "
            "Transcribed text is inserted into the editor."
        ),
        "tooltip_voice_command": (
            "Start or stop a voice command. "
            "Transcribed text is executed as a command."
        ),

        "speech_result_empty": "Recognized speech: -",
        "speech_result_text": "Recognized speech: {text}",

        "command_label": "Command:",
        "command_placeholder": "e.g. bold, search for ..., generate ...",

        "status_ready": "Ready",
        "status_new_file_created": "New file created",
        "status_file_opened": "File opened",
        "status_file_saved": "File saved",

        "dialog_open_file_title": "Open file",
        "dialog_save_file_title": "Save file",
        "file_filter_open": "HTML files (*.html);;Markdown files (*.md *.markdown);;Text files (*.txt);;All files (*.*)",
        "file_filter_save": "HTML files (*.html);;Markdown files (*.md *.markdown);;Text files (*.txt)",

        "error_title": "Error",
        "error_file_open": "The file could not be opened:\n{error}",
        "error_file_save": "The file could not be saved:\n{error}",

        "dialog_save_changes_title": "Save changes?",
        "dialog_save_changes_text": "The document has been modified. Do you want to save your changes?",

        "dialog_ai_busy_title": "AI is still working",
        "dialog_ai_busy_text": "Please wait until the AI action has finished.",
        "dialog_speech_busy_title": "Speech recognition is still working",
        "dialog_speech_busy_text": "Please wait until transcription has finished.",

        "dialog_dictation_title": "Dictation",
        "dialog_voice_command_title": "Voice command",
        "dialog_speech_title": "Speech recognition",

        "dialog_export_pdf_title": "Export as PDF",
        "file_filter_pdf": "PDF files (*.pdf)",
        "status_pdf_exported": "PDF exported",
        "error_pdf_export": "The PDF could not be exported:\n{error}",
        "action_export_pdf": "Export as PDF",

        "error_recording_start": "The recording could not be started:\n{error}",
        "error_dictation_process": "The dictation could not be processed:\n{error}",
        "error_voice_command_process": "The voice command could not be processed:\n{error}",

        "status_dictation_started": "Dictation started",
        "status_dictation_stopped": "Dictation stopped",
        "status_dictation_recording": "Dictation recording is running ...",
        "status_no_recording": "No recording available",
        "status_transcribing_dictation": "Transcribing dictation ...",
        "status_dictation_inserted": "Dictation inserted",

        "status_voice_command_started": "Voice command started",
        "status_voice_command_stopped": "Voice command stopped",
        "status_voice_command_recording": "Voice command recording is running ...",
        "status_transcribing_voice_command": "Transcribing voice command ...",
        "status_no_voice_command": "No voice command recognized",
        "status_voice_command_recognized": "Voice command recognized: {command}",
        "status_voice_command_corrected": "Voice command recognized: {original} → {command}",

        "status_speech_already_running": "Speech recognition is already running",
        "status_settings_saved": "Settings saved",
        "status_font_not_found": "Font not found: {family}",

        "status_no_search_text": "No search text specified",
        "status_found_text": "Found: {text}",
        "status_found_text_from_start": "Found from beginning of document: {text}",
        "status_text_not_found": "Not found: {text}",

        "status_no_selection_to_replace": "No selection available to replace",
        "status_selection_replaced": "Selection replaced",
        "status_replaced_text": "Replaced: {search_text} → {replacement_text}",

        "status_ai_already_working": "The AI is already working",
        "status_ai_generating": "AI is generating text ...",
        "status_ai_text_inserted": "AI text inserted",
        "status_ai_continuation_inserted": "AI continuation inserted",
        "status_ai_selection_replaced": "AI selection replaced",
        "status_unknown_ai_mode": "Unknown AI mode: {mode}",
        "status_ai_error": "AI error",
        "dialog_ai_error_title": "AI error",

        "status_no_selection_for_ai": "Please select text first",
        "status_ai_transforming_selection": "AI is editing the selection ...",
        "status_ai_continuing": "AI is continuing text ...",
        "context_missing": "No context before cursor found",
        "dialog_ai_status_title": "AI status",
        "dialog_ollama_test_title": "Ollama test",

        "ai_status_settings_path": "Settings file",
        "ai_status_ollama": "Ollama",
        "ai_status_base_url": "Address",
        "ai_status_model": "Model",
        "ai_status_timeout": "Timeout",
        "ai_status_fake_mode": "Fake mode",
        "ai_status_generation": "Generation",
        "ai_status_transform": "Transformation",
        "ai_status_continue": "Continuation",
        "ai_status_temperature": "Temperature",
        "ai_status_num_predict": "Max. response length",
        "ai_status_speech": "Speech recognition",
        "ai_status_speech_model": "Whisper model",
        "ai_status_sample_rate": "Sample rate",
        "ai_status_device": "Device",
        "ai_status_compute_type": "Compute type",
        "ai_status_beam_size": "Beam size",
        "ai_status_interface_language": "Interface language",
        "ai_status_text_language": "Text language",
        "ai_status_yes": "Yes",
        "ai_status_no": "No",

        "ollama_test_models": "Found models",
        "ollama_test_no_models": "(no models found)",
        "ollama_test_success_status": "Ollama is reachable.",
        "ollama_test_failure_status": "Ollama is not fully available.",
        "unit_tokens": "tokens",
        "file_type_html": "HTML files (*.html)",
        "file_type_text": "Text files (*.txt)",
        "file_type_all": "All files (*.*)",

        "status_open_cancelled": "Open cancelled",
        "status_save_cancelled": "Save cancelled",
        "status_new_file_cancelled": "New file cancelled",
    },
}


def get_language() -> str:
    settings = load_settings()
    language = settings.get("interface_language", "de")

    if language not in TRANSLATIONS:
        return "de"

    return language


def tr(key: str, **kwargs) -> str:
    language = get_language()
    text = TRANSLATIONS.get(language, TRANSLATIONS["de"]).get(
        key,
        TRANSLATIONS["de"].get(key, key),
    )

    if kwargs:
        return text.format(**kwargs)

    return text


def get_command_language_module():
    language = get_language()

    if language == "en":
        from app.locales import en
        return en

    from app.locales import de
    return de


def command_message(key: str, **kwargs) -> str:
    language_module = get_command_language_module()
    messages = getattr(language_module, "MESSAGES", {})

    text = messages.get(key, key)

    if kwargs:
        return text.format(**kwargs)

    return text


def speech_language() -> str:
    language_module = get_command_language_module()
    return getattr(language_module, "SPEECH_LANGUAGE", "de")


def speech_initial_prompt() -> str:
    language_module = get_command_language_module()
    return getattr(
        language_module,
        "SPEECH_INITIAL_PROMPT",
        (
            "Dies ist ein diktierter Text für eine Textverarbeitung. "
            "Achte auf korrekte Rechtschreibung und sinnvolle Wörter."
        ),
    )


def speech_message(key: str, **kwargs) -> str:
    language_module = get_command_language_module()
    messages = getattr(language_module, "SPEECH_MESSAGES", {})

    text = messages.get(key, key)

    if kwargs:
        return text.format(**kwargs)

    return text



def llm_text_generation_language_name(language_code: str) -> str:
    language_module = get_command_language_module()
    names = getattr(
        language_module,
        "LLM_TEXT_GENERATION_LANGUAGE_NAMES",
        {
            "de": "Deutsch",
            "en": "Englisch",
        },
    )

    return names.get(language_code, names.get("de", "Deutsch"))


def llm_prompt(key: str, **kwargs) -> str:
    language_module = get_command_language_module()
    prompts = getattr(language_module, "LLM_PROMPTS", {})

    text = prompts.get(key, key)

    if kwargs:
        return text.format(**kwargs)

    return text


def llm_message(key: str, **kwargs) -> str:
    language_module = get_command_language_module()
    messages = getattr(language_module, "LLM_MESSAGES", {})

    text = messages.get(key, key)

    if kwargs:
        return text.format(**kwargs)

    return text


def settings_text(key: str, **kwargs) -> str:
    language_module = get_command_language_module()
    texts = getattr(language_module, "SETTINGS_DIALOG_TEXTS", {})

    text = texts.get(key, key)

    if kwargs:
        return text.format(**kwargs)

    return text


def voice_command_corrections() -> dict:
    language_module = get_command_language_module()
    return getattr(language_module, "VOICE_COMMAND_CORRECTIONS", {})


def llm_worker_message(key: str, **kwargs) -> str:
    language_module = get_command_language_module()
    messages = getattr(language_module, "LLM_WORKER_MESSAGES", {})

    text = messages.get(key, key)

    if kwargs:
        return text.format(**kwargs)

    return text

