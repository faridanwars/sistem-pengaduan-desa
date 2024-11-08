from database import Database
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from datetime import datetime

class AdminDetailPesanScreen(Screen):
    def on_enter(self):
        # Memuat detail pesan saat layar dimasuki
        self.load_detail()

    def load_detail(self):
        # Ambil data dari previous screen (misalnya, dari ScreenManager)
        notif = self.manager.get_screen('admin_pesan').selected_notif  # Ambil notifikasi yang dipilih

        # Memastikan data notifikasi tersedia
        if notif:
            # Menampilkan detail notifikasi
            self.ids.message_container.clear_widgets()  # Kosongkan kontainer pesan

            # Menambahkan timestamp di atas pesan
            timestamp_label = Label(
                text=self.format_time(notif['timestamp']),  # Format timestamp
                size_hint_y=None,
                height=dp(30),
                halign='right',
                valign='middle',
                padding=[0, dp(5)]  # Menambahkan padding vertikal
            )
            self.ids.message_container.add_widget(timestamp_label)  # Menambahkan label timestamp

            # Menambahkan spacer untuk jarak antara timestamp dan pesan
            spacer = Label(size_hint_y=None, height=dp(10))  # Spacer dengan tinggi 10 dp
            self.ids.message_container.add_widget(spacer)  # Tambahkan spacer

            # Menambahkan pesan admin
            self.ids.message_container.add_widget(self.create_message_bubble(notif['pesan'], 'admin'))  # Menambahkan pesan admin
            self.ids.message_container.add_widget(self.create_message_bubble("Pesan balasan dari pengguna.", 'user'))  # Contoh pesan pengguna
        else:
            self.ids.message_container.add_widget(Label(text="Tidak ada detail yang tersedia."))

    def send_message(self):
        # Mengambil teks dari TextInput
        message_text = self.ids.message_input.text.strip()  # Menghapus spasi di awal dan akhir

        if message_text:  # Pastikan pesan tidak kosong
            # Logika untuk mengirim pesan
            print(f"Pesan terkirim: {message_text}")  # Menampilkan pesan di konsol

            # Menambahkan pesan ke message_container
            self.ids.message_container.add_widget(self.create_message_bubble(message_text, 'admin'))  # Menampilkan pesan admin

            # Mengirim pesan ke pengguna melalui database
            notif = self.manager.get_screen('admin_pesan').selected_notif  # Ambil notifikasi yang dipilih
            user_id = notif['user_id']  # Misalkan user_id ada di notif

            # Kirim pesan ke database dengan timestamp yang benar
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            Database.send_message(user_id, {"content": message_text, "timestamp": timestamp})

            # Kosongkan TextInput setelah mengirim pesan
            self.ids.message_input.text = ""
        else:
            print("Pesan tidak boleh kosong.")  # Menampilkan pesan jika input kosong

    def create_message_bubble(self, message, sender):
        # Membuat kotak pesan
        bubble = BoxLayout(size_hint_y=None, height=dp(50), padding=dp(10), spacing=dp(10))
        message_label = Label(text=message, size_hint_x=0.8, halign='left', valign='middle', text_size=(self.width * 0.8, None))

        # Menentukan warna berdasarkan pengirim
        if sender == 'admin':
            message_label.color = (1, 1, 1, 1)  # Warna putih untuk admin
            bubble.md_bg_color = (0.0, 0.5, 0.5, 1)  # Warna untuk latar belakang admin
        else:
            message_label.color = (0.678, 0.847, 0.902, 1)  # Warna biru langit untuk pengguna
            bubble.md_bg_color = (0.9, 0.9, 0.9, 1)  # Warna untuk latar belakang pengguna

        bubble.add_widget(message_label)  # Tambahkan label pesan ke kotak
        return bubble

    def format_time(self, timestamp):
        # Mengonversi timestamp menjadi format waktu yang lebih mudah dibaca
        try:
            time_format = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            return time_format.strftime("%d %b %Y, %I:%M %p")  # Format waktu, misalnya "01 Jan 2023, 03:40 PM"
        except Exception as e:
            print(f"Error saat memformat waktu: {e}")
            return timestamp  # Jika terjadi kesalahan, kembalikan timestamp asli

    def back_to_messages(self):
        # Kembali ke halaman pesan
        self.manager.current = 'admin_pesan'
