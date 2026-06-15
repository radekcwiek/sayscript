import sys

from PySide6.QtWidgets import QApplication

from app.logging_setup import setup_logging
from app.main_window import MiniEditor


def main():
    logger = setup_logging()
    logger.info("Application starting")

    app = QApplication(sys.argv)
    window = MiniEditor()
    window.show()

    logger.info("Main window shown")
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
