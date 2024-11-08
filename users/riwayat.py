from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.list import OneLineListItem
from kivymd.uix.dialog import MDDialog
from database import Database
from kivymd.uix.button import MDFlatButton

class RiwayatScreen(Screen):
    def on_enter(self):
        self.load_pengaduan()

    def load_pengaduan(self):
        app = MDApp.get_running_app()
        user_id = app.get_current_user_id()  # Ambil user_id dari aplikasi
        pengaduan_list = Database.get_pengaduan(user_id)  # Ambil pengaduan dari database

        print("Pengaduan List:", pengaduan_list)  # Tambahkan log ini untuk debugging

        # Hapus daftar yang ada sebelum memuat yang baru
        self.ids.pengaduan_list.clear_widgets()

        if pengaduan_list:
            for pengaduan_id, pengaduan_data in pengaduan_list:
                item = OneLineListItem(
                    text=pengaduan_data['judul'], 
                    on_release=lambda x, id=pengaduan_id: self.show_detail(id)
                )
                self.ids.pengaduan_list.add_widget(item)
        else:
            item = OneLineListItem(text="Tidak ada pengaduan ditemukan.")
            self.ids.pengaduan_list.add_widget(item)

    def show_detail(self, pengaduan_id):
        # Tampilkan detail pengaduan berdasarkan ID
        app = MDApp.get_running_app()
        user_id = app.get_current_user_id()  # Ambil user_id dari aplikasi
        pengaduan_detail = Database.get_pengaduan_by_id(user_id, pengaduan_id)
        
        if pengaduan_detail:
            detail_message = (
                f"Judul: {pengaduan_detail['judul']}\n"
                f"Alamat: {pengaduan_detail['alamat']}\n"
                f"Deskripsi: {pengaduan_detail['deskripsi']}\n"
                f"Gambar: {pengaduan_detail['gambar']}\n"
                f"Status: {pengaduan_detail['status']}"
            )
            self.show_dialog(detail_message)
        else:
            self.show_dialog("Detail pengaduan tidak ditemukan.")

    def show_dialog(self, message):
        dialog = MDDialog(
            title="Detail Pengaduan",
            text=message,
            buttons=[
                MDFlatButton(text="Tutup", on_release=lambda x: dialog.dismiss())
            ],
        )
        dialog.open()