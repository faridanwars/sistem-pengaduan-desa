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

class AdminHomeScreen(Screen):
    def on_enter(self):
        """Method yang dipanggil saat layar AdminHomeScreen ditampilkan."""
        user_count = Database.get_user_count()  # Mengambil jumlah pengguna dari database
        self.ids.user_count_label.text = str(user_count)  # Memperbarui label dengan jumlah pengguna

class MyApp(MDApp):
    def build(self):
        self.root = Builder.load_file('admin_home.kv')  # Ganti dengan nama file Kivy Anda
        return self.root