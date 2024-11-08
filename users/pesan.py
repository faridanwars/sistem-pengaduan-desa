from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDIconButton
from database import Database
from users.pengaduan import MasukanScreen, PengaduanScreen
from kivymd.uix.filemanager import MDFileManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.metrics import dp
from kivymd.uix.list import OneLineAvatarIconListItem, ILeftBody, IRightBodyTouch
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivy.uix.image import Image as KivyImage
from kivymd.uix.list import OneLineListItem
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import os
from datetime import datetime

class PesanScreen(Screen):
    pass

class DetailPesanScreen(Screen):
    def on_enter(self):
        user_id = MDApp.get_running_app().get_current_user_id()  # Menggunakan MDApp untuk mendapatkan ID
        self.load_messages(user_id)

    def load_messages(self, user_id):
        messages = Database.get_messages(user_id)
        self.ids.message_container.clear_widgets()

        for message_id, message in messages:
            self.add_message_widget(message['message'], message['timestamp'], is_received=True)

    def add_message_widget(self, message_text, timestamp, is_received):
        message_layout = MDBoxLayout(adaptive_height=True, padding=dp(10))
        message_label = MDLabel(
            text=message_text, 
            theme_text_color="Custom", 
            text_color=(0, 0, 0, 1) if is_received else (1, 1, 1, 1)
        )

        if is_received:
            message_layout.md_bg_color = MDApp.get_running_app().theme_cls.bg_light
        else:
            message_layout.md_bg_color = MDApp.get_running_app().theme_cls.bg_dark
            message_layout.pos_hint = {"right": 1}

        message_layout.add_widget(message_label)
        message_layout.add_widget(MDLabel(
            text=timestamp, 
            font_style="Caption", 
            halign='right', 
            theme_text_color="Hint"
        ))
        self.ids.message_container.add_widget(message_layout)

    def send_message(self):
        user_id = MDApp.get_running_app().get_current_user_id()
        message_text = self.ids.message_input.text
        
        # Mengambil waktu saat ini dan memformatnya
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Format: YYYY-MM-DD HH:MM:SS

        if message_text:
            message_data = {
                "message": message_text,
                "timestamp": timestamp
            }
            Database.send_message(user_id, message_data)
            self.add_message_widget(message_text, timestamp, is_received=False)
            self.ids.message_input.text = ""
