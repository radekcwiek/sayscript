import requests


class LlmClient:
    def __init__(
        self,
        model_name: str = "qwen3:8b",
        base_url: str = "http://localhost:11434",
        timeout: int = 600,
        use_fake_response: bool = False,
    ):
        self.model_name = model_name
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.use_fake_response = use_fake_response

    def generate_text(self, prompt: str) -> str:
        if self.use_fake_response:
            return self.generate_fake_text(prompt)

        return self.generate_with_ollama(prompt)

    def generate_fake_text(self, prompt: str) -> str:
        return (
            "[KI-Generierung Platzhalter]\n\n"
            f"Aufgabe: {prompt}\n\n"
            "Hier wird später die Antwort von Qwen eingefügt."
        )

    def generate_with_ollama(self, prompt: str) -> str:
        url = f"{self.base_url}/api/generate"

        payload = {
            "model": self.model_name,
            "prompt": self.build_generation_prompt(prompt),
            "stream": False,
            "options": {
                "temperature": 0.7,
                "num_predict": 600,
            },
        }

        try:
            response = requests.post(
                url,
                json=payload,
                timeout=self.timeout,
            )
            response.raise_for_status()

        except requests.exceptions.ConnectionError:
            return (
                "[Fehler]\n\n"
                "Ollama ist nicht erreichbar. Läuft Ollama auf diesem Rechner?"
            )

        except requests.exceptions.Timeout:
            return (
                "[Fehler]\n\n"
                "Die KI-Anfrage hat zu lange gedauert."
            )

        except requests.exceptions.RequestException as error:
            return (
                "[Fehler]\n\n"
                f"Die KI-Anfrage ist fehlgeschlagen:\n{error}"
            )

        data = response.json()
        generated_text = data.get("response", "").strip()

        if not generated_text:
            return (
                "[Fehler]\n\n"
                "Das Modell hat keinen Text zurückgegeben."
            )

        return generated_text

    def build_generation_prompt(self, user_prompt: str) -> str:
        return (
            "Du bist ein hilfreicher Schreibassistent innerhalb einer lokalen "
            "Textverarbeitung namens Dictator.\n\n"
            "Schreibe den gewünschten Text direkt aus. "
            "Gib keine Erklärungen über deine Vorgehensweise. "
            "Gib nur den Text zurück, der in das Dokument eingefügt werden soll.\n\n"
            f"Aufgabe: {user_prompt}"
        )
