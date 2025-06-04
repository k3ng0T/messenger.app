import sys
from PySide6.QtWidgets import QApplication
from ui.login import LoginWindow
from db.database import init_db
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent
STYLE_FILE = APP_DIR / "ui" / "style.qss"



if __name__ == "__main__":
    app = QApplication(sys.argv)

    with open(STYLE_FILE, "r", encoding="utf-8") as f:
        app.setStyleSheet(f.read())


    window = LoginWindow()
    window.show()
    sys.exit(app.exec())
