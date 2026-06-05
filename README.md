command_router.py → versteht Befehle
llm_client.py     → spricht mit Ollama/Qwen
llm_worker.py     → führt KI-Aufrufe im Hintergrund aus
main.py           → Editor, UI, Einfügen, Speichern
config.py         → zentrale KI-Einstellungen

Hinweis für Entwickler:
Bei Microsoft-Store-Python kann settings.json beim Start über python main.py
unter AppData\Local\Packages\PythonSoftwareFoundation... landen.
Die gebaute EXE verwendet den normalen AppData-Ordner.
