from PySide6.QtWidgets import (
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
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

        form_layout = QFormLayout()
        form_layout.addRow("Ollama-Adresse:", self.ollama_base_url_input)
        form_layout.addRow("Modellname:", self.model_name_input)
        form_layout.addRow("Timeout:", self.timeout_input)
        form_layout.addRow("Fake-Modus:", self.fake_llm_checkbox)

        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
        )
        self.button_box.accepted.connect(self.save_and_accept)
        self.button_box.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addLayout(form_layout)
        layout.addWidget(self.button_box)

        self.setLayout(layout)

    def save_and_accept(self) -> None:
        self.settings["ollama_base_url"] = self.ollama_base_url_input.text().strip()
        self.settings["ollama_model_name"] = self.model_name_input.text().strip()
        self.settings["llm_timeout_seconds"] = self.timeout_input.value()
        self.settings["use_fake_llm"] = self.fake_llm_checkbox.isChecked()

        save_settings(self.settings)
        self.accept()
