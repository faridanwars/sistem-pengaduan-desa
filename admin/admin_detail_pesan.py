from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.metrics import dp
from datetime import datetime
from kivy.core.text import LabelBase

# Daftarkan font kustom Montserrat
LabelBase.register(name='Montserrat', fn_regular='assets/font/Montserrat-Regular.otf')

class AdminDetailPesanScreen(Screen):
    notif = None  # Menyimpan notifikasi yang diterima

    def on_enter(self):
        # Periksa apakah 'message_list' ada dalam self.ids
        if 'message_list' in self.ids:
            self.ids.message_list.clear_widgets()  # Kosongkan daftar pesan sebelumnya
            if self.notif:
                self.add_message_widget(self.notif)  # Tambahkan widget pesan

    def set_notif(self, notif):
        self.notif = notif  # Menyimpan notifikasi yang diterima

    def add_message_widget(self, notif):
        # Buat BoxLayout untuk menampung pesan
        item_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(100),
            padding=(dp(10), dp(10)),
            spacing=dp(10)
        )

        # Label untuk pesan
        message_label = Label(
            text=notif['pesan'],
            size_hint_y=None,
            height=dp(50),
            halign='left',
            valign='top',
            text_size=(self.width * 0.9, None),
            font_name='Montserrat'  # Menggunakan font Montserrat
        )
        message_label.bind(texture_size=message_label.setter('size'))

        # Label untuk waktu
        time_label = Label(
            text=self.format_time(notif['timestamp']),
            size_hint_y=None,
            height=dp(20),
            halign='right',
            valign='middle',
            padding_x=dp(20),
            font_name='Montserrat'  # Menggunakan font Montserrat
        )

        # Tambahkan label pesan dan waktu ke item layout
        item_layout.add_widget(message_label)
        item_layout.add_widget(time_label)

        # Periksa apakah 'message_list' ada sebelum menambahkan widget
        if 'message_list' in self.ids:
            self.ids.message_list.add_widget(item_layout)

    def format_time(self, timestamp):
        time_format = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        return time_format.strftime("%d/%m/%Y %H.%M")
