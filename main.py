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
import os
from datetime import datetime

# admin
from login import LoginScreen, CreateAccountScreen
from admin.admin_home import AdminHomeScreen
from admin.admin_pesan import AdminPesanScreen
from admin.admin_detail_pesan import AdminDetailPesanScreen
from admin.admin_pengaduan import AdminPengaduanScreen
from admin.admin_daftar import AdminDaftarScreen
from admin.admin_arsip import AdminArsipScreen
from admin.admin_profil import AdminProfilScreen
from admin.daftar_user import DaftarUserScreen 

from users.home import HomeScreen
from users.pesan import PesanScreen
from users.detailpesan import DetailPesanScreen
from users.pengaduan import PengaduanScreen
from users.masukan import MasukanScreen
from users.status import StatusScreen
from users.profil import ProfilScreen

# Load .kv files
Builder.load_file('login.kv')
Builder.load_file('users/home.kv')
Builder.load_file('users/pesan.kv')
Builder.load_file('users/pengaduan.kv')
Builder.load_file('users/profil.kv')
Builder.load_file('users/masukan.kv')
Builder.load_file('users/status.kv')
Builder.load_file('users/detailpesan.kv')
Builder.load_file('admin/admin_home.kv')
Builder.load_file('admin/admin_profil.kv')
Builder.load_file('admin/admin_pesan.kv')
Builder.load_file('admin/admin_detail_pesan.kv')
Builder.load_file('admin/admin_pengaduan.kv')
Builder.load_file('admin/admin_daftar.kv')
Builder.load_file('admin/admin_arsip.kv')
Builder.load_file('admin/daftar_user.kv') 

# Define Custom Screen Manager to handle current_user_id
class CustomScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_user_id = None

    def set_current_user_id(self, user_id):
        self.current_user_id = user_id

    def get_current_user_id(self):
        return self.current_user_id

class RiwayatScreen(Screen):
    pass

class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_user_id = None

    def set_current_user_id(self, username):
        self.current_user_id = username

    def get_current_user_id(self):
        return self.current_user_id

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"

        sm = CustomScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(CreateAccountScreen(name='create_account'))

        # Admin screens
        sm.add_widget(AdminHomeScreen(name='admin_home'))
        sm.add_widget(AdminPesanScreen(name='admin_pesan'))
        sm.add_widget(AdminDetailPesanScreen(name='admin_detail_pesan'))
        sm.add_widget(AdminProfilScreen(name='admin_profil'))
        sm.add_widget(AdminPengaduanScreen(name='admin_pengaduan'))
        sm.add_widget(AdminDaftarScreen(name='admin_daftar'))
        sm.add_widget(AdminArsipScreen(name='admin_arsip'))
        sm.add_widget(DaftarUserScreen(name='daftar_user'))

        # User screens
        sm.add_widget(HomeScreen(name='users_home'))
        sm.add_widget(PesanScreen(name='pesan'))
        sm.add_widget(PengaduanScreen(name='pengaduan'))
        sm.add_widget(ProfilScreen(name='profil'))
        sm.add_widget(MasukanScreen(name='masukan'))
        sm.add_widget(StatusScreen(name='status'))
        sm.add_widget(DetailPesanScreen(name='detailpesan'))

        return sm

if __name__ == "__main__":
    Window.size = (360, 640)
    MainApp().run()
