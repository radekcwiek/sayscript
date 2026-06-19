# SPDX-License-Identifier: Apache-2.0

"""
Settings dialogue for SayScript.

This dialogue lets the user configure Ollama, local LLM parameters, speech
recognition, interface options, language settings, and auto-save behavior.

The settings are loaded from app.settings when the dialogue opens and are written
back when the user presses Save.
"""

from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFormLayout,
    QGroupBox,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from app.llm_client import LlmClient
from app.localization import settings_text
from app.settings import load_settings, save_settings


class SettingsDialog(QDialog):
    """
    Dialog for editing persistent SayScript settings.

    The settings content is placed inside a scroll area so the dialogue remains
    usable on smaller screens. The button row stays outside the scroll area and
    is therefore always visible.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.settings = load_settings()

        self.configure_window()
        self.create_input_widgets()
        self.create_button_box()
        self.create_main_layout()

    # Window setup ----------------------------------------------------------

    def configure_window(self) -> None:
        """Configure title and default size of the settings dialogue."""
        self.setWindowTitle(self.txt("title"))
        self.setMinimumWidth(520)
        self.setMinimumHeight(420)
        self.resize(620, 720)

    # Widget creation -------------------------------------------------------

    def create_input_widgets(self) -> None:
        """Create all input widgets used by the dialogue."""
        self.create_ollama_inputs()
        self.create_interface_inputs()
        self.create_generation_inputs()
        self.create_speech_inputs()
        self.create_autosave_inputs()

    def create_ollama_inputs(self) -> None:
        """Create widgets for Ollama connection and general LLM settings."""
        self.ollama_base_url_input = QLineEdit()
        self.ollama_base_url_input.setText(
            self.settings["ollama_base_url"]
        )
        self.ollama_base_url_input.setToolTip(
            self.txt("tooltip_ollama_base_url")
        )

        self.model_name_input = QLineEdit()
        self.model_name_input.setText(
            self.settings["ollama_model_name"]
        )
        self.model_name_input.setToolTip(
            self.txt("tooltip_model_name")
        )

        self.timeout_input = QSpinBox()
        self.timeout_input.setRange(10, 3600)
        self.timeout_input.setValue(
            int(self.settings["llm_timeout_seconds"])
        )
        self.timeout_input.setSuffix(self.txt("suffix_seconds"))
        self.timeout_input.setToolTip(
            self.txt("tooltip_timeout")
        )

        self.fake_llm_checkbox = QCheckBox()
        self.fake_llm_checkbox.setChecked(
            bool(self.settings["use_fake_llm"])
        )
        self.fake_llm_checkbox.setToolTip(
            self.txt("tooltip_fake_mode")
        )

        self.test_ollama_button = QPushButton(
            self.txt("button_test_ollama")
        )
        self.test_ollama_button.clicked.connect(
            self.test_ollama_connection
        )
        self.test_ollama_button.setToolTip(
            self.txt("tooltip_test_ollama")
        )

    def create_interface_inputs(self) -> None:
        """Create widgets for UI visibility and language settings."""
        self.show_command_input_checkbox = QCheckBox()
        self.show_command_input_checkbox.setChecked(
            bool(self.settings["show_command_input"])
        )
        self.show_command_input_checkbox.setToolTip(
            self.txt("tooltip_show_command_input")
        )

        self.show_speech_result_checkbox = QCheckBox()
        self.show_speech_result_checkbox.setChecked(
            bool(self.settings["show_speech_result"])
        )
        self.show_speech_result_checkbox.setToolTip(
            self.txt("tooltip_show_speech_result")
        )

        self.interface_language_input = self.create_language_combo_box(
            self.settings["interface_language"]
        )
        self.interface_language_input.setToolTip(
            self.txt("tooltip_interface_language")
        )

        self.text_generation_language_input = self.create_language_combo_box(
            self.settings["text_generation_language"]
        )
        self.text_generation_language_input.setToolTip(
            self.txt("tooltip_text_generation_language")
        )

    def create_generation_inputs(self) -> None:
        """Create widgets for generation, transformation, and continuation."""
        temperature_tooltip = self.txt("tooltip_temperature")
        num_predict_tooltip = self.txt("tooltip_num_predict")

        self.generate_temperature_input = self.create_temperature_input(
            self.settings["generate_temperature"]
        )
        self.generate_temperature_input.setToolTip(temperature_tooltip)

        self.generate_num_predict_input = self.create_num_predict_input(
            self.settings["generate_num_predict"]
        )
        self.generate_num_predict_input.setToolTip(num_predict_tooltip)

        self.transform_temperature_input = self.create_temperature_input(
            self.settings["transform_temperature"]
        )
        self.transform_temperature_input.setToolTip(temperature_tooltip)

        self.transform_num_predict_input = self.create_num_predict_input(
            self.settings["transform_num_predict"]
        )
        self.transform_num_predict_input.setToolTip(num_predict_tooltip)

        self.continue_temperature_input = self.create_temperature_input(
            self.settings["continue_temperature"]
        )
        self.continue_temperature_input.setToolTip(temperature_tooltip)

        self.continue_num_predict_input = self.create_num_predict_input(
            self.settings["continue_num_predict"]
        )
        self.continue_num_predict_input.setToolTip(num_predict_tooltip)

    def create_speech_inputs(self) -> None:
        """Create widgets for faster-whisper transcription settings."""
        self.speech_model_size_input = QComboBox()
        self.speech_model_size_input.addItems(
            ["tiny", "base", "small", "medium", "large-v3"]
        )
        self.speech_model_size_input.setCurrentText(
            self.settings["speech_model_size"]
        )
        self.speech_model_size_input.setToolTip(
            self.txt("tooltip_speech_model_size")
        )

        self.speech_sample_rate_input = QSpinBox()
        self.speech_sample_rate_input.setRange(8000, 48000)
        self.speech_sample_rate_input.setSingleStep(1000)
        self.speech_sample_rate_input.setValue(
            int(self.settings["speech_sample_rate"])
        )
        self.speech_sample_rate_input.setSuffix(self.txt("suffix_hz"))
        self.speech_sample_rate_input.setToolTip(
            self.txt("tooltip_speech_sample_rate")
        )

        self.speech_device_input = QComboBox()
        self.speech_device_input.addItems(["cpu", "cuda"])
        self.speech_device_input.setCurrentText(
            self.settings["speech_device"]
        )
        self.speech_device_input.setToolTip(
            self.txt("tooltip_speech_device")
        )

        self.speech_compute_type_input = QComboBox()
        self.speech_compute_type_input.addItems(
            ["int8", "float32", "float16"]
        )
        self.speech_compute_type_input.setCurrentText(
            self.settings["speech_compute_type"]
        )
        self.speech_compute_type_input.setToolTip(
            self.txt("tooltip_speech_compute_type")
        )

        self.speech_beam_size_input = QSpinBox()
        self.speech_beam_size_input.setRange(1, 20)
        self.speech_beam_size_input.setValue(
            int(self.settings["speech_beam_size"])
        )
        self.speech_beam_size_input.setToolTip(
            self.txt("tooltip_speech_beam_size")
        )

    def create_autosave_inputs(self) -> None:
        """Create widgets for auto-save settings."""
        self.enable_autosave_checkbox = QCheckBox(
            self.txt("enable_autosave")
        )
        self.enable_autosave_checkbox.setChecked(
            bool(self.settings["enable_autosave"])
        )

        self.autosave_interval_input = QSpinBox()
        self.autosave_interval_input.setRange(10, 3600)
        self.autosave_interval_input.setSingleStep(10)
        self.autosave_interval_input.setValue(
            int(self.settings["autosave_interval_seconds"])
        )

    def create_button_box(self) -> None:
        """Create Save and Cancel buttons."""
        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
        )
        self.button_box.accepted.connect(self.save_and_accept)
        self.button_box.rejected.connect(self.reject)

    # Layout creation -------------------------------------------------------

    def create_main_layout(self) -> None:
        """Build the dialogue layout with scrollable settings and fixed buttons."""
        layout = QVBoxLayout()
        layout.addWidget(self.create_scroll_area())
        layout.addWidget(self.button_box)

        self.setLayout(layout)

    def create_scroll_area(self) -> QScrollArea:
        """Create the scroll area containing all settings groups."""
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)

        content_layout.addWidget(self.create_connection_group())
        content_layout.addWidget(self.create_generate_group())
        content_layout.addWidget(self.create_transform_group())
        content_layout.addWidget(self.create_continue_group())
        content_layout.addWidget(self.create_speech_group())
        content_layout.addWidget(self.create_autosave_group())
        content_layout.addStretch()

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(content_widget)

        return scroll_area

    def create_connection_group(self) -> QGroupBox:
        """Create the group for connection, UI, and language settings."""
        group = QGroupBox(self.txt("group_connection"))
        layout = QFormLayout()

        layout.addRow(
            self.txt("label_ollama_base_url"),
            self.ollama_base_url_input,
        )
        layout.addRow(
            self.txt("label_model_name"),
            self.model_name_input,
        )
        layout.addRow(
            self.txt("label_timeout"),
            self.timeout_input,
        )
        layout.addRow(
            self.txt("label_fake_mode"),
            self.fake_llm_checkbox,
        )
        layout.addRow(
            self.txt("label_show_command_input"),
            self.show_command_input_checkbox,
        )
        layout.addRow(
            self.txt("label_show_speech_result"),
            self.show_speech_result_checkbox,
        )
        layout.addRow(
            self.txt("label_interface_language"),
            self.interface_language_input,
        )
        layout.addRow(
            self.txt("label_text_generation_language"),
            self.text_generation_language_input,
        )
        layout.addRow("", self.test_ollama_button)

        group.setLayout(layout)
        return group

    def create_generate_group(self) -> QGroupBox:
        """Create the group for text generation parameters."""
        group = QGroupBox(self.txt("group_generation"))
        layout = QFormLayout()

        layout.addRow(
            self.txt("label_temperature"),
            self.generate_temperature_input,
        )
        layout.addRow(
            self.txt("label_max_response_length"),
            self.generate_num_predict_input,
        )

        group.setLayout(layout)
        return group

    def create_transform_group(self) -> QGroupBox:
        """Create the group for selected-text transformation parameters."""
        group = QGroupBox(self.txt("group_transform"))
        layout = QFormLayout()

        layout.addRow(
            self.txt("label_temperature"),
            self.transform_temperature_input,
        )
        layout.addRow(
            self.txt("label_max_response_length"),
            self.transform_num_predict_input,
        )

        group.setLayout(layout)
        return group

    def create_continue_group(self) -> QGroupBox:
        """Create the group for text continuation parameters."""
        group = QGroupBox(self.txt("group_continue"))
        layout = QFormLayout()

        layout.addRow(
            self.txt("label_temperature"),
            self.continue_temperature_input,
        )
        layout.addRow(
            self.txt("label_max_response_length"),
            self.continue_num_predict_input,
        )

        group.setLayout(layout)
        return group

    def create_speech_group(self) -> QGroupBox:
        """Create the group for speech recognition parameters."""
        group = QGroupBox(self.txt("group_speech"))
        layout = QFormLayout()

        layout.addRow(
            self.txt("label_whisper_model"),
            self.speech_model_size_input,
        )
        layout.addRow(
            self.txt("label_sample_rate"),
            self.speech_sample_rate_input,
        )
        layout.addRow(
            self.txt("label_device"),
            self.speech_device_input,
        )
        layout.addRow(
            self.txt("label_compute_type"),
            self.speech_compute_type_input,
        )
        layout.addRow(
            self.txt("label_beam_size"),
            self.speech_beam_size_input,
        )

        group.setLayout(layout)
        return group

    def create_autosave_group(self) -> QGroupBox:
        """Create the group for auto-save settings."""
        group = QGroupBox(self.txt("autosave_group"))
        layout = QFormLayout()

        layout.addRow(self.enable_autosave_checkbox)
        layout.addRow(
            self.txt("autosave_interval_seconds"),
            self.autosave_interval_input,
        )

        group.setLayout(layout)
        return group

    # Save handling ---------------------------------------------------------

    def save_and_accept(self) -> None:
        """
        Store all current widget values and close the dialogue.

        The parent window reloads the changed settings after the dialogue has
        been accepted.
        """
        self.settings["ollama_base_url"] = (
            self.ollama_base_url_input.text().strip()
        )
        self.settings["ollama_model_name"] = (
            self.model_name_input.text().strip()
        )
        self.settings["llm_timeout_seconds"] = self.timeout_input.value()
        self.settings["use_fake_llm"] = (
            self.fake_llm_checkbox.isChecked()
        )

        self.settings["show_command_input"] = (
            self.show_command_input_checkbox.isChecked()
        )
        self.settings["show_speech_result"] = (
            self.show_speech_result_checkbox.isChecked()
        )

        self.settings["interface_language"] = (
            self.interface_language_input.currentData()
        )
        self.settings["text_generation_language"] = (
            self.text_generation_language_input.currentData()
        )

        self.settings["generate_temperature"] = (
            self.generate_temperature_input.value()
        )
        self.settings["generate_num_predict"] = (
            self.generate_num_predict_input.value()
        )

        self.settings["transform_temperature"] = (
            self.transform_temperature_input.value()
        )
        self.settings["transform_num_predict"] = (
            self.transform_num_predict_input.value()
        )

        self.settings["continue_temperature"] = (
            self.continue_temperature_input.value()
        )
        self.settings["continue_num_predict"] = (
            self.continue_num_predict_input.value()
        )

        self.settings["speech_model_size"] = (
            self.speech_model_size_input.currentText()
        )
        self.settings["speech_sample_rate"] = (
            self.speech_sample_rate_input.value()
        )
        self.settings["speech_device"] = (
            self.speech_device_input.currentText()
        )
        self.settings["speech_compute_type"] = (
            self.speech_compute_type_input.currentText()
        )
        self.settings["speech_beam_size"] = (
            self.speech_beam_size_input.value()
        )

        self.settings["enable_autosave"] = (
            self.enable_autosave_checkbox.isChecked()
        )
        self.settings["autosave_interval_seconds"] = (
            self.autosave_interval_input.value()
        )

        save_settings(self.settings)
        self.accept()

    # Ollama test -----------------------------------------------------------

    def test_ollama_connection(self) -> None:
        """
        Test the configured Ollama endpoint and model name.

        This uses the values currently visible in the dialogue, not necessarily
        the values already saved in settings.json.
        """
        model_name = self.model_name_input.text().strip()
        base_url = self.ollama_base_url_input.text().strip()
        timeout = min(self.timeout_input.value(), 10)

        if not base_url:
            QMessageBox.warning(
                self,
                self.txt("ollama_test_title"),
                self.txt("ollama_base_url_missing"),
            )
            return

        if not model_name:
            QMessageBox.warning(
                self,
                self.txt("ollama_test_title"),
                self.txt("ollama_model_name_missing"),
            )
            return

        self.test_ollama_button.setEnabled(False)

        try:
            llm_client = LlmClient(
                model_name=model_name,
                base_url=base_url,
                timeout=timeout,
                use_fake_response=False,
            )

            status = llm_client.check_ollama_status()

            models_text = "\n".join(status["models"])

            if not models_text:
                models_text = self.txt("ollama_no_models_found")

            message = (
                f"{status['message']}\n\n"
                f"{self.txt('ollama_found_models')}\n"
                f"{models_text}"
            )

            if status["ok"]:
                QMessageBox.information(
                    self,
                    self.txt("ollama_test_title"),
                    message,
                )
            else:
                QMessageBox.warning(
                    self,
                    self.txt("ollama_test_title"),
                    message,
                )

        finally:
            self.test_ollama_button.setEnabled(True)

    # Reusable widget helpers ----------------------------------------------

    def create_language_combo_box(self, value: str) -> QComboBox:
        """Create a language combo box and select the given language code."""
        combo_box = QComboBox()
        combo_box.addItem(self.txt("language_german"), "de")
        combo_box.addItem(self.txt("language_english"), "en")

        self.set_combo_by_data(combo_box, value)

        return combo_box

    def create_temperature_input(self, value: float) -> QDoubleSpinBox:
        """Create a spin box for LLM temperature values."""
        input_box = QDoubleSpinBox()
        input_box.setRange(0.0, 2.0)
        input_box.setSingleStep(0.1)
        input_box.setDecimals(2)
        input_box.setValue(float(value))

        return input_box

    def create_num_predict_input(self, value: int) -> QSpinBox:
        """Create a spin box for maximum LLM response length."""
        input_box = QSpinBox()
        input_box.setRange(50, 4000)
        input_box.setSingleStep(50)
        input_box.setValue(int(value))
        input_box.setSuffix(self.txt("suffix_tokens"))

        return input_box

    def set_combo_by_data(
        self,
        combo_box: QComboBox,
        value: str,
        fallback_index: int = 0,
    ) -> None:
        """
        Select an item in a combo box by its stored data value.

        If the value is not available, the fallback index is selected instead.
        This protects the dialogue from invalid or outdated settings files.
        """
        index = combo_box.findData(value)

        if index < 0:
            index = fallback_index

        combo_box.setCurrentIndex(index)

    # Localization ----------------------------------------------------------

    def txt(self, key: str, **kwargs) -> str:
        """Return a localized settings-dialogue text."""
        return settings_text(key, **kwargs)
