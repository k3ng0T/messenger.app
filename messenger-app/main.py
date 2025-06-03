import sys
from PySide6.QtWidgets import QApplication
from login import LoginWindow
from database import init_db
from pathlib import Path


APP_DIR = Path(__file__).resolve().parent
DB_FILE = APP_DIR / "messages.db"
conn = init_db(DB_FILE)




if __name__ == "__main__":
    app = QApplication(sys.argv)

    with open("messenger-app\style.qss", "r") as f:
        app.setStyleSheet(f.read())


    window = LoginWindow()
    window.show()
    sys.exit(app.exec())
