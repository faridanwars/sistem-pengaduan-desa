from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.metrics import dp
from kivy.uix.button import Button
from kivymd.uix.button import MDFlatButton
from database import Database
from datetime import datetime
from kivymd.uix.dialog import MDDialog

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
            item_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(80), padding=dp(10))

            # Avatar atau ikon
            avatar = Image(
                source='path/to/avatar/icon.png',  # Ganti dengan path ke ikon avatar yang sesuai
                size_hint_x=None,
                width=dp(50),
            )

            # Label untuk judul pengaduan
            message_label = Label(
                text=judul_pengaduan,  # Menampilkan judul pengaduan
                size_hint=(0.6, 1),  # Memberikan ruang yang lebih besar untuk judul
                halign='left',
                valign='middle'
            )

            # Label untuk waktu
            time_label = Label(
                text=self.format_time(notif['timestamp']),  # Mengambil timestamp dari notifikasi
                size_hint=(0.3, 1),  # Memberikan ruang untuk waktu
                halign='right',
                valign='middle'
            )

            # Menambahkan fungsi untuk menampilkan detail notifikasi saat judul ditekan
            message_label.bind(on_touch_down=lambda instance, touch: self.show_notification_detail(notif) if instance.collide_point(*touch.pos) else False)

            item_layout.add_widget(avatar)  # Tambahkan avatar ke BoxLayout
            item_layout.add_widget(message_label)  # Tambahkan judul ke BoxLayout
            item_layout.add_widget(time_label)  # Tambahkan waktu ke BoxLayout

            self.ids.notifikasi_list.add_widget(item_layout)  # Tambahkan BoxLayout ke list

    def format_time(self, timestamp):
        # Mengonversi timestamp menjadi format waktu yang lebih mudah dibaca
        time_format = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        return time_format.strftime("%I:%M %p")  # Format waktu, misalnya "03:40 PM"

    def show_notification_detail(self, notif):
        # Membuat label untuk menampilkan detail notifikasi
        detail_label = Label(
            text=f"Pesan: {notif['pesan']}",  # Hanya menampilkan pesan
            halign='left',
            valign='middle',
            size_hint_x=1,  # Mengatur lebar label agar sesuai dengan dialog
            size_hint_y=None,
            height=self.get_label_height(notif['pesan']),  # Mengatur tinggi label berdasarkan isi pesan
        )

        # Membuat dialog
        close_button = MDFlatButton(text="Tutup", on_release=lambda x: dialog.dismiss())

        # Membuat dialog
        dialog = MDDialog(
            title='Detail Notifikasi',
            type='custom',
            content_cls=BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10)),
            buttons=[close_button]
        )

        # Menambahkan label ke dalam dialog
        dialog.content_cls.add_widget(detail_label)

        # Menampilkan dialog
        dialog.open()

    def get_label_height(self, text):
        # Menghitung tinggi label berdasarkan isi teks
        label = Label(text=text, size_hint_x=None, width=self.width * 0.75)  # Membuat label sementara untuk menghitung tinggi
        label.bind(size=label.setter('size'))  # Mengikat ukuran label
        label.texture_update()  # Memperbarui tekstur untuk mendapatkan ukuran yang benar
        return label.height + dp(20)  # Menambahkan padding
