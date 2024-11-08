import pyrebase
from config import get_firebase_config
import os
from datetime import datetime

class Database:
    config = get_firebase_config()
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()

    @staticmethod
    def test_connection():
        """
        Menguji koneksi ke database Firebase dengan mengambil data pengguna.
        Menampilkan pesan apakah koneksi berhasil atau ada kesalahan.
        """
        try:
            users = Database.db.child("users").get()
            if users.val() is not None:
                print("DEBUG: Koneksi ke database berhasil. Pengguna yang ditemukan:")
                for user in users.each():
                    print(user.val())
            else:
                print("DEBUG: Tidak ada pengguna ditemukan.")
        except Exception as e:
            print(f"DEBUG: Kesalahan saat menghubungi database: {e}")

    @staticmethod
    def add_user(user_data):
        """
        Menambahkan pengguna baru ke Firebase dengan data yang diberikan.
        """
        try:
            return Database.db.child("users").push(user_data)
        except Exception as e:
            print(f"Error menambahkan pengguna: {e}")
            raise e

    @staticmethod
    def get_user(username):
        """
        Mengambil data pengguna berdasarkan username.
        Jika pengguna ditemukan, mengembalikan data pengguna pertama.
        """
        try:
            users = Database.db.child("users").order_by_child("username").equal_to(username).get()
            if users.each():  
                print(f"Data pengguna ditemukan: {users.each()[0].val()}")
                return users.each()[0].val()  
            else:
                print("Data pengguna tidak ditemukan.")
                return None
        except Exception as e:
            print(f"Kesalahan saat mengambil data pengguna: {e}")
            return None

    @staticmethod
    def get_user_by_id(user_id):
        """
        Mengambil data pengguna berdasarkan user_id.
        """
        try:
            user = Database.db.child("users").child(user_id).get()
            if user.val() is not None:
                print(f"Data pengguna ditemukan: {user.val()}")
                return user.val()  
            else:
                print("Data pengguna tidak ditemukan.")
                return None
        except Exception as e:
            print(f"Kesalahan saat mengambil data pengguna: {e}")
            return None

    @staticmethod
    def get_user_by_nik(nik):
        """
        Mengambil data pengguna berdasarkan NIK (Nomor Induk Kependudukan).
        """
        try:
            users = Database.db.child("users").order_by_child("nik").equal_to(nik).get()
            if users.each():  
                print(f"Data pengguna ditemukan: {users.each()[0].val()}")
                return users.each()[0].val()  
            else:
                print("Data pengguna tidak ditemukan.")
                return None
        except Exception as e:
            print(f"Kesalahan saat mengambil data pengguna: {e}")
            return None
        
    @staticmethod
    def update_user(username, user_data):
        """
        Mengupdate data pengguna berdasarkan username.
        """
        try:
            users = Database.db.child("users").order_by_child("username").equal_to(username).get()
            if users.each():  
                user_id = users.each()[0].key()  # Ambil ID pengguna yang ditemukan
                Database.db.child("users").child(user_id).set(user_data)  # Gunakan set untuk memperbarui
            else:
                print("Pengguna tidak ditemukan.")
        except Exception as e:
            print(f"Error memperbarui pengguna: {e}")
            raise e

    @staticmethod
    def add_user_pengaduan(user_id, pengaduan_data):
        """
        Menambahkan pengaduan baru untuk pengguna tertentu.
        """
        try:
            pengaduan_ref = Database.db.child("pengaduan").child(user_id).push(pengaduan_data)
            return pengaduan_ref
        except Exception as e:
            print(f"Error menambahkan pengaduan untuk pengguna {user_id}: {e}")
            raise e
        
    @staticmethod
    def delete_user_pengaduan(user_id, pengaduan_id):
        """
        Menghapus pengaduan tertentu berdasarkan user_id dan pengaduan_id.
        """
        try:
            Database.db.child("pengaduan").child(user_id).child(pengaduan_id).remove()
        except Exception as e:
            print(f"Error menghapus pengaduan untuk pengguna {user_id}: {e}")
            raise e

    @staticmethod
    def get_pengaduan(user_id):
        """
        Mengambil semua pengaduan untuk pengguna tertentu berdasarkan user_id.
        """
        try: 
            pengaduan = Database.db.child("pengaduan").child(user_id).get()
            print(f"Data pengaduan untuk user {user_id} dari Firebase:", pengaduan.val())  # Tambahkan log ini
            if pengaduan.val() is not None:
                return [(item.key(), item.val()) for item in pengaduan.each()]  # Mengembalikan list of tuples (id, data)
            return []  
        except Exception as e:
            print(f"Error mendapatkan data pengaduan untuk pengguna {user_id}: {e}")
            return []

    @staticmethod
    def send_message(user_id, message_data):
        """
        Mengirim pesan untuk pengguna tertentu ke Firebase.
        """
        try:
            return Database.db.child("messages").child(user_id).push(message_data)
        except Exception as e:
            print(f"Error mengirim pesan untuk pengguna {user_id}: {e}")
            raise e

    @staticmethod
    def get_messages(user_id):
        """
        Mengambil semua pesan yang dikirim oleh pengguna berdasarkan user_id.
        """
        try:
            messages = Database.db.child("messages").child(user_id).get()
            if messages.val() is not None:
                return [(item.key(), item.val()) for item in messages.each()]  
            return []  
        except Exception as e:
            print(f"Error mendapatkan pesan untuk pengguna {user_id}: {e}")
            return []

    @staticmethod
    def delete_message(user_id, message_id):
        """
        Menghapus pesan tertentu untuk pengguna berdasarkan user_id dan message_id.
        """
        try:
            Database.db.child("messages").child(user_id).child(message_id).remove()
        except Exception as e:
            print(f"Error menghapus pesan untuk pengguna {user_id}: {e}")
            raise e

    @staticmethod
    def get_all_pengaduan():
        """
        Mengambil semua pengaduan yang ada di Firebase tanpa memfilter berdasarkan user_id.
        """
        try:
            pengaduan = Database.db.child("pengaduan").get()
            if pengaduan.val() is not None:
                return [(item.key(), item.val()) for item in pengaduan.each()]
            return []
        except Exception as e:
            print(f"Error mendapatkan semua pengaduan: {e}")
            return []

    @staticmethod
    def get_pengaduan_by_id(user_id, pengaduan_id):
        """
        Mengambil pengaduan berdasarkan ID pengguna dan ID pengaduan.
        """
        try:
            pengaduan = Database.db.child("pengaduan").child(user_id).child(pengaduan_id).get()
            return pengaduan.val() if pengaduan.val() is not None else None
        except Exception as e:
            print(f"Error mendapatkan pengaduan dengan ID {pengaduan_id} untuk pengguna {user_id}: {e}")
            return None
        
    @staticmethod
    def update_pengaduan_status(user_id, pengaduan_id, status):
        """
        Memperbarui status pengaduan untuk pengguna berdasarkan user_id dan pengaduan_id.
        """
        try:
            Database.db.child("pengaduan").child(user_id).child(pengaduan_id).update({"status": status})
        except Exception as e:
            print(f"Error memperbarui status pengaduan {pengaduan_id}: {e}")
            raise e
   
    @staticmethod
    def get_user_count():
        """
        Mengambil jumlah total pengguna yang terdaftar di Firebase.
        """
        try:
            users = Database.db.child("users").get()
            if users.val() is not None:
                return len(users.each())  
            return 0  
        except Exception as e:
            print(f"Error mendapatkan jumlah pengguna: {e}")
            return 0
        
    @staticmethod
    def add_message(user_id, message_content):
        """
        Menambahkan pesan baru dengan konten dan waktu pengiriman untuk pengguna tertentu.
        """
        try:
            message_data = {
                "content": message_content,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            return Database.db.child("messages").child(user_id).push(message_data)
        except Exception as e:
            print(f"Error menambahkan pesan untuk pengguna {user_id}: {e}")
            raise e

    @staticmethod
    def get_messages_by_user(user_id):
        """
        Mengambil semua pesan untuk pengguna tertentu berdasarkan user_id.
        """
        try:
            messages = Database.db.child("messages").child(user_id).get()
            if messages:
                return messages.val().values()  
            return []
        except Exception as e:
            print(f"Error mengambil pesan untuk pengguna {user_id}: {e}")
            return []

    @staticmethod
    def add_notification(pengaduan_id, user_id, notification_data):
        """
        Menambahkan notifikasi untuk pengaduan tertentu.
        """
        try:
            return Database.db.child("pengaduan").child(user_id).child(pengaduan_id).child("notifikasi").push(notification_data)
        except Exception as e:
            print(f"Error menambahkan notifikasi untuk pengaduan {pengaduan_id}: {e}")
            raise e

    @staticmethod
    def get_notifications(user_id, pengaduan_id):
        """
        Mengambil semua notifikasi untuk pengaduan tertentu.
        """
        try:
            notifications = Database.db.child("pengaduan").child(user_id).child(pengaduan_id).child("notifikasi").get()
            if notifications.val() is not None:
                return [(item.key(), item.val()) for item in notifications.each()]  
            return []  
        except Exception as e:
            print(f"Error mendapatkan notifikasi untuk pengaduan {pengaduan_id}: {e}")
            return []