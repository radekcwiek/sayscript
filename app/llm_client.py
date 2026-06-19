# SPDX-License-Identifier: Apache-2.0

"""
Client for local LLM communication through Ollama.

LlmClient is the central interface between SayScript and the local Ollama API.
It supports three main text operations:

- generate new text from a prompt
- transform selected text according to an instruction
- continue existing text

The client can also run in fake-response mode, which is useful for UI testing
without a running Ollama instance.
"""

import requests

from app.settings import load_settings
from app.localization import (
    llm_message,
    llm_prompt,
    llm_text_generation_language_name,
)


class LlmClient:
    """
    Small wrapper around Ollama's local HTTP API.

    Settings are loaded during initialization, but individual connection
    parameters can be overridden. This is used by the settings dialogue and
    diagnostics code to test custom values before they become permanent.
    """

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

    # Public text operations ------------------------------------------------

    def generate_text(self, prompt: str) -> str:
        """
        Generate a new text from a user prompt.

        In fake mode, no HTTP request is made.
        """
        if self.use_fake_response:
            return self.generate_fake_text(prompt)

        return self.generate_with_ollama(prompt)

    def transform_text(self, instruction: str, selected_text: str) -> str:
        """
        Transform selected text according to a user instruction.

        Example instructions could be "make this shorter" or
        "rewrite this in a more formal tone".
        """
        if self.use_fake_response:
            return llm_message(
                "fake_transform",
                instruction=instruction,
                selected_text=selected_text,
            )

        return self.transform_with_ollama(instruction, selected_text)

    def continue_text(self, context_text: str) -> str:
        """
        Continue existing text using the current document context.
        """
        if self.use_fake_response:
            return llm_message(
                "fake_continue",
                context_text=context_text,
            )

        return self.continue_with_ollama(context_text)

    # Ollama-backed operations ---------------------------------------------

    def generate_with_ollama(self, prompt: str) -> str:
        """Generate text through Ollama."""
        return self.request_ollama(
            prompt=self.build_generation_prompt(prompt),
            temperature=self.settings["generate_temperature"],
            num_predict=self.settings["generate_num_predict"],
        )

    def transform_with_ollama(self, instruction: str, selected_text: str) -> str:
        """Transform selected text through Ollama."""
        return self.request_ollama(
            prompt=self.build_transform_prompt(instruction, selected_text),
            temperature=self.settings["transform_temperature"],
            num_predict=self.settings["transform_num_predict"],
        )

    def continue_with_ollama(self, context_text: str) -> str:
        """Continue text through Ollama."""
        return self.request_ollama(
            prompt=self.build_continue_prompt(context_text),
            temperature=self.settings["continue_temperature"],
            num_predict=self.settings["continue_num_predict"],
        )

    # Prompt builders -------------------------------------------------------

    def build_generation_prompt(self, user_prompt: str) -> str:
        """Build the localized prompt used for text generation."""
        output_language = self.get_text_generation_language_name()

        return llm_prompt(
            "generation",
            output_language=output_language,
            user_prompt=user_prompt,
        )

    def build_transform_prompt(self, instruction: str, selected_text: str) -> str:
        """Build the localized prompt used for selected-text transformation."""
        output_language = self.get_text_generation_language_name()

        return llm_prompt(
            "transform",
            output_language=output_language,
            instruction=instruction,
            selected_text=selected_text,
        )

    def build_continue_prompt(self, context_text: str) -> str:
        """Build the localized prompt used for text continuation."""
        output_language = self.get_text_generation_language_name()

        return llm_prompt(
            "continue",
            output_language=output_language,
            context_text=context_text,
        )

    # HTTP communication ----------------------------------------------------

    def request_ollama(
        self,
        prompt: str,
        temperature: float,
        num_predict: int,
    ) -> str:
        """
        Send a non-streaming chat request to Ollama and return the response text.

        SayScript uses /api/chat instead of /api/generate because chat models
        often behave more reliably with this endpoint. The "think": False flag
        is used for thinking-capable models that support disabling reasoning
        output.
        """
        url = f"{self.base_url}/api/chat"

        payload = {
            "model": self.model_name,
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            "stream": False,
            "think": False,
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
            return llm_message("ollama_connection_error")

        except requests.exceptions.Timeout:
            return llm_message("ollama_timeout_error")

        except requests.exceptions.RequestException as error:
            return llm_message("ollama_request_error", error=error)

        data = response.json()

        message = data.get("message", {})
        generated_text = message.get("content", "").strip()

        if not generated_text:
            thinking_text = message.get("thinking", "").strip()

            return llm_message(
                "ollama_empty_response",
                thinking_text=thinking_text[:1000],
                data=data,
            )

        return generated_text

    # Status checks ---------------------------------------------------------

    def check_ollama_status(self) -> dict:
        """
        Check whether Ollama is reachable and whether the configured model exists.

        Returns a small dictionary that can be displayed in the settings dialogue
        or diagnostics dialogue.
        """
        url = f"{self.base_url}/api/tags"

        try:
            response = requests.get(
                url,
                timeout=10,
            )
            response.raise_for_status()

        except requests.exceptions.ConnectionError:
            return {
                "ok": False,
                "message": llm_message("ollama_status_connection_error"),
                "models": [],
            }

        except requests.exceptions.Timeout:
            return {
                "ok": False,
                "message": llm_message("ollama_status_timeout_error"),
                "models": [],
            }

        except requests.exceptions.RequestException as error:
            return {
                "ok": False,
                "message": llm_message("ollama_status_request_error", error=error),
                "models": [],
            }

        data = response.json()
        models = data.get("models", [])

        model_names = [
            model.get("name", "")
            for model in models
            if model.get("name")
        ]

        model_available = self.model_name in model_names

        if model_available:
            message = llm_message(
                "ollama_status_model_found",
                model_name=self.model_name,
            )
        else:
            message = llm_message(
                "ollama_status_model_not_found",
                model_name=self.model_name,
            )

        return {
            "ok": model_available,
            "message": message,
            "models": model_names,
        }

    # Helpers ---------------------------------------------------------------

    def generate_fake_text(self, prompt: str) -> str:
        """
        Return a localized fake response for development and UI testing.
        """
        return llm_message("fake_generation", prompt=prompt)

    def get_text_generation_language_name(self) -> str:
        """
        Return the localized language name used inside LLM prompts.

        The settings store a compact language code such as "de" or "en".
        Prompt templates use a human-readable language name.
        """
        language_code = self.settings.get("text_generation_language", "de")
        return llm_text_generation_language_name(language_code)
