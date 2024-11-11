from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivymd.uix.list import OneLineAvatarIconListItem
from kivy.uix.image import Image as KivyImage
from kivy.metrics import dp
from database import Database

class PesanScreen(Screen):
    def on_enter(self):
        self.load_notifikasi()  # Memuat notifikasi saat memasuki layar

    def load_notifikasi(self):
        self.ids.notifikasi_list.clear_widgets()  # Kosongkan daftar notifikasi sebelumnya
        user_id = self.get_active_user_id()  # Ambil ID pengguna yang aktif
        print(f"Mengambil pengaduan untuk user_id: {user_id}")  # Debugging
        pengaduan_list = Database.get_pengaduan(user_id)  # Ambil pengaduan untuk pengguna ini

        for pengaduan_id, pengaduan in pengaduan_list:
            notifications = Database.get_notifications(user_id, pengaduan_id)  # Ambil notifikasi untuk pengaduan ini
            if notifications:  # Jika ada notifikasi
                if 'judul' in pengaduan:  # Periksa apakah kunci 'judul' ada
                    judul_pengaduan = pengaduan['judul']
                    self.add_notifikasi_widget(judul_pengaduan, pengaduan)  # Tambahkan widget notifikasi
                else:
                    print(f"Pengaduan ID {pengaduan_id} tidak memiliki kunci 'judul': {pengaduan}")  # Debugging

    def get_active_user_id(self):
        # Implementasikan logika untuk mendapatkan ID pengguna yang aktif
        app = MDApp.get_running_app()
        return app.get_current_user_id()  # Ganti dengan cara yang sesuai untuk mendapatkan user_id yang aktif

    def add_notifikasi_widget(self, judul_pengaduan, pengaduan):
        # Buat BoxLayout untuk menampung elemen notifikasi
        item_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(70), padding=dp(10), spacing=dp(10))

        # Avatar atau ikon
        avatar = KivyImage(source='assets/image/profile.png', size_hint_x=None, width=dp(50))  # Ganti dengan path ke ikon avatar yang sesuai
        item_layout.add_widget(avatar)  # Tambahkan avatar ke BoxLayout

        # BoxLayout untuk detail pesan
        detail_box = BoxLayout(orientation='vertical', size_hint=(1, None), padding=(20, 0), spacing=dp(5))

        # Label untuk judul pengaduan
        message_label = Label(
            text=judul_pengaduan,  # Menampilkan judul pengaduan
            size_hint_y=None,
            height=dp(50),  # Atur tinggi label judul
            halign='left',
            valign='middle',
            text_size=(self.width * 0.6, None)  # Atur lebar teks
        )
        detail_box.add_widget(message_label)  # Tambahkan label pesan ke detail_box

        # Tambahkan detail_box ke item_layout
        item_layout.add_widget(detail_box)

        # Tambahkan event handler untuk message_label agar dapat diklik
        message_label.bind(on_touch_down=self.on_label_touch)

        # Simpan referensi ke pengaduan dalam item_layout
        item_layout.pengaduan = pengaduan

        self.ids.notifikasi_list.add_widget(item_layout)  # Tambahkan item_layout ke daftar notifikasi

    def on_label_touch(self, instance, touch):
        # Pastikan touch berada dalam area label
        if instance.collide_point(*touch.pos):
            # Cari item_layout induk dan dapatkan pengaduan terkait
            parent = instance.parent.parent
            if hasattr(parent, 'pengaduan'):
                self.show_detail(parent.pengaduan)

    def show_detail(self, pengaduan):
        # Pindah ke halaman detail dan passing pengaduan
        self.manager.current = 'detailpesan'  # Ganti dengan nama screen DetailPesan
        detail_screen = self.manager.get_screen('detailpesan')
        detail_screen.set_notif(pengaduan)  # Panggil metode set_notif() untuk mengatur data
