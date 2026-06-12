from PySide6.QtWidgets import (
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFormLayout,
    QGroupBox,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QComboBox,
)

from app.settings import load_settings, save_settings
from app.llm_client import LlmClient
from app.localization import settings_text


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle(self.txt("title"))
        self.setMinimumWidth(420)

        self.settings = load_settings()

        self.ollama_base_url_input = QLineEdit()
        self.ollama_base_url_input.setText(
            self.settings["ollama_base_url"]
        )

        self.model_name_input = QLineEdit()
        self.model_name_input.setText(
            self.settings["ollama_model_name"]
        )

        self.timeout_input = QSpinBox()
        self.timeout_input.setRange(10, 3600)
        self.timeout_input.setValue(
            int(self.settings["llm_timeout_seconds"])
        )
        self.timeout_input.setSuffix(self.txt("suffix_seconds"))

        self.fake_llm_checkbox = QCheckBox()
        self.fake_llm_checkbox.setChecked(
            bool(self.settings["use_fake_llm"])
        )

        self.show_command_input_checkbox = QCheckBox()
        self.show_command_input_checkbox.setChecked(
            bool(self.settings["show_command_input"])
        )
        self.show_command_input_checkbox.setToolTip(
            self.txt("tooltip_show_command_input")
        )

        self.interface_language_input = QComboBox()
        self.interface_language_input.addItem(self.txt("language_german"), "de")
        self.interface_language_input.addItem(self.txt("language_english"), "en")
        self.interface_language_input.setCurrentIndex(
            self.interface_language_input.findData(
                self.settings["interface_language"]
            )
        )
        self.interface_language_input.setToolTip(
            self.txt("tooltip_interface_language")
        )

        self.text_generation_language_input = QComboBox()
        self.text_generation_language_input.addItem(self.txt("language_german"), "de")
        self.text_generation_language_input.addItem(self.txt("language_english"), "en")
        self.text_generation_language_input.setCurrentIndex(
            self.text_generation_language_input.findData(
                self.settings["text_generation_language"]
            )
        )
        self.text_generation_language_input.setToolTip(
            self.txt("tooltip_text_generation_language")
        )

        self.interface_language_input = QComboBox()
        self.interface_language_input.addItem(self.txt("language_german"), "de")
        self.interface_language_input.addItem(self.txt("language_english"), "en")
        self.set_combo_by_data(
            self.interface_language_input,
            self.settings["interface_language"],
        )
        self.interface_language_input.setToolTip(
            self.txt("tooltip_interface_language")
        )

        self.text_generation_language_input = QComboBox()
        self.text_generation_language_input.addItem(self.txt("language_german"), "de")
        self.text_generation_language_input.addItem(self.txt("language_english"), "en")
        self.set_combo_by_data(
            self.text_generation_language_input,
            self.settings["text_generation_language"],
        )
        self.text_generation_language_input.setToolTip(
            self.txt("tooltip_text_generation_language")
        )

        self.ollama_base_url_input.setToolTip(self.txt("tooltip_ollama_base_url"))
        self.model_name_input.setToolTip(self.txt("tooltip_model_name"))
        self.timeout_input.setToolTip(self.txt("tooltip_timeout"))
        self.fake_llm_checkbox.setToolTip(self.txt("tooltip_fake_mode"))

        self.generate_temperature_input = self.create_temperature_input(
            self.settings["generate_temperature"]
        )
        self.generate_num_predict_input = self.create_num_predict_input(
            self.settings["generate_num_predict"]
        )

        self.transform_temperature_input = self.create_temperature_input(
            self.settings["transform_temperature"]
        )
        self.transform_num_predict_input = self.create_num_predict_input(
            self.settings["transform_num_predict"]
        )

        self.continue_temperature_input = self.create_temperature_input(
            self.settings["continue_temperature"]
        )
        self.continue_num_predict_input = self.create_num_predict_input(
            self.settings["continue_num_predict"]
        )

        self.speech_model_size_input = QComboBox()
        self.speech_model_size_input.addItems(["tiny", "base", "small", "medium", "large-v3"])
        self.speech_model_size_input.setCurrentText(
            self.settings["speech_model_size"]
        )

        self.speech_sample_rate_input = QSpinBox()
        self.speech_sample_rate_input.setRange(8000, 48000)
        self.speech_sample_rate_input.setSingleStep(1000)
        self.speech_sample_rate_input.setValue(
            int(self.settings["speech_sample_rate"])
        )
        self.speech_sample_rate_input.setSuffix(self.txt("suffix_hz"))

        self.speech_device_input = QComboBox()
        self.speech_device_input.addItems(["cpu", "cuda"])
        self.speech_device_input.setCurrentText(
            self.settings["speech_device"]
        )

        self.speech_compute_type_input = QComboBox()
        self.speech_compute_type_input.addItems(["int8", "float32", "float16"])
        self.speech_compute_type_input.setCurrentText(
            self.settings["speech_compute_type"]
        )

        self.speech_beam_size_input = QSpinBox()
        self.speech_beam_size_input.setRange(1, 20)
        self.speech_beam_size_input.setValue(
            int(self.settings["speech_beam_size"])
        )

        temperature_tooltip = self.txt("tooltip_temperature")
        num_predict_tooltip = self.txt("tooltip_num_predict")

        self.speech_model_size_input.setToolTip(self.txt("tooltip_speech_model_size"))
        self.speech_sample_rate_input.setToolTip(self.txt("tooltip_speech_sample_rate"))
        self.speech_device_input.setToolTip(self.txt("tooltip_speech_device"))
        self.speech_compute_type_input.setToolTip(self.txt("tooltip_speech_compute_type"))
        self.speech_beam_size_input.setToolTip(self.txt("tooltip_speech_beam_size"))

        self.generate_temperature_input.setToolTip(temperature_tooltip)
        self.transform_temperature_input.setToolTip(temperature_tooltip)
        self.continue_temperature_input.setToolTip(temperature_tooltip)

        self.generate_num_predict_input.setToolTip(num_predict_tooltip)
        self.transform_num_predict_input.setToolTip(num_predict_tooltip)
        self.continue_num_predict_input.setToolTip(num_predict_tooltip)

        self.test_ollama_button = QPushButton(self.txt("button_test_ollama"))
        self.test_ollama_button.clicked.connect(self.test_ollama_connection)
        self.test_ollama_button.setToolTip(self.txt("tooltip_test_ollama"))

        connection_group = QGroupBox(self.txt("group_connection"))
        connection_layout = QFormLayout()

        connection_layout.addRow(self.txt("label_ollama_base_url"), self.ollama_base_url_input)
        connection_layout.addRow(self.txt("label_model_name"), self.model_name_input)
        connection_layout.addRow(self.txt("label_timeout"), self.timeout_input)
        connection_layout.addRow(self.txt("label_fake_mode"), self.fake_llm_checkbox)
        connection_layout.addRow(self.txt("label_show_command_input"), self.show_command_input_checkbox)
        connection_layout.addRow(self.txt("label_interface_language"), self.interface_language_input)
        connection_layout.addRow(self.txt("label_text_generation_language"), self.text_generation_language_input)
        connection_layout.addRow("", self.test_ollama_button)

        connection_group.setLayout(connection_layout)

        generate_group = QGroupBox(self.txt("group_generation"))
        generate_layout = QFormLayout()
        generate_layout.addRow(self.txt("label_temperature"), self.generate_temperature_input)
        generate_layout.addRow(self.txt("label_max_response_length"), self.generate_num_predict_input)
        generate_group.setLayout(generate_layout)

        transform_group = QGroupBox(self.txt("group_transform"))
        transform_layout = QFormLayout()
        transform_layout.addRow(self.txt("label_temperature"), self.transform_temperature_input)
        transform_layout.addRow(self.txt("label_max_response_length"), self.transform_num_predict_input)
        transform_group.setLayout(transform_layout)

        continue_group = QGroupBox(self.txt("group_continue"))
        continue_layout = QFormLayout()
        continue_layout.addRow(self.txt("label_temperature"), self.continue_temperature_input)
        continue_layout.addRow(self.txt("label_max_response_length"), self.continue_num_predict_input)
        continue_group.setLayout(continue_layout)

        speech_group = QGroupBox(self.txt("group_speech"))
        speech_layout = QFormLayout()
        speech_layout.addRow(self.txt("label_whisper_model"), self.speech_model_size_input)
        speech_layout.addRow(self.txt("label_sample_rate"), self.speech_sample_rate_input)
        speech_layout.addRow(self.txt("label_device"), self.speech_device_input)
        speech_layout.addRow(self.txt("label_compute_type"), self.speech_compute_type_input)
        speech_layout.addRow(self.txt("label_beam_size"), self.speech_beam_size_input)
        speech_group.setLayout(speech_layout)

        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
        )
        self.button_box.accepted.connect(self.save_and_accept)
        self.button_box.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addWidget(connection_group)
        layout.addWidget(generate_group)
        layout.addWidget(transform_group)
        layout.addWidget(continue_group)
        layout.addWidget(speech_group)
        layout.addWidget(self.button_box)

        self.setLayout(layout)


    def txt(self, key: str, **kwargs) -> str:
        return settings_text(key, **kwargs)


    def save_and_accept(self) -> None:
        self.settings["ollama_base_url"] = self.ollama_base_url_input.text().strip()
        self.settings["ollama_model_name"] = self.model_name_input.text().strip()
        self.settings["llm_timeout_seconds"] = self.timeout_input.value()
        self.settings["use_fake_llm"] = self.fake_llm_checkbox.isChecked()

        self.settings["generate_temperature"] = self.generate_temperature_input.value()
        self.settings["generate_num_predict"] = self.generate_num_predict_input.value()

        self.settings["transform_temperature"] = self.transform_temperature_input.value()
        self.settings["transform_num_predict"] = self.transform_num_predict_input.value()

        self.settings["continue_temperature"] = self.continue_temperature_input.value()
        self.settings["continue_num_predict"] = self.continue_num_predict_input.value()

        self.settings["speech_model_size"] = self.speech_model_size_input.currentText()
        self.settings["speech_sample_rate"] = self.speech_sample_rate_input.value()
        self.settings["speech_device"] = self.speech_device_input.currentText()
        self.settings["speech_compute_type"] = self.speech_compute_type_input.currentText()
        self.settings["speech_beam_size"] = self.speech_beam_size_input.value()
        self.settings["show_command_input"] = self.show_command_input_checkbox.isChecked()

        self.settings["interface_language"] = (
            self.interface_language_input.currentData()
        )
        self.settings["text_generation_language"] = (
            self.text_generation_language_input.currentData()
        )

        save_settings(self.settings)
        self.accept()


    def create_temperature_input(self, value: float) -> QDoubleSpinBox:
        input_box = QDoubleSpinBox()
        input_box.setRange(0.0, 2.0)
        input_box.setSingleStep(0.1)
        input_box.setDecimals(2)
        input_box.setValue(float(value))
        return input_box


    def create_num_predict_input(self, value: int) -> QSpinBox:
        input_box = QSpinBox()
        input_box.setRange(50, 4000)
        input_box.setSingleStep(50)
        input_box.setValue(int(value))
        input_box.setSuffix(self.txt("suffix_tokens"))
        return input_box


    def test_ollama_connection(self) -> None:
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


    def set_combo_by_data(
        self,
        combo_box: QComboBox,
        value: str,
        fallback_index: int = 0,
    ) -> None:
        index = combo_box.findData(value)

        if index < 0:
            index = fallback_index

        combo_box.setCurrentIndex(index)
