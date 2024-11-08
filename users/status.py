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

class StatusScreen(Screen):
    def on_enter(self):
        self.update_status()

    def update_status(self):
        app = MDApp.get_running_app()
        username = app.get_current_user_id()
        print(f"Mencari pengaduan untuk pengguna: {username}")  # Debugging

        # Ambil pengaduan dari database
        pengaduan_list = Database.get_pengaduan(username)
        print("Pengaduan List:", pengaduan_list)  # Debugging
        self.display_pengaduan(pengaduan_list)  # Pastikan metode ini ada

    def display_pengaduan(self, pengaduan_list):
        self.ids.status_layout.clear_widgets()  # Kosongkan layout sebelumnya
        for index, (pengaduan_id, pengaduan) in enumerate(pengaduan_list, start=1):  # Menggunakan enumerate pada list
            # Pastikan pengaduan adalah dictionary dan memiliki kunci 'judul'
            if isinstance(pengaduan, dict) and 'judul' in pengaduan:
                # Buat BoxLayout untuk setiap pengaduan
                pengaduan_box = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))

                # Label untuk judul pengaduan
                title_label = MDLabel(text=f"{index}. {pengaduan['judul']}", size_hint_x=0.6)

                # Ikon status untuk menunjukkan diterima, ditolak, atau belum diproses
                status_icon = MDIconButton(
                    icon='check-circle' if pengaduan.get('status') == 'accepted' else
                         'cancel' if pengaduan.get('status') == 'rejected' else
                         'alert-circle',  # Ikon untuk pengaduan yang belum diproses
                    icon_color=(0, 1, 0, 1) if pengaduan.get('status') == 'accepted' else
                                (1, 0, 0, 1) if pengaduan.get('status') == 'rejected' else
                                (1, 1, 0, 1),  # Kuning untuk pengaduan yang belum diproses
                    size_hint=(0.3, 1)  # Ukuran ikon
                )

                # Ikon hapus
                delete_button = MDIconButton(
                    icon='trash-can',
                    on_release=lambda x, id=pengaduan_id: self.delete_pengaduan(id)  # Gunakan ID dari pengaduan
                )

                # Tambahkan Label dan Ikon ke BoxLayout
                pengaduan_box.add_widget(title_label)
                pengaduan_box.add_widget(status_icon)  # Menambahkan ikon status
                pengaduan_box.add_widget(delete_button)

                # Tambahkan BoxLayout ke layout utama
                self.ids.status_layout.add_widget(pengaduan_box)

    def delete_pengaduan(self, pengaduan_id):
        # Logika untuk menghapus pengaduan di database
        try:
            username = MDApp.get_running_app().get_current_user_id()  # Ambil current_user_id
            Database.delete_user_pengaduan(username, pengaduan_id)  # Pastikan Anda memiliki metode ini di Database
            self.show_dialog("Pengaduan berhasil dihapus!")
            self.update_status()  # Perbarui tampilan setelah penghapusan
        except Exception as e:
            self.show_dialog(f"Gagal menghapus pengaduan: {e}")

    def show_dialog(self, pesan):
        dialog = MDDialog(
            text=pesan,
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=lambda x: dialog.dismiss()
                ),
            ],
        )
        dialog.open()