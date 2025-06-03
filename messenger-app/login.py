from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox
from database import get_user_by_credentials, create_user
from messenger import MessengerUI
from database import init_db
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt, Signal
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent
DB_FILE = APP_DIR / "messages.db"
conn = init_db(DB_FILE) 


class ClickableLabel(QLabel):
    clicked = Signal()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()

    



class LoginWindow(QWidget):
    def open_register_window(self):
        self.register_window = RegisterWindow()
        self.register_window.show()
        self.hide()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Вход")
        self.setGeometry(400, 200, 800, 500)

        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        layout.addStretch(1)
        layout.addWidget(QLabel("Вход"), alignment=Qt.AlignCenter)
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Логин (с 3 до 16 символов)")
        self.username_input.setMaximumSize(400, 40)
        self.username_input.setMinimumSize(300, 40)
        self.username_input.setMaxLength(16)
        layout.addWidget(self.username_input, alignment=Qt.AlignCenter)


        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Пароль (c 8 до 16 символов)")
        self.password_input.setMaximumSize(400, 40)
        self.password_input.setMinimumSize(300, 40)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setMaxLength(16)
        layout.addWidget(self.password_input, alignment=Qt.AlignCenter)


        self.login_btn = QPushButton("Войти", self)
        self.login_btn.setMaximumWidth(400)
        self.login_btn.setMinimumWidth(300)
        
        self.register_link = ClickableLabel("Нет аккаунта? <u><span style='color:#007BFF;'>Зарегистрироваться</span></u>")
        self.register_link.setTextFormat(Qt.RichText)
        self.register_link.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.register_link.setCursor(Qt.PointingHandCursor)
        self.register_link.clicked.connect(self.open_register_window)
        layout.addWidget(self.login_btn, alignment=Qt.AlignCenter)
        layout.addWidget(self.register_link, alignment=Qt.AlignCenter)


        self.login_btn.clicked.connect(self.login)

        layout.addStretch(1)


# подключаешь сигнал

        layout.addWidget(self.register_link, alignment=Qt.AlignCenter)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if not username or not password:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля")
            return
        if len(self.username_input.text())<3:
            QMessageBox.warning(self, "Ошибка", "Логин должен быть больше 3 символов")
            return
        if len(self.password_input.text())<8:
            QMessageBox.warning(self, "Ошибка", "Пароль должен быть больше 8 символов")
            return

       

        user = get_user_by_credentials(conn, username, password)

        if user:
            self.hide()
            self.messenger = MessengerUI(current_user=username)
            self.messenger.show()
        else:
            QMessageBox.warning(self, "Ошибка", "Невреный логин или пароль")





class ClickableLabel(QLabel):
    clicked = Signal()
    def mousePressEvent(self, event):
        self.clicked.emit()

class RegisterWindow(QWidget):
    def open_login_window(self):
        self.login_window = LoginWindow()
        self.login_window.show()
        self.hide()
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Регистрация")
        self.setGeometry(400, 200, 800, 500)

        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        layout.addStretch(1)
        self.reg_username_input = QLineEdit(self)
        self.reg_username_input.setPlaceholderText("Логин (с 3 до 16 символов)")
        self.reg_username_input.setMaximumSize(400, 40)
        self.reg_username_input.setMinimumSize(300, 40)
        self.reg_username_input.setMaxLength(16)


        self.reg_password_input = QLineEdit(self)
        self.reg_password_input.setPlaceholderText("Пароль (c 8 до 16 символов)")
        self.reg_password_input.setMaximumSize(400, 40)
        self.reg_password_input.setMinimumSize(300, 40)
        self.reg_password_input.setEchoMode(QLineEdit.Password)
        self.reg_password_input.setMaxLength(16)

        self.register_button = QPushButton("Зарегистрироваться")
        self.register_button.setMaximumWidth(400)
        self.register_button.setMinimumWidth(300)
        self.register_button.clicked.connect(self.try_register)

        layout.addWidget(QLabel("Регистрация"), alignment=Qt.AlignCenter)
        layout.addWidget(self.reg_username_input, alignment=Qt.AlignCenter)
        layout.addWidget(self.reg_password_input, alignment=Qt.AlignCenter)
        layout.addWidget(self.register_button, alignment=Qt.AlignCenter)

        self.login_link = ClickableLabel("Есть аккаунт? <u><span style='color:#007BFF;'>Войти</span></u>")
        self.login_link.setTextFormat(Qt.RichText)
        self.login_link.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.login_link.setCursor(Qt.PointingHandCursor)
        self.login_link.clicked.connect(self.open_login_window)
        
        layout.addStretch(1)
        layout.addWidget(self.login_link, alignment=Qt.AlignCenter)
    def try_register(self):
        username = self.reg_username_input.text()
        password = self.reg_password_input.text()
        if not username or not password:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля")
            return
        if len(self.reg_username_input.text())<3:
            QMessageBox.warning(self, "Ошибка", "Логин должен быть больше 3 символов")
            return
        if len(self.reg_password_input.text())<8:
            QMessageBox.warning(self, "Ошибка", "Пароль должен быть больше 8 символов")
            return


        result = create_user(conn, username, password)
        if result:
            QMessageBox.information(self, "Успех", "Регистрация прошла успешно!")
            self.login_window = LoginWindow()
            self.login_window.show()
            self.close()
        else:
            QMessageBox.warning(self, "Ошибка", "Пользователь уже существует")


    def try_login(self):
        username = self.username_input.text()
        password = self.password_input.text()


        user = get_user_by_credentials(username, password)
        if user:
            QMessageBox.information(self, "Успех", f"Добро пожаловать, {username}!")
        else:
            QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль")


