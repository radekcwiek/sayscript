from PySide6.QtWidgets import (
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFormLayout,
    QGroupBox,
    QLineEdit,
    QSpinBox,
    QVBoxLayout,
)

from app.settings import load_settings, save_settings


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Einstellungen")
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
        self.timeout_input.setSuffix(" Sekunden")

        self.fake_llm_checkbox = QCheckBox()
        self.fake_llm_checkbox.setChecked(
            bool(self.settings["use_fake_llm"])
        )

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

        connection_group = QGroupBox("Verbindung")
        connection_layout = QFormLayout()
        connection_layout.addRow("Ollama-Adresse:", self.ollama_base_url_input)
        connection_layout.addRow("Modellname:", self.model_name_input)
        connection_layout.addRow("Timeout:", self.timeout_input)
        connection_layout.addRow("Fake-Modus:", self.fake_llm_checkbox)
        connection_group.setLayout(connection_layout)

        generate_group = QGroupBox("Generierung")
        generate_layout = QFormLayout()
        generate_layout.addRow("Temperature:", self.generate_temperature_input)
        generate_layout.addRow("Max. Antwortlänge:", self.generate_num_predict_input)
        generate_group.setLayout(generate_layout)

        transform_group = QGroupBox("Transformation")
        transform_layout = QFormLayout()
        transform_layout.addRow("Temperature:", self.transform_temperature_input)
        transform_layout.addRow("Max. Antwortlänge:", self.transform_num_predict_input)
        transform_group.setLayout(transform_layout)

        continue_group = QGroupBox("Fortsetzung")
        continue_layout = QFormLayout()
        continue_layout.addRow("Temperature:", self.continue_temperature_input)
        continue_layout.addRow("Max. Antwortlänge:", self.continue_num_predict_input)
        continue_group.setLayout(continue_layout)

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
        layout.addWidget(self.button_box)

        self.setLayout(layout)


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
        input_box.setSuffix(" Tokens")
        return input_box
