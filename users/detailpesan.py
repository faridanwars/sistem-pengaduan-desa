from datetime import datetime
from kivy.uix.screenmanager import Screen
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

class DetailPesanScreen(Screen):
    notif = None  # Menyimpan notifikasi yang diterima

    def on_enter(self):
        # Debug: cetak data notifikasi untuk memeriksa apakah diterima dengan benar
        print("Notif Data:", self.notif)

        if self.notif and isinstance(self.notif, dict):
            # Akses data notifikasi dari struktur yang benar
            notifikasi_data = self.notif.get('notifikasi', {})
            if notifikasi_data:
                # Ambil data dari notifikasi pertama (ID unik)
                first_key = next(iter(notifikasi_data))
                notif_detail = notifikasi_data.get(first_key, {})

                # Tampilkan pesan dan waktu dari notifikasi
                self.ids.notif_title.text = notif_detail.get('pesan', "Pesan tidak tersedia")
                self.ids.notif_time.text = self.format_time(notif_detail.get('timestamp', ""))
            else:
                # Menampilkan pesan default jika data notifikasi tidak ada
                self.ids.notif_title.text = "Pesan tidak tersedia"
                self.ids.notif_time.text = "Waktu tidak tersedia"
        else:
            # Menampilkan pesan default jika data notifikasi tidak valid
            self.ids.notif_title.text = "Pesan tidak tersedia"
            self.ids.notif_time.text = "Waktu tidak tersedia"

    def set_notif(self, notif):
        """Menyimpan notifikasi yang diterima dan memicu pembaruan tampilan."""
        self.notif = notif
        self.on_enter()  # Memperbarui tampilan saat notifikasi diatur

    def format_time(self, timestamp):
        """Mengonversi timestamp menjadi format waktu yang lebih mudah dibaca."""
        try:
            # Mengonversi string timestamp ke format yang mudah dibaca
            time_format = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            return time_format.strftime("%d/%m/%Y %H.%M")
        except ValueError:
            return "Waktu tidak tersedia"