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
from urllib.parse import quote
import os

class AdminDaftarScreen(Screen):
    def on_enter(self):
        self.load_pengaduan()

    def load_pengaduan(self):
        # Ambil semua pengaduan dari database
        pengaduan_list = Database.get_all_pengaduan()  # Pastikan Anda memiliki metode ini
        self.ids.pengaduan_grid.clear_widgets()  # Kosongkan layout sebelumnya

        for user_id, pengaduan_data in pengaduan_list:
            for pengaduan_id, pengaduan in pengaduan_data.items():  # Mengakses data pengaduan
                # Hanya tambahkan pengaduan yang belum diterima atau ditolak
                if pengaduan.get('status') not in ['accepted', 'rejected']:  # Memeriksa status pengaduan
                    self.add_pengaduan_widget(user_id, pengaduan_id, pengaduan)  # Menggunakan user_id dan pengaduan_id

    def add_pengaduan_widget(self, user_id, pengaduan_id, pengaduan):
        # Cek apakah pengaduan adalah dictionary dan memiliki kunci 'judul' dan 'gambar'
        if isinstance(pengaduan, dict) and 'judul' in pengaduan and 'gambar' in pengaduan:
            # Buat BoxLayout untuk setiap pengaduan
            pengaduan_box = MDBoxLayout(orientation='vertical', size_hint=(None, None), size=(dp(100), dp(150)), padding=dp(5))

            image_source = pengaduan['gambar']
            print(f"Memuat gambar dari URL: {image_source}")  # Debug URL gambar
            image_widget = KivyImage(source=image_source, size_hint=(1, 0.7), allow_stretch=True)

            # Menangani kesalahan saat memuat gambar
            def on_image_error(instance):
                print(f"Gambar tidak ditemukan: {image_source}")  # Log kesalahan
                instance.source = 'path/to/placeholder/image.png'  # Ganti dengan path gambar placeholder

            image_widget.bind(on_error=on_image_error)  # Bind event error

            image_widget.bind(on_touch_down=lambda instance, touch: self.show_detail_pengaduan(user_id, pengaduan_id) if instance.collide_point(*touch.pos) else False)

            # Label untuk judul pengaduan
            title_label = MDLabel(text=pengaduan['judul'], size_hint=(1, 0.3), halign='center')
            title_label.bind(on_touch_down=lambda instance, touch: self.show_detail_pengaduan(user_id, pengaduan_id) if instance.collide_point(*touch.pos) else False)

            # Tambahkan Gambar dan Label ke BoxLayout
            pengaduan_box.add_widget(image_widget)
            pengaduan_box.add_widget(title_label)

            # Tambahkan BoxLayout ke GridLayout utama
            self.ids.pengaduan_grid.add_widget(pengaduan_box)
        else:
            print(f"Pengaduan dengan ID {pengaduan_id} tidak memiliki judul atau gambar yang valid: {pengaduan}")

    def show_detail_pengaduan(self, user_id, pengaduan_id):
        print(f"Mencoba mendapatkan detail pengaduan dengan ID: {pengaduan_id} untuk pengguna {user_id}")  # Debug print
        pengaduan = Database.get_pengaduan_by_id(user_id, pengaduan_id)  # Menggunakan user_id dan pengaduan_id
        if pengaduan:
            detail_text = f"Judul: {pengaduan['judul']}\nDeskripsi: {pengaduan['deskripsi']}\nAlamat: {pengaduan['alamat']}\nGambar: {pengaduan['gambar']}\nUser: {user_id}"
            self.show_dialog(detail_text, user_id, pengaduan_id)  # Pass user_id dan pengaduan_id
        else:
            self.show_dialog("Pengaduan tidak ditemukan.")

    def show_dialog(self, message, user_id, pengaduan_id):
        dialog = MDDialog(
            title="Detail Pengaduan",
            text=message,
            buttons=[
                MDFlatButton(text="Tutup", on_release=lambda x: dialog.dismiss()),
                MDFlatButton(text="Terima", on_release=lambda x: self.terima_pengaduan(user_id, pengaduan_id, dialog)),  # Tambahkan tombol Terima
                MDFlatButton(text="Tolak", on_release=lambda x: self.tolak_pengaduan(user_id, pengaduan_id, dialog))  # Tambahkan tombol Tolak
            ],
        )
        dialog.open()

    def terima_pengaduan(self, user_id, pengaduan_id, dialog):
        # Logika untuk menandai pengaduan sebagai diterima
        try:
            Database.update_pengaduan_status(user_id, pengaduan_id, status="accepted")  # Pastikan Anda memiliki metode ini
            dialog.dismiss()  # Tutup dialog setelah menerima pengaduan
            self.load_pengaduan()  # Muat ulang pengaduan untuk memperbarui tampilan
        except Exception as e:
            self.show_dialog(f"Gagal menerima pengaduan: {e}")

    def tolak_pengaduan(self, user_id, pengaduan_id, dialog):
        # Logika untuk menandai pengaduan sebagai ditolak
        try:
            Database.update_pengaduan_status(user_id, pengaduan_id, status="rejected")  # Pastikan Anda memiliki metode ini
            dialog.dismiss()  # Tutup dialog setelah menolak pengaduan
            self.load_pengaduan()  # Muat ulang pengaduan untuk memperbarui tampilan
        except Exception as e:
            self.show_dialog(f"Gagal menolak pengaduan: {e}")