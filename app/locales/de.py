COMMAND_ALIASES = {
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
    "ai_status": {
        "ki status",
        "ki-status",
        "ai status",
        "modell status",
        "ollama status",
        "zeige ki status",
        "systemstatus",
        "system status",
        "status",
        "spracherkennung status",
        "whisper status",
    },
    "ollama_test": {
        "ollama test",
        "ki test",
        "ai test",
        "modell test",
        "teste ollama",
        "teste ki",
    },
    "open_settings_dialog": {
        "einstellungen",
        "einstellungen öffnen",
        "settings",
        "settings öffnen",
        "konfiguration",
        "konfiguration öffnen",
    },
}


FONT_SIZE_PREFIXES = {
    "schriftgröße",
    "schriftgroesse",
    "schrift größe",
    "schrift groesse",
    "größe",
    "groesse",
}

FONT_FAMILY_PREFIXES = {
    "schriftart",
    "schrift",
    "font",
    "font family",
}

INSERT_TEXT_PREFIXES = {
    "füge ein",
    "fuege ein",
    "einfügen",
    "einfuegen",
    "text einfügen",
    "text einfuegen",
}

SEARCH_TEXT_PREFIXES = {
    "suche nach",
    "suche",
    "finde",
    "find",
    "search",
    "search for",
}

REPLACE_SELECTION_PREFIXES = {
    "ersetze auswahl durch",
    "ersetze markierung durch",
    "ersetze selektion durch",
    "ersetze durch",
    "auswahl ersetzen durch",
    "markierung ersetzen durch",
}

REPLACE_TEXT_PREFIXES = {
    "ersetze",
    "ersetze nächstes",
    "ersetze naechstes",
}

REPLACE_TEXT_SEPARATORS = {
    "durch",
}

GENERATE_TEXT_PREFIXES = {
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

TRANSFORM_SELECTION_PREFIXES = {
    "formuliere auswahl um",
    "formuliere markierung um",
    "formuliere um",
    "ändere auswahl",
    "aendere auswahl",
    "bearbeite auswahl",
    "verbessere auswahl",
    "korrigiere auswahl",
    "mache auswahl",
    "überarbeite auswahl",
    "ueberarbeite auswahl",
    "überarbeite markierung",
    "ueberarbeite markierung",
    "bearbeite markierung",
}

MESSAGES = {
    "unknown_command": "Unbekannter Befehl: {command}",
    "command_corrected": "Befehl korrigiert: {original} → {alias}",

    "executed_bold": "Befehl ausgeführt: fett",
    "executed_italic": "Befehl ausgeführt: kursiv",
    "executed_delete_selection": "Befehl ausgeführt: Auswahl gelöscht",
    "executed_select_all": "Befehl ausgeführt: alles markiert",
    "executed_new_line": "Befehl ausgeführt: neue Zeile",
    "executed_undo": "Befehl ausgeführt: rückgängig",
    "executed_redo": "Befehl ausgeführt: wiederholen",
    "executed_cut": "Befehl ausgeführt: ausschneiden",
    "executed_copy": "Befehl ausgeführt: kopieren",
    "executed_paste": "Befehl ausgeführt: einfügen",

    "executed_save": "Befehl ausgeführt: speichern",
    "save_cancelled": "Speichern abgebrochen",
    "executed_open": "Befehl ausgeführt: öffnen",
    "open_cancelled": "Öffnen abgebrochen",
    "executed_new_file": "Befehl ausgeführt: neue Datei",
    "new_file_cancelled": "Neue Datei abgebrochen",

    "executed_heading_1": "Befehl ausgeführt: Überschrift 1",
    "executed_heading_2": "Befehl ausgeführt: Überschrift 2",
    "executed_normal_text": "Befehl ausgeführt: normaler Text",
    "executed_align_left": "Befehl ausgeführt: linksbündig",
    "executed_align_center": "Befehl ausgeführt: zentriert",
    "executed_align_right": "Befehl ausgeführt: rechtsbündig",

    "executed_bullet_list": "Befehl ausgeführt: Liste",
    "executed_numbered_list": "Befehl ausgeführt: nummerierte Liste",
    "executed_remove_list": "Befehl ausgeführt: Liste entfernt",
    "executed_indent": "Befehl ausgeführt: einrücken",
    "executed_outdent": "Befehl ausgeführt: ausrücken",

    "executed_font_size": "Befehl ausgeführt: Schriftgröße {value}",
    "executed_font_family": "Befehl ausgeführt: Schriftart {value}",
    "executed_insert_text": "Befehl ausgeführt: Text eingefügt",

    "font_size_out_of_range": "Schriftgröße muss zwischen 6 und 96 liegen",
}

SPEECH_LANGUAGE = "de"

SPEECH_INITIAL_PROMPT = (
    "Dies ist ein deutscher diktierter Text für eine Textverarbeitung. "
    "Achte auf korrekte deutsche Rechtschreibung, Umlaute und sinnvolle Wörter."
)

SPEECH_MESSAGES = {
    "no_text_recognized": "Kein Text erkannt.",
    "transcription_error": "Transkriptionsfehler: {error}",
}

LLM_TEXT_GENERATION_LANGUAGE_NAMES = {
    "de": "Deutsch",
    "en": "Englisch",
}

LLM_PROMPTS = {
    "generation": (
        "Du bist ein Schreibassistent in einer Textverarbeitung.\n\n"
        "WICHTIG:\n"
        "- Gib ausschließlich den fertigen Text zurück.\n"
        "- Keine Analyse.\n"
        "- Keine Gedanken.\n"
        "- Keine Erklärung.\n"
        "- Keine Einleitung.\n"
        "- Schreibe nicht, was du tun wirst.\n"
        "- Gib nur den Text aus, der direkt in ein Dokument eingefügt werden soll.\n"
        "- Schreibe den Text in dieser Sprache: {output_language}.\n\n"
        "Aufgabe: {user_prompt}"
    ),
    "transform": (
        "Du bist ein hilfreicher Schreibassistent innerhalb einer lokalen "
        "Textverarbeitung namens Dictator.\n\n"
        "Bearbeite den folgenden Text gemäß der Anweisung. "
        "Gib ausschließlich den überarbeiteten Text zurück. "
        "Keine Kommentare, keine Erklärungen, keine Markdown-Umrahmung. "
        "Schreibe den überarbeiteten Text in dieser Sprache: {output_language}.\n\n"
        "Anweisung: {instruction}\n\n"
        "Text:\n{selected_text}"
    ),
    "continue": (
        "Du bist ein hilfreicher Schreibassistent innerhalb einer lokalen "
        "Textverarbeitung namens Dictator.\n\n"
        "Schreibe den folgenden Text sinnvoll weiter. "
        "Gib nur die Fortsetzung zurück, nicht den bisherigen Text. "
        "Keine Kommentare, keine Erklärungen, keine Markdown-Umrahmung. "
        "Schreibe die Fortsetzung in dieser Sprache: {output_language}.\n\n"
        "Bisheriger Text:\n{context_text}"
    ),
}

LLM_MESSAGES = {
    "fake_generation": (
        "[KI-Generierung Platzhalter]\n\n"
        "Aufgabe: {prompt}\n\n"
        "Hier wird später die Antwort von Qwen eingefügt."
    ),
    "fake_transform": (
        "[KI-Transformation Platzhalter]\n\n"
        "Anweisung: {instruction}\n\n"
        "Ausgangstext:\n{selected_text}"
    ),
    "fake_continue": (
        "[KI-Fortsetzung Platzhalter]\n\n"
        "Kontext:\n{context_text}\n\n"
        "Hier wird später die Fortsetzung von Qwen eingefügt."
    ),

    "ollama_connection_error": (
        "[Fehler]\n\n"
        "Ollama ist nicht erreichbar. Läuft Ollama auf diesem Rechner?"
    ),
    "ollama_timeout_error": (
        "[Fehler]\n\n"
        "Die KI-Anfrage hat zu lange gedauert."
    ),
    "ollama_request_error": (
        "[Fehler]\n\n"
        "Die KI-Anfrage ist fehlgeschlagen:\n{error}"
    ),
    "ollama_empty_response": (
        "[Fehler]\n\n"
        "Das Modell hat keinen sichtbaren Text zurückgegeben.\n\n"
        "Thinking-Feld:\n{thinking_text}\n\n"
        "Ollama-Antwort:\n{data}"
    ),

    "ollama_status_connection_error": "Ollama ist nicht erreichbar.",
    "ollama_status_timeout_error": "Die Ollama-Anfrage hat zu lange gedauert.",
    "ollama_status_request_error": "Ollama-Statusabfrage fehlgeschlagen: {error}",
    "ollama_status_model_found": "Ollama ist erreichbar. Modell gefunden: {model_name}",
    "ollama_status_model_not_found": "Ollama ist erreichbar, aber Modell nicht gefunden: {model_name}",
}

SETTINGS_DIALOG_TEXTS = {
    "title": "Einstellungen",

    "group_connection": "Verbindung",
    "group_generation": "Generierung",
    "group_transform": "Transformation",
    "group_continue": "Fortsetzung",
    "group_speech": "Spracherkennung",

    "label_ollama_base_url": "Ollama-Adresse:",
    "label_model_name": "Modellname:",
    "label_timeout": "Timeout:",
    "label_fake_mode": "Fake-Modus:",
    "label_show_command_input": "Befehlszeile anzeigen:",
    "label_interface_language": "Bedienungssprache:",
    "label_text_generation_language": "Textsprache:",

    "label_temperature": "Temperature:",
    "label_max_response_length": "Max. Antwortlänge:",

    "label_whisper_model": "Whisper-Modell:",
    "label_sample_rate": "Sample Rate:",
    "label_device": "Device:",
    "label_compute_type": "Compute Type:",
    "label_beam_size": "Beam Size:",

    "button_test_ollama": "Ollama testen",

    "suffix_seconds": " Sekunden",
    "suffix_hz": " Hz",
    "suffix_tokens": " Tokens",

    "language_german": "Deutsch",
    "language_english": "English",

    "tooltip_show_command_input": (
        "Zeigt oder versteckt die manuelle Befehlszeile unter den Sprachbuttons."
    ),
    "tooltip_interface_language": (
        "Sprache der Bedienoberfläche."
    ),
    "tooltip_text_generation_language": (
        "Sprache, in der die KI neue Texte erzeugt, Texte fortsetzt und markierte Texte überarbeitet."
    ),
    "tooltip_ollama_base_url": (
        "Adresse der lokalen Ollama-API. Standard: http://localhost:11434"
    ),
    "tooltip_model_name": (
        "Name des Ollama-Modells, z. B. qwen3:8b."
    ),
    "tooltip_timeout": (
        "Maximale Wartezeit für eine KI-Antwort in Sekunden."
    ),
    "tooltip_fake_mode": (
        "Wenn aktiviert, verwendet Dictator Platzhalterantworten statt echter KI."
    ),
    "tooltip_temperature": (
        "Steuert die Kreativität der Antwort. "
        "Niedrige Werte sind sachlicher, höhere Werte freier und kreativer."
    ),
    "tooltip_num_predict": (
        "Maximale Länge der KI-Antwort in Tokens. "
        "Höhere Werte erlauben längere Antworten, können aber langsamer sein."
    ),
    "tooltip_speech_model_size": (
        "Whisper-Modellgröße. Größer ist genauer, aber langsamer. "
        "Für Dictator empfohlen: medium."
    ),
    "tooltip_speech_sample_rate": (
        "Samplerate der Mikrofonaufnahme. Für Dictator aktuell empfohlen: 16000 Hz."
    ),
    "tooltip_speech_device": (
        "cpu für normale Rechner, cuda für NVIDIA-GPU."
    ),
    "tooltip_speech_compute_type": (
        "Rechenformat für faster-whisper. CPU: int8 oder float32. NVIDIA-GPU: float16."
    ),
    "tooltip_speech_beam_size": (
        "Suchbreite der Transkription. Höher kann genauer sein, aber langsamer. Empfohlen: 10."
    ),
    "tooltip_test_ollama": (
        "Prüft, ob Ollama erreichbar ist und ob das angegebene Modell vorhanden ist."
    ),

    "ollama_test_title": "Ollama-Test",
    "ollama_base_url_missing": "Bitte gib eine Ollama-Adresse ein.",
    "ollama_model_name_missing": "Bitte gib einen Modellnamen ein.",
    "ollama_no_models_found": "(keine Modelle gefunden)",
    "ollama_found_models": "Gefundene Modelle:",
    "ollama_test_success": "Ollama ist erreichbar.\n\n{message}\n\nModelle:\n{models}",
    "ollama_test_failure": "Ollama-Test fehlgeschlagen.\n\n{message}",
}

VOICE_COMMAND_CORRECTIONS = {
    "fett punkt": "fett",
    "fett ausrufezeichen": "fett",

    "kursiv punkt": "kursiv",
    "kursiv ausrufezeichen": "kursiv",

    "speichern punkt": "speichern",
    "speichern ausrufezeichen": "speichern",

    "öffnen punkt": "öffnen",
    "oeffnen": "öffnen",
    "oeffnen punkt": "öffnen",

    "neu punkt": "neu",
    "neue datei punkt": "neue datei",

    "rückgängig punkt": "rückgängig",
    "rueckgängig": "rückgängig",
    "rueckgaengig": "rückgängig",
    "rueckgaengig punkt": "rückgängig",

    "wiederholen punkt": "wiederholen",

    "alles markieren punkt": "alles markieren",
    "neue zeile punkt": "neue zeile",

    "ki status punkt": "ki status",
    "ollama test punkt": "ollama test",

    "einstellungen punkt": "einstellungen",
}

LLM_WORKER_MESSAGES = {
    "no_selection": "Keine Auswahl für KI-Bearbeitung vorhanden.",
    "unknown_mode": "Unbekannter KI-Modus: {mode}",
    "empty_response": "Die KI hat keinen Text zurückgegeben.",
    "worker_error": "KI-Fehler: {error}",
}
