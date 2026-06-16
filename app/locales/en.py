COMMAND_ALIASES = {
    "bold": {
        "bold",
        "make bold",
        "format bold",
    },
    "italic": {
        "italic",
        "make italic",
        "format italic",
    },
    "delete_selection": {
        "delete selection",
        "delete selected text",
        "remove selection",
        "remove selected text",
    },
    "select_all": {
        "select all",
        "select everything",
        "mark all",
    },
    "new_line": {
        "new line",
        "line break",
        "new paragraph",
        "paragraph",
    },
    "undo": {
        "undo",
    },
    "redo": {
        "redo",
    },
    "cut": {
        "cut",
        "cut selection",
        "cut selected text",
    },
    "copy": {
        "copy",
        "copy selection",
        "copy selected text",
    },
    "paste": {
        "paste",
        "insert from clipboard",
    },
    "save": {
        "save",
        "save file",
        "save document",
    },
    "open": {
        "open",
        "open file",
        "open document",
    },
    "new_file": {
        "new",
        "new file",
        "new document",
        "create new document",
    },
    "export_pdf": {
        "export as pdf",
        "export pdf",
        "save as pdf",

        "export as p d f",
        "export p d f",
        "save as p d f",

        "export as pdf file",
        "export pdf file",
        "save as pdf file",
    },
    "print_document": {
        "print",
        "print document",
        "print file",
        "send to printer",
    },
    "diagnostics": {
        "diagnostics",
        "diagnosis",
        "system check",
        "show diagnostics",
        "open diagnostics",
        "show system status",
        "system status",
    },
    "heading_1": {
        "heading 1",
        "heading one",
        "title",
        "make heading 1",
        "make title",
    },
    "heading_2": {
        "heading 2",
        "heading two",
        "subtitle",
        "make heading 2",
    },
    "normal_text": {
        "normal text",
        "default text",
        "regular text",
        "standard text",
    },
    "align_left": {
        "align left",
        "left align",
        "text left",
    },
    "align_center": {
        "align center",
        "center",
        "center text",
        "center align",
    },
    "align_right": {
        "align right",
        "right align",
        "text right",
    },
    "bullet_list": {
        "bullet list",
        "bulleted list",
        "list",
        "list with bullets",
    },
    "numbered_list": {
        "numbered list",
        "numbering",
        "list with numbers",
    },
    "indent": {
        "indent",
        "indent text",
        "indent paragraph",
    },
    "outdent": {
        "outdent",
        "outdent text",
        "outdent paragraph",
        "decrease indent",
    },
    "continue_text": {
        "continue",
        "continue text",
        "write on",
        "keep writing",
        "continue writing",
    },
    "remove_list": {
        "remove list",
        "delete list",
        "no list",
        "remove bullets",
        "remove numbering",
        "back to text",
    },
    "ai_status": {
        "ai status",
        "model status",
        "ollama status",
        "show ai status",
        "system status",
        "status",
        "speech recognition status",
        "whisper status",
    },
    "ollama_test": {
        "ollama test",
        "ai test",
        "model test",
        "test ollama",
        "test ai",
    },
    "open_settings_dialog": {
        "settings",
        "open settings",
        "configuration",
        "open configuration",
    },
    "about": {
        "version",
        "about",
        "about sayscript",
        "program info",
        "app info",
    },
}


FONT_SIZE_PREFIXES = {
    "font size",
    "text size",
    "size",
}

FONT_FAMILY_PREFIXES = {
    "font",
    "font family",
    "typeface",
}

INSERT_TEXT_PREFIXES = {
    "insert",
    "insert text",
    "type",
    "write",
}

SEARCH_TEXT_PREFIXES = {
    "search for",
    "search",
    "find",
    "find text",
}

REPLACE_SELECTION_PREFIXES = {
    "replace selection with",
    "replace selected text with",
    "replace with",
}

REPLACE_TEXT_PREFIXES = {
    "replace",
    "replace next",
}

REPLACE_TEXT_SEPARATORS = {
    "with",
}

GENERATE_TEXT_PREFIXES = {
    "generate",
    "create",
    "write a text about",
    "write a short text about",
    "write a paragraph about",
    "write an introduction to",
    "draft",
}

TRANSFORM_SELECTION_PREFIXES = {
    "transform selection",
    "rewrite selection",
    "rewrite selected text",
    "change selection",
    "change selected text",
    "improve selection",
    "improve selected text",
    "make selection",
    "make selected text",
    "shorten selection",
    "make selection shorter",
}

MESSAGES = {
    "unknown_command": "Unknown command: {command}",
    "command_corrected": "Command corrected: {original} → {alias}",

    "executed_bold": "Command executed: bold",
    "executed_italic": "Command executed: italic",
    "executed_delete_selection": "Command executed: selection deleted",
    "executed_select_all": "Command executed: selected all",
    "executed_new_line": "Command executed: new line",
    "executed_undo": "Command executed: undo",
    "executed_redo": "Command executed: redo",
    "executed_cut": "Command executed: cut",
    "executed_copy": "Command executed: copy",
    "executed_paste": "Command executed: paste",

    "executed_save": "Command executed: save",
    "save_cancelled": "Save cancelled",
    "executed_open": "Command executed: open",
    "open_cancelled": "Open cancelled",
    "executed_new_file": "Command executed: new file",
    "new_file_cancelled": "New file cancelled",

    "executed_export_pdf": "Command executed: export as PDF",
    "export_pdf_cancelled": "PDF export cancelled",
    "executed_print": "Command executed: print",
    "print_cancelled": "Print cancelled",
    "executed_about": "Command executed: About SayScript",
    "executed_diagnostics": "Command executed: diagnostics",

    "executed_heading_1": "Command executed: heading 1",
    "executed_heading_2": "Command executed: heading 2",
    "executed_normal_text": "Command executed: normal text",
    "executed_align_left": "Command executed: align left",
    "executed_align_center": "Command executed: align center",
    "executed_align_right": "Command executed: align right",

    "executed_bullet_list": "Command executed: bullet list",
    "executed_numbered_list": "Command executed: numbered list",
    "executed_remove_list": "Command executed: list removed",
    "executed_indent": "Command executed: indent",
    "executed_outdent": "Command executed: outdent",

    "executed_font_size": "Command executed: font size {value}",
    "executed_font_family": "Command executed: font {value}",
    "executed_insert_text": "Command executed: text inserted",

    "font_size_out_of_range": "Font size must be between 6 and 96",
}

SPEECH_LANGUAGE = "en"

SPEECH_INITIAL_PROMPT = (
    "This is English dictated text for a word processor. "
    "Use correct English spelling, punctuation, and natural wording."
)

SPEECH_MESSAGES = {
    "no_text_recognized": "No text recognized.",
    "transcription_error": "Transcription error: {error}",
}

LLM_TEXT_GENERATION_LANGUAGE_NAMES = {
    "de": "German",
    "en": "English",
}

LLM_PROMPTS = {
    "generation": (
        "You are a writing assistant inside a word processor.\n\n"
        "IMPORTANT:\n"
        "- Return only the finished text.\n"
        "- No analysis.\n"
        "- No thoughts.\n"
        "- No explanation.\n"
        "- No introduction.\n"
        "- Do not write what you are going to do.\n"
        "- Return only the text that should be inserted into the document.\n"
        "- Write the text in this language: {output_language}.\n\n"
        "Task: {user_prompt}"
    ),
    "transform": (
        "You are a helpful writing assistant inside a local word processor "
        "called SayScript.\n\n"
        "Edit the following text according to the instruction. "
        "Return only the revised text. "
        "No comments, no explanations, no Markdown wrapper. "
        "Write the revised text in this language: {output_language}.\n\n"
        "Instruction: {instruction}\n\n"
        "Text:\n{selected_text}"
    ),
    "continue": (
        "You are a helpful writing assistant inside a local word processor "
        "called SayScript.\n\n"
        "Continue the following text in a natural way. "
        "Return only the continuation, not the existing text. "
        "No comments, no explanations, no Markdown wrapper. "
        "Write the continuation in this language: {output_language}.\n\n"
        "Existing text:\n{context_text}"
    ),
}

LLM_MESSAGES = {
    "fake_generation": (
        "[AI generation placeholder]\n\n"
        "Task: {prompt}\n\n"
        "Qwen's response will be inserted here later."
    ),
    "fake_transform": (
        "[AI transformation placeholder]\n\n"
        "Instruction: {instruction}\n\n"
        "Original text:\n{selected_text}"
    ),
    "fake_continue": (
        "[AI continuation placeholder]\n\n"
        "Context:\n{context_text}\n\n"
        "Qwen's continuation will be inserted here later."
    ),

    "ollama_connection_error": (
        "[Error]\n\n"
        "Ollama is not reachable. Is Ollama running on this computer?"
    ),
    "ollama_timeout_error": (
        "[Error]\n\n"
        "The AI request took too long."
    ),
    "ollama_request_error": (
        "[Error]\n\n"
        "The AI request failed:\n{error}"
    ),
    "ollama_empty_response": (
        "[Error]\n\n"
        "The model did not return any visible text.\n\n"
        "Thinking field:\n{thinking_text}\n\n"
        "Ollama response:\n{data}"
    ),

    "ollama_status_connection_error": "Ollama is not reachable.",
    "ollama_status_timeout_error": "The Ollama request took too long.",
    "ollama_status_request_error": "Ollama status request failed: {error}",
    "ollama_status_model_found": "Ollama is reachable. Model found: {model_name}",
    "ollama_status_model_not_found": "Ollama is reachable, but model not found: {model_name}",
}

SETTINGS_DIALOG_TEXTS = {
    "title": "Settings",

    "group_connection": "Connection",
    "group_generation": "Generation",
    "group_transform": "Transformation",
    "group_continue": "Continuation",
    "group_speech": "Speech recognition",

    "label_ollama_base_url": "Ollama address:",
    "label_model_name": "Model name:",
    "label_timeout": "Timeout:",
    "label_fake_mode": "Fake mode:",
    "label_show_command_input": "Show command input:",
    "label_interface_language": "Interface language:",
    "label_text_generation_language": "Text language:",

    "label_temperature": "Temperature:",
    "label_max_response_length": "Max. response length:",

    "label_whisper_model": "Whisper model:",
    "label_sample_rate": "Sample rate:",
    "label_device": "Device:",
    "label_compute_type": "Compute type:",
    "label_beam_size": "Beam size:",

    "button_test_ollama": "Test Ollama",

    "suffix_seconds": " seconds",
    "suffix_hz": " Hz",
    "suffix_tokens": " tokens",

    "language_german": "Deutsch",
    "language_english": "English",

    "label_show_speech_result": "Show recognized speech:",
    "tooltip_show_speech_result": (
        "Shows or hides the line with the most recently recognized dictation or voice command."
    ),

    "tooltip_show_command_input": (
        "Shows or hides the manual command input below the speech buttons."
    ),
    "tooltip_interface_language": (
        "Language of the user interface."
    ),
    "tooltip_text_generation_language": (
        "Language used by the AI for generating, continuing, and transforming text."
    ),
    "tooltip_ollama_base_url": (
        "Address of the local Ollama API. Default: http://localhost:11434"
    ),
    "tooltip_model_name": (
        "Name of the Ollama model, e.g. qwen3:8b."
    ),
    "tooltip_timeout": (
        "Maximum waiting time for an AI response in seconds."
    ),
    "tooltip_fake_mode": (
        "When enabled, SayScript uses placeholder responses instead of real AI."
    ),
    "tooltip_temperature": (
        "Controls the creativity of the response. "
        "Lower values are more factual, higher values are freer and more creative."
    ),
    "tooltip_num_predict": (
        "Maximum length of the AI response in tokens. "
        "Higher values allow longer responses, but can be slower."
    ),
    "tooltip_speech_model_size": (
        "Whisper model size. Larger is more accurate, but slower. "
        "Recommended for SayScript: medium."
    ),
    "tooltip_speech_sample_rate": (
        "Sample rate of the microphone recording. Currently recommended for SayScript: 16000 Hz."
    ),
    "tooltip_speech_device": (
        "cpu for normal computers, cuda for NVIDIA GPUs."
    ),
    "tooltip_speech_compute_type": (
        "Compute format for faster-whisper. CPU: int8 or float32. NVIDIA GPU: float16."
    ),
    "tooltip_speech_beam_size": (
        "Search width of the transcription. Higher can be more accurate, but slower. Recommended: 10."
    ),
    "tooltip_test_ollama": (
        "Checks whether Ollama is reachable and whether the selected model is available."
    ),

    "ollama_test_title": "Ollama test",
    "ollama_base_url_missing": "Please enter an Ollama address.",
    "ollama_model_name_missing": "Please enter a model name.",
    "ollama_no_models_found": "(no models found)",
    "ollama_found_models": "Found models:",
    "ollama_test_success": "Ollama is reachable.\n\n{message}\n\nModels:\n{models}",
    "ollama_test_failure": "Ollama test failed.\n\n{message}",
}

VOICE_COMMAND_CORRECTIONS = {
    "bold period": "bold",
    "bold dot": "bold",
    "bold full stop": "bold",
    "bold exclamation mark": "bold",

    "italic period": "italic",
    "italic dot": "italic",
    "italic full stop": "italic",
    "italic exclamation mark": "italic",

    "save period": "save",
    "save dot": "save",
    "save full stop": "save",

    "open period": "open",
    "open dot": "open",
    "open full stop": "open",

    "new period": "new",
    "new file period": "new file",

    "undo period": "undo",
    "redo period": "redo",

    "select all period": "select all",
    "new line period": "new line",

    "ai status period": "ai status",
    "ollama test period": "ollama test",

    "settings period": "settings",

    "export as pdf period": "export as pdf",
    "export pdf period": "export pdf",
    "save as pdf period": "save as pdf",
    "export as p d f period": "export as p d f",
    "export p d f period": "export p d f",

    "print period": "print",
    "print document period": "print document",
    "send to printer period": "send to printer",

    "diagnostics period": "diagnostics",
    "diagnosis period": "diagnosis",
    "system check period": "system check",
    "show diagnostics period": "show diagnostics",
}

LLM_WORKER_MESSAGES = {
    "no_selection": "No selection available for AI editing.",
    "unknown_mode": "Unknown AI mode: {mode}",
    "empty_response": "The AI did not return any text.",
    "worker_error": "AI error: {error}",
}
