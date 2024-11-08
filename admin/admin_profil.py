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

class AdminProfilScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.file_manager = MDFileManager(
            exit_manager=self.exit_file_manager,
            select_path=self.select_file,
        )

    def open_file_chooser(self):
        self.file_manager.show('/')  # Tampilkan pemilih file

    def select_file(self, path):
        self.ids.profile_image.source = path  # Update gambar profil dengan path yang dipilih
        print(f"File yang dipilih: {path}")  # Debug print
        self.exit_file_manager()  # Tutup file manager

        # Simpan path gambar ke database
        app = MDApp.get_running_app()
        username = app.get_current_user_id()  # Menggunakan metode baru

        # Ambil data pengguna saat ini
        existing_user_data = Database.get_user(username)

        if existing_user_data:
            # Gabungkan data yang sudah ada dengan path gambar yang baru
            existing_user_data['profile_image'] = path  # Update hanya field profile_image

            # Simpan kembali data pengguna ke database
            try:
                Database.update_user(username, existing_user_data)  # Pastikan Anda memiliki metode ini
            except Exception as e:
                print(f"Gagal memperbarui gambar profil: {e}")

    def exit_file_manager(self, *args):
        self.file_manager.close()  # Tutup file manager

    def on_enter(self):
        self.load_user_data()  # Panggil fungsi untuk memuat data pengguna saat layar dibuka

    def load_user_data(self):
        app = MDApp.get_running_app()
        username = app.get_current_user_id()  # Ambil current_user_id

        # Ambil data pengguna dari database
        user_data = Database.get_user(username)
        if user_data:
            # Isi TextField dengan data pengguna
            self.ids.username_field.text = user_data.get('username', '')
            self.ids.nik_field.text = user_data.get('nik', '')
            self.ids.alamat_field.text = user_data.get('address', '')
            self.ids.password_field.text = user_data.get('password', '')
            self.ids.profile_image.source = user_data.get('profile_image', 'assets/image/profile.png')  # Gambar default

    def update_profile(self):
        app = MDApp.get_running_app()
        username = app.get_current_user_id()  # Ambil current_user_id

        # Ambil data dari TextField
        updated_data = {
            'nik': self.ids.nik_field.text,
            'address': self.ids.alamat_field.text,
            'password': self.ids.password_field.text,
            'profile_image': self.ids.profile_image.source
        }

        # Ambil data pengguna saat ini untuk memastikan tidak ada data yang hilang
        existing_user_data = Database.get_user(username)

        if existing_user_data:
            # Gabungkan data yang sudah ada dengan data yang baru
            updated_data = {**existing_user_data, **updated_data}  # Menggabungkan dictionary

        # Simpan data yang diperbarui ke database
        try:
            Database.update_user(username, updated_data)  # Panggil metode untuk memperbarui pengguna
            self.show_dialog("Profil berhasil diperbarui!")
        except Exception as e:
            self.show_dialog(f"Gagal memperbarui profil: {e}")

    def show_dialog(self, message):
        dialog = MDDialog(
            title="Informasi",
            text=message,
            buttons=[
                MDFlatButton(text="OK", on_release=lambda x: dialog.dismiss())
            ],
        )
        dialog.open()
