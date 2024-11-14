from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.metrics import dp
from datetime import datetime
from kivy.core.text import LabelBase

from database import Database

# Daftarkan font kustom Montserrat
LabelBase.register(name='Montserrat', fn_regular='assets/font/Montserrat-Regular.otf')

class AdminPesanScreen(Screen):
    def on_enter(self):
        self.load_notifikasi()

    def load_notifikasi(self):
        self.ids.notifikasi_list.clear_widgets()  # Kosongkan layout sebelumnya
        pengaduan_list = Database.get_all_pengaduan()  # Ambil semua pengaduan

        for user_id, pengaduan_data in pengaduan_list:
            for pengaduan_id, pengaduan in pengaduan_data.items():
                notifikasi = Database.get_notifications(user_id, pengaduan_id)  # Ambil notifikasi untuk pengaduan ini
                if notifikasi:
                    for notif_id, notif in notifikasi:
                        self.add_notifikasi_widget(pengaduan['judul'], notif)

    def add_notifikasi_widget(self, judul_pengaduan, notif):
        if isinstance(notif, dict):
            # Buat BoxLayout untuk menampung informasi notifikasi
            item_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(80), padding=[dp(10), dp(5)], spacing=dp(10))

            # Avatar atau ikon
            avatar = Image(
                source='assets/image/profile.png',  # Ganti dengan path ke ikon avatar yang sesuai
                size_hint_x=None,
                width=dp(50),
            )

            # Label untuk judul pengaduan
            message_label = Label(
                text=judul_pengaduan,  # Menampilkan judul pengaduan
                size_hint=(0.7, 1),  # Memberikan ruang yang lebih besar untuk judul
                halign='left',
                valign='middle',
                text_size=(self.width * 0.7, None),  # Atur lebar teks
                font_name='Montserrat'  # Menggunakan font Montserrat
            )
            message_label.bind(size=message_label.setter('text_size'))

            # Label untuk waktu
            time_label = Label(
                text=self.format_time(notif['timestamp']),  # Mengambil timestamp dari notifikasi
                size_hint=(0.3, 1),  # Memberikan ruang untuk waktu
                halign='right',
                valign='middle',
                font_name='Montserrat'  # Menggunakan font Montserrat
            )

            # Menambahkan fungsi untuk berpindah ke detail pesan saat judul ditekan
            message_label.bind(on_touch_down=lambda instance, touch: self.go_to_detail(notif) if instance.collide_point(*touch.pos) else False)

            item_layout.add_widget(avatar)  # Tambahkan avatar ke BoxLayout
            item_layout.add_widget(message_label)  # Tambahkan judul ke BoxLayout
            item_layout.add_widget(time_label)  # Tambahkan waktu ke BoxLayout

            self.ids.notifikasi_list.add_widget(item_layout)  # Tambahkan BoxLayout ke list

    def format_time(self, timestamp):
        # Mengonversi timestamp menjadi format waktu yang lebih mudah dibaca
        time_format = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        return time_format.strftime("%I:%M %p")  # Format waktu, misalnya "03:40 PM"

    def go_to_detail(self, notif):
        # Pindah ke halaman detail dan passing notifikasi
        self.manager.current = 'admin_detail_pesan'
        detail_screen = self.manager.get_screen('admin_detail_pesan')
        detail_screen.set_notif(notif)  # Mengirimkan notifikasi ke halaman detail
