from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDIconButton
from database import Database
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

class PengaduanScreen(Screen):
    user_id = ""  # Menyimpan user_id pengguna saat ini
    pengaduan_data = []  # List untuk menyimpan data pengaduan

    def on_enter(self):
        app = MDApp.get_running_app()
        username = app.get_current_user_id()  # Ambil username dari aplikasi
        self.ids['greeting_label'].text = f"Halo {username}"  # Update label

    def add_pengaduan(self, pengaduan):
        self.pengaduan_data.append(pengaduan)

class MasukanScreen(Screen):
    pass