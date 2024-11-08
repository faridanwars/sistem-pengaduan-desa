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
from storage import StorageManager
import os
from datetime import datetime

class MasukanScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.file_manager = MDFileManager(
            exit_manager=self.exit_file_manager,
            select_path=self.select_file,
        )

    def open_file_chooser(self):
        self.file_manager.show('/')  # Atur direktori awal

    def select_file(self, path):
        self.ids.gambar_field.text = path  # Memperbarui text field dengan path yang dipilih
        print(f"File yang dipilih: {path}")  # Debug print
        self.exit_file_manager()  # Tutup file manager

    def exit_file_manager(self, *args):
        self.file_manager.close()  # Menggunakan close untuk menutup file manager

    def save_pengaduan(self):
        judul = self.ids.judul_field.text
        alamat = self.ids.alamat_field.text
        deskripsi = self.ids.deskripsi_field.text
        gambar = self.ids.gambar_field.text

        app = MDApp.get_running_app()
        username = app.current_user_id

        # Memastikan pengguna terdaftar
        user_data = Database.get_user(username)
        if user_data is None:
            self.show_dialog("Pengguna tidak terdaftar.")
            return

        pengaduan_data = {
            'judul': judul,
            'alamat': alamat,
            'deskripsi': deskripsi,
            'gambar': gambar
        }

        try:
            # Upload gambar ke Firebase Storage
            upload_response = StorageManager.upload_image(gambar)  # Mengupload gambar
            if upload_response['status'] == 'success':
                pengaduan_data['gambar'] = upload_response['url']  # Mengupdate URL gambar
            else:
                self.show_dialog("Gagal mengupload gambar.")  # Menangani kesalahan upload

            # Menyimpan pengaduan ke database
            Database.add_user_pengaduan(username, pengaduan_data)
            self.show_dialog("Pengaduan berhasil disimpan!")
        except Exception as e:
            self.show_dialog(f"Terjadi kesalahan: {str(e)}")

        # Reset text fields
        self.ids.judul_field.text = ""
        self.ids.alamat_field.text = ""
        self.ids.deskripsi_field.text = ""
        self.ids.gambar_field.text = ""

    def show_dialog(self, message):
        dialog = MDDialog(
            title="Informasi",
            text=message,
            buttons=[
                MDFlatButton(text="Tutup", on_release=lambda x: self.close_dialog(dialog))  # Memanggil close_dialog
            ],
        )
        dialog.open()

    def close_dialog(self, dialog):
        dialog.dismiss()  # Tutup dialog
        # Arahkan ke StatusScreen
        app = MDApp.get_running_app()
        app.root.current = 'status'  # Pastikan 'status' adalah nama layar yang benar