import requests
from app import config
from app.settings import load_settings


class LlmClient:
    def __init__(
        self,
        model_name: str | None = None,
        base_url: str | None = None,
        timeout: int | None = None,
        use_fake_response: bool | None = None,
    ):
        self.settings = load_settings()

        self.model_name = (
            model_name
            or self.settings["ollama_model_name"]
        )

        self.base_url = (
            base_url
            or self.settings["ollama_base_url"]
        ).rstrip("/")

        self.timeout = (
            timeout
            or self.settings["llm_timeout_seconds"]
        )

        if use_fake_response is None:
            self.use_fake_response = self.settings["use_fake_llm"]
        else:
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
        return self.request_ollama(
            prompt=self.build_generation_prompt(prompt),
            temperature=self.settings["generate_temperature"],
            num_predict=self.settings["generate_num_predict"],
        )


    def build_generation_prompt(self, user_prompt: str) -> str:
        return (
            "Du bist ein hilfreicher Schreibassistent innerhalb einer lokalen "
            "Textverarbeitung namens Dictator.\n\n"
            "Schreibe den gewünschten Text direkt aus. "
            "Gib keine Erklärungen über deine Vorgehensweise. "
            "Gib nur den Text zurück, der in das Dokument eingefügt werden soll.\n\n"
            f"Aufgabe: {user_prompt}"
        )


    def transform_text(self, instruction: str, selected_text: str) -> str:
        if self.use_fake_response:
            return (
                "[KI-Transformation Platzhalter]\n\n"
                f"Anweisung: {instruction}\n\n"
                f"Ausgangstext:\n{selected_text}"
            )

        return self.transform_with_ollama(instruction, selected_text)


    def transform_with_ollama(self, instruction: str, selected_text: str) -> str:
        return self.request_ollama(
            prompt=self.build_transform_prompt(instruction, selected_text),
            temperature=self.settings["transform_temperature"],
            num_predict=self.settings["transform_num_predict"],
        )


    def build_transform_prompt(self, instruction: str, selected_text: str) -> str:
        return (
            "Du bist ein hilfreicher Schreibassistent innerhalb einer lokalen "
            "Textverarbeitung namens Dictator.\n\n"
            "Bearbeite den folgenden Text gemäß der Anweisung. "
            "Gib ausschließlich den überarbeiteten Text zurück. "
            "Keine Kommentare, keine Erklärungen, keine Markdown-Umrahmung.\n\n"
            f"Anweisung: {instruction}\n\n"
            f"Text:\n{selected_text}"
        )


    def continue_text(self, context_text: str) -> str:
        if self.use_fake_response:
            return (
                "[KI-Fortsetzung Platzhalter]\n\n"
                f"Kontext:\n{context_text}\n\n"
                "Hier wird später die Fortsetzung von Qwen eingefügt."
            )

        return self.continue_with_ollama(context_text)


    def continue_with_ollama(self, context_text: str) -> str:
        return self.request_ollama(
            prompt=self.build_continue_prompt(context_text),
            temperature=self.settings["continue_temperature"],
            num_predict=self.settings["continue_num_predict"],
        )


    def build_continue_prompt(self, context_text: str) -> str:
        return (
            "Du bist ein hilfreicher Schreibassistent innerhalb einer lokalen "
            "Textverarbeitung namens Dictator.\n\n"
            "Schreibe den folgenden Text sinnvoll weiter. "
            "Gib nur die Fortsetzung zurück, nicht den bisherigen Text. "
            "Keine Kommentare, keine Erklärungen, keine Markdown-Umrahmung.\n\n"
            f"Bisheriger Text:\n{context_text}"
        )


    def request_ollama(
        self,
        prompt: str,
        temperature: float,
        num_predict: int,
    ) -> str:
        url = f"{self.base_url}/api/generate"

        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": num_predict,
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
