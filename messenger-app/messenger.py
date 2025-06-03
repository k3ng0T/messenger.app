from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QLineEdit, QPushButton, 
    QLabel, QStackedWidget, QMessageBox, QInputDialog
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QPixmap
from database import init_db, get_all_chats, add_chat
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent
ICON_DIR = APP_DIR / "icon"
DB_FILE = APP_DIR / "messages.db"







# ===== ЧАТ =====
class ChatWidget(QWidget):
    def __init__(self, db_conn, chat_name, main_window):
        super().__init__()
        self.chat_name = chat_name
        self.db = init_db(DB_FILE)
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        self.message_list = QListWidget()
        layout.addWidget(self.message_list)

        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setFixedHeight(40)
        self.input_field.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.input_field)

        self.send_button = QPushButton("➤")
        self.send_button.setFixedWidth(50)
        self.send_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_button)

        layout.addLayout(input_layout)

    def load_messages(self):
        self.message_list.clear()
        cursor = self.db.cursor()
        cursor.execute("SELECT content FROM messages WHERE chat=? ORDER BY timestamp ASC", (self.chat_name,))
        for row in cursor.fetchall():
            self.message_list.addItem(row[0])

    def send_message(self):
        text = self.input_field.text().strip()
        if text:
            cursor = self.db.cursor()
            cursor.execute(
                "INSERT INTO messages (chat, content) VALUES (?, ?)",
                (self.chat_name, f"{self.main_window.current_user}: {text}")
            )
            self.db.commit()
            self.input_field.clear()
            self.load_messages()

# ===== ПРОФИЛЬ =====
class ProfileWidget(QWidget):
    def __init__(self, username):
        super().__init__()
        layout = QVBoxLayout(self)
        self.user = QLabel(f"Имя пользователя: {username}")
        """label = QLabel(self)
        pixmap = QPixmap(ICON_DIR / "default_profile.png")
        pixmap = pixmap.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        label.setPixmap(pixmap)"""
        self.user.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.user)
        layout.addStretch(1)

# ===== ГЛАВНОЕ ОКНО =====
class MessengerUI(QWidget):
    def __init__(self, current_user):
        super().__init__()
        self.current_user = current_user
        self.setWindowTitle("🔥 Мессенджер")
        self.setMinimumSize(900, 600)

        self.db = init_db(DB_FILE)
        self.chat_widgets = {}

        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout(self)
        left_panel = QVBoxLayout()

        # Кнопка "Создать чат"
        self.create_button = QPushButton("Создать чат")
        self.create_button.clicked.connect(self.create_chat)
        left_panel.addWidget(self.create_button)

        # Список чатов
        self.chat_list = QListWidget()
        self.chat_list.currentTextChanged.connect(self.switch_chat)
        left_panel.addWidget(self.chat_list, stretch=1)

        # Кнопки внизу: Чаты / Профиль
        bottom_buttons = QHBoxLayout()
        self.btn_chats = QPushButton("")
        self.btn_profile = QPushButton("")
        self.btn_chats.setIcon(QIcon(str(ICON_DIR/'chat.png')))
        self.btn_profile.setIcon(QIcon(str(ICON_DIR/"user.png")))
        self.btn_chats.setIconSize(QSize(50, 50))
        self.btn_profile.setIconSize(QSize(50, 50))
        bottom_buttons.addWidget(self.btn_chats)
        bottom_buttons.addWidget(self.btn_profile)

        self.btn_chats.clicked.connect(self.show_current_chat)
        self.btn_profile.clicked.connect(self.show_profile)

        left_panel.addLayout(bottom_buttons)
        main_layout.addLayout(left_panel, 1)

        # Центральная часть — переключение виджетов
        self.stack = QStackedWidget()
        self.profile_widget = ProfileWidget(self.current_user)
        self.stack.addWidget(self.profile_widget)

        self.chat_names = get_all_chats(self.db)
        if not self.chat_names:
            add_chat(self.db, "Общий чат")
            self.chat_names = ["Общий чат"]

        for chat_name in self.chat_names:
            self.add_chat_widget(chat_name)

        main_layout.addWidget(self.stack, 3)

        # Выбор первого чата
        self.chat_list.addItems(self.chat_names)
        self.chat_list.setCurrentRow(0)
        self.show_current_chat()

    def add_chat_widget(self, name):
        chat = ChatWidget(self.db, name, self)
        self.chat_widgets[name] = chat
        self.stack.insertWidget(self.stack.count() - 1, chat)  # перед профилем

    def switch_chat(self, name):
        if name in self.chat_widgets:
            self.stack.setCurrentWidget(self.chat_widgets[name])
            self.chat_widgets[name].load_messages()

    def show_current_chat(self):
        current = self.chat_list.currentItem()
        if current:
            self.switch_chat(current.text())

    def show_profile(self):
        self.stack.setCurrentWidget(self.profile_widget)

    def create_chat(self):
        name, ok = QInputDialog.getText(self, "Создать чат", "Имя нового чата:")
        if ok and name.strip():
            if name in self.chat_names:
                QMessageBox.warning(self, "Ошибка", "Такой чат уже есть.")
                return

            if add_chat(name):
                self.chat_names.append(name)
                self.chat_list.addItem(name)
                self.add_chat_widget(name)
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось создать чат.")
