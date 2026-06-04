class LlmClient:
    def generate_text(self, prompt: str) -> str:
        return (
            "[KI-Generierung Platzhalter]\n\n"
            f"Aufgabe: {prompt}\n\n"
            "Hier wird später die Antwort von Qwen eingefügt."
        )
