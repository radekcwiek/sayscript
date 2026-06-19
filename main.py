# SPDX-License-Identifier: Apache-2.0

"""
Application entry point for SayScript.

This module starts logging, creates the Qt application object, opens the main
editor window, and then hands control to Qt's event loop.
"""

import multiprocessing
import sys


def main() -> None:
    """
    Start the SayScript desktop application.

    Imports that initialize Qt, faster-whisper, or other heavy libraries happen
    inside this function. This keeps PyInstaller's multiprocessing bootstrap
    path as clean as possible.
    """
    from PySide6.QtWidgets import QApplication

    from app.logging_setup import setup_logging
    from app.main_window import MiniEditor

    logger = setup_logging()
    logger.info("Application starting")

    app = QApplication(sys.argv)

    window = MiniEditor()
    window.show()

    logger.info("Main window shown")

    sys.exit(app.exec())


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
