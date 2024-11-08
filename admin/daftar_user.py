from kivy.uix.screenmanager import Screen
from kivymd.uix.list import OneLineAvatarListItem, MDList
from kivymd.uix.button import MDIconButton, MDFlatButton
from kivymd.uix.dialog import MDDialog
from database import Database
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

class DaftarUserScreen(Screen):
    dialog = None  # Untuk menyimpan dialog

    def on_enter(self):
        # Mengambil data pengguna dari database
        self.ids.user_list.clear_widgets()  # Menghapus widget sebelumnya
        users = Database.db.child("users").get()  # Mengambil semua pengguna

        if users.val() is not None:
            for user in users.each():
                user_data = user.val()
                user_id = user.key()  # Ambil ID pengguna
                user_name = user_data.get('username', 'Nama Tidak Ditemukan')

                # Menggunakan BoxLayout untuk menampung nama dan tombol hapus
                item_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='40dp')

                # Menambahkan nama pengguna
                list_item = OneLineAvatarListItem(text=user_name)
                item_layout.add_widget(list_item)  # Menambahkan nama pengguna ke layout

                # Menghubungkan klik pada item daftar untuk menampilkan detail pengguna
                list_item.bind(on_release=lambda x, user_data=user_data: self.show_user_details(user_data))

                # Membuat tombol hapus sebagai ikon
                delete_button = MDIconButton(
                    icon="trash-can",  # Menggunakan ikon untuk tombol hapus
                    size_hint=(None, None),
                    size=(40, 40),
                    pos_hint={"center_y": 0.5},
                    on_release=lambda x, user_id=user_id, user_name=user_name: self.confirm_delete_user(user_id, user_name)  # Menghubungkan tombol dengan fungsi konfirmasi hapus
                )

                item_layout.add_widget(delete_button)  # Menambahkan tombol hapus ke layout
                self.ids.user_list.add_widget(item_layout)  # Menambahkan layout ke dalam daftar
        else:
            # Jika tidak ada pengguna
            self.ids.user_list.add_widget(OneLineAvatarListItem(text="Tidak ada pengguna ditemukan"))

    def confirm_delete_user(self, user_id, user_name):
        """Menampilkan dialog konfirmasi sebelum menghapus pengguna."""
        if user_name.lower() == "admin":  # Pengecekan apakah nama pengguna adalah "admin"
            # Tampilkan peringatan bahwa admin tidak bisa dihapus
            MDDialog(
                title="Peringatan",
                text="Pengguna 'admin' tidak dapat dihapus.",
                buttons=[
                    MDFlatButton(
                        text="Tutup",  # Teks untuk tombol 'Tutup'
                        on_release=self.close_dialog  # Menutup dialog
                    )
                ]
            ).open()
        else:
            self.dialog = MDDialog(
                title="Konfirmasi Hapus",
                text="Apakah Anda yakin ingin menghapus pengguna ini?",
                buttons=[
                    MDFlatButton(
                        text="Tidak",  # Teks untuk tombol 'Tidak'
                        on_release=self.close_dialog  # Menutup dialog
                    ),
                    MDFlatButton(
                        text="Ya",  # Teks untuk tombol 'Ya'
                        on_release=lambda x: self.delete_user(user_id)  # Menghapus pengguna jika ya
                    )
                ]
            )
            self.dialog.open()

    def show_user_details(self, user_data):
        """Menampilkan dialog detail pengguna."""
        self.dialog = MDDialog(
            title="Detail Pengguna",
            text=f"Nama: {user_data['username']}\n"
                 f"Alamat: {user_data['address']}\n"
                 f"NIK: {user_data['nik']}",
            buttons=[
                MDFlatButton(
                    text="Tutup",
                    on_release=self.close_dialog  # Menutup dialog
                )
            ]
        )
        self.dialog.open()

    def close_dialog(self, *args):
        """Menutup dialog."""
        if self.dialog:
            self.dialog.dismiss()

    def delete_user(self, user_id):
        """Menghapus pengguna dari database."""
        Database.db.child("users").child(user_id).remove()
        self.on_enter()  # Memperbarui tampilan setelah penghapusan