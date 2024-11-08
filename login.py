from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.core.window import Window
from kivy.lang import Builder
from database import Database
from kivymd.app import MDApp

class CreateAccountScreen(Screen):
    dialog = None

    def show_dialog(self, pesan):
        if not self.dialog:
            self.dialog = MDDialog(
                text=pesan,
                buttons=[
                    MDFlatButton(
                        text="OK",
                        on_release=lambda x: self.dialog.dismiss()
                    ),
                ],
            )
        else:
            self.dialog.text = pesan
        self.dialog.open()

    def register_account(self):
        print("Metode register_account dipanggil")
        # Ambil data yang diinput pengguna dari form
        username = self.ids['username_field'].text
        nik = self.ids['nik_field'].text
        address = self.ids['address_field'].text
        password = self.ids['create_account_password_field'].text
        profile_image = 'assets/image/profile.png'  # Ganti dengan path gambar default

        # Validasi dasar: pastikan semua kolom diisi
        if not username or not nik or not address or not password:
            self.show_dialog("Semua kolom harus diisi!")
            return

        # Cek apakah username sudah ada
        existing_user_by_username = Database.get_user(username)
        if existing_user_by_username is not None:
            self.show_dialog("Username sudah digunakan, silakan pilih yang lain.")
            return

        # Cek apakah NIK sudah ada
        existing_user_by_nik = Database.get_user_by_nik(nik)
        if existing_user_by_nik is not None:
            self.show_dialog("NIK sudah digunakan, silakan pilih yang lain.")
            return

        # Buat data pengguna dalam bentuk dictionary
        user_data = {
            "username": username,
            "nik": nik,
            "address": address,
            "password": password,
            "role": "admin" if username == "admin" else "user",  # Otomatis memberikan peran
            "profile_image": profile_image  # Menyimpan path gambar profil
        }

        # Simpan data ke Firebase
        try:
            Database.add_user(user_data)
            self.show_dialog("Akun berhasil dibuat!")
            self.manager.current = 'login'  # Arahkan ke layar login
            self.ids['username_field'].text = ""
            self.ids['nik_field'].text = ""
            self.ids['address_field'].text = ""
            self.ids['create_account_password_field'].text = ""
        except Exception as e:
            self.show_dialog(f"Gagal membuat akun: {e}")

class LoginScreen(Screen):
    dialog = None

    def show_dialog(self, pesan):
        if not self.dialog:
            self.dialog = MDDialog(
                text=pesan,
                buttons=[
                    MDFlatButton(
                        text="OK",
                        on_release=lambda x: self.dialog.dismiss()
                    ),
                ],
            )
        else:
            self.dialog.text = pesan
        self.dialog.open()

    def check_credentials(self):
        # Ambil data yang diinput pengguna dari form
        username = self.ids['login_username_field'].text
        password = self.ids['login_password_field'].text

        # Validasi dasar: pastikan username dan password diisi
        if not username or not password:
            self.show_dialog("Username dan password harus diisi!")
            return

        # Cek username dan password di Firebase
        try:
            user_data = Database.get_user(username)
            if user_data and user_data['password'] == password:
                app = MDApp.get_running_app()
                app.set_current_user_id(username)  # Set current_user_id
                role = user_data['role']
                if role == "admin":
                    self.manager.current = 'admin_home'
                else:
                    self.manager.current = 'users_home'
            else:
                self.show_dialog("Username atau password salah!")
        except Exception as e:
            self.show_dialog(f"Gagal memeriksa data: {e}")

class HomeScreen(Screen):
    pass

class AdminHomeScreen(Screen):
    pass

class MyApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"

        Builder.load_file('login.kv')
        Builder.load_file('users/home.kv')
        Builder.load_file('admin/admin_home.kv')

        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(CreateAccountScreen(name='create_account'))  # Memanggil CreateAccountScreen dari login.py
        sm.add_widget(HomeScreen(name='users_home'))
        sm.add_widget(AdminHomeScreen(name='admin_home'))  # Untuk admin home
        return sm

if __name__ == "__main__":
    Window.size = (360, 640)
    MyApp().run()