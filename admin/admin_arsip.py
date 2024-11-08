from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDIconButton
from database import Database
from kivymd.uix.filemanager import MDFileManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.metrics import dp
from kivymd.uix.list import OneLineAvatarIconListItem, ILeftBody, IRightBodyTouch
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivy.uix.image import Image as KivyImage
from kivymd.uix.list import OneLineListItem
from reportlab.lib.pagesizes import letter
from kivy.uix.boxlayout import BoxLayout
from datetime import datetime
from kivymd.uix.list import OneLineListItem 
import os

class AdminArsipScreen(Screen):
    def on_enter(self):
        self.load_pengaduan()

    def load_pengaduan(self):
        pengaduan_list = Database.get_all_pengaduan()  # Ambil semua pengaduan
        self.ids.arsip_list.clear_widgets()  # Kosongkan layout sebelumnya
        nomor = 1  # Inisialisasi nomor urut

        for user_id, pengaduan_data in pengaduan_list:
            for pengaduan_id, pengaduan in pengaduan_data.items():
                if pengaduan.get('status') in ['accepted', 'rejected']:
                    self.add_pengaduan_widget(user_id, pengaduan_id, pengaduan, nomor)  # Pass nomor urut
                    nomor += 1  # Increment nomor urut

    def add_pengaduan_widget(self, user_id, pengaduan_id, pengaduan, nomor):
        if isinstance(pengaduan, dict) and 'judul' in pengaduan and 'gambar' in pengaduan:
            # Buat BoxLayout untuk menampung nomor, judul, dan tombol cetak
            item_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50), padding=dp(5))

            # Label untuk nomor urut
            nomor_label = MDLabel(
                text=str(nomor),  # Menampilkan nomor urut
                size_hint=(0.1, 1),  # Memberikan ruang untuk nomor
                halign='center'
            )

            # Label untuk judul pengaduan
            title_label = MDLabel(
                text=pengaduan['judul'],
                size_hint=(0.7, 1),  # Memberikan ruang yang lebih besar untuk judul
                halign='center',
                on_touch_down=lambda instance, touch: self.show_detail_pengaduan(user_id, pengaduan_id) if instance.collide_point(*touch.pos) else False
            )

            # Tombol cetak
            print_button = MDIconButton(
                icon='printer',
                size_hint=(0.2, 1),  # Ukuran ikon
                on_release=lambda x: self.cetak_pdf(pengaduan, user_id)
            )

            item_layout.add_widget(nomor_label)  # Tambahkan nomor urut ke BoxLayout
            item_layout.add_widget(title_label)  # Tambahkan judul ke BoxLayout
            item_layout.add_widget(print_button)  # Tambahkan ikon cetak ke BoxLayout

            self.ids.arsip_list.add_widget(item_layout)  # Tambahkan BoxLayout ke list
        else:
            print(f"Pengaduan dengan ID {pengaduan_id} tidak memiliki judul atau gambar yang valid: {pengaduan}")

    def show_detail_pengaduan(self, user_id, pengaduan_id):
        print(f"Mencoba mendapatkan detail pengaduan dengan ID: {pengaduan_id} untuk pengguna {user_id}")
        pengaduan = Database.get_pengaduan_by_id(user_id, pengaduan_id)
        if pengaduan:
            judul = pengaduan.get('judul', 'Tidak Diketahui')  # Menyimpan judul pengaduan
            status = pengaduan.get('status', 'Tidak Diketahui')
            detail_text = f"Judul: {judul}\nDeskripsi: {pengaduan['deskripsi']}\nAlamat: {pengaduan['alamat']}\nUser: {user_id}\nStatus: {status}"
            self.show_dialog(detail_text, user_id, pengaduan_id, judul)  # Passing judul ke dialog
        else:
            self.show_dialog("Pengaduan tidak ditemukan.", user_id, pengaduan_id, 'Tidak Diketahui')

    def show_dialog(self, message, user_id, pengaduan_id, judul):
        dialog_buttons = [
            MDFlatButton(text="Selesai", on_release=lambda x: self.send_notification(user_id, pengaduan_id, judul, dialog)),
            MDFlatButton(text="Tutup", on_release=lambda x: dialog.dismiss())  # Tombol tutup
        ]
        dialog = MDDialog(
            title="Detail Pengaduan",
            text=message,
            buttons=dialog_buttons,
        )
        dialog.open()

    def send_notification(self, user_id, pengaduan_id, judul, dialog):
    # Mengambil detail pengaduan
        pengaduan = Database.get_pengaduan_by_id(user_id, pengaduan_id)
        # Pesan yang akan dikirimkan kepada pengguna
        message = (f"Pengaduan dengan judul '{judul}' telah selesai diproses.\n"
                f"User: {user_id}")  # Menggunakan informasi tambahan

        try:
            # Menggunakan metode add_message untuk mengirimkan pesan ke pengguna
            Database.add_message(user_id, message)

            # Menambahkan notifikasi ke pengaduan
            notification_data = {
                "pengirim": "admin",  # Menggunakan ID atau nama admin
                "pesan": message,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "dibaca": False,
                "tipe": "notifikasi"
            }
            Database.add_notification(pengaduan_id, user_id, notification_data)

            # Menampilkan dialog konfirmasi bahwa pesan telah terkirim
            self.show_dialog_with_only_close("Notifikasi berhasil dikirim ke pengguna!", user_id, pengaduan_id, judul)
        except Exception as e:
            # Menampilkan pesan error jika pengiriman notifikasi gagal
            self.show_dialog_with_only_close(f"Gagal mengirim notifikasi: {str(e)}", user_id, pengaduan_id, judul)
        
        # Menutup dialog setelah mengirim notifikasi
        dialog.dismiss()

    def show_dialog_with_only_close(self, message, user_id, pengaduan_id, judul):
        # Dialog ini hanya menampilkan tombol "Tutup"
        dialog = MDDialog(
            title="Detail Pengaduan",
            text=message,
            buttons=[
                MDFlatButton(text="Tutup", on_release=lambda x: dialog.dismiss())
            ],
        )
        dialog.open()




    def cetak_pdf(self, pengaduan, user_id):
    # Menentukan nama file PDF
        pdf_file_name = f"{pengaduan['judul']}_{user_id}.pdf"
        pdf_folder = "admin/arsip"  # Folder tempat menyimpan PDF
        pdf_file_path = os.path.join(pdf_folder, pdf_file_name)  # Menggabungkan folder dan nama file

        # Pastikan folder ada
        os.makedirs(pdf_folder, exist_ok=True)  # Membuat folder jika belum ada

        # Membuat PDF menggunakan reportlab
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas

        c = canvas.Canvas(pdf_file_path, pagesize=letter)
        width, height = letter

        # Kop Surat
        c.drawImage("assets/image/udb.png", 80, height - 140, width=80, height=80)  # Ganti dengan path logo daerah
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(width / 2, height - 80, "LAYANAN PENGADUAN SURAKARTA")
        c.setFont("Helvetica-Bold", 14)
        c.drawCentredString(width / 2, height - 100, "KECAMATAN SERENGAN")
        c.drawCentredString(width / 2, height - 120, "KELURAHAN TIPES")

        # Alamat
        c.setFont("Helvetica", 10)
        c.drawCentredString(width / 2, height - 140, "Jl. Bhayangkara No.55, Tipes, Kec. Serengan, Kota Surakarta")

        # Garis pemisah
        c.line(100, height - 145, 500, height - 145)  # Garis horizontal

        # Tanggal dan Penerima Surat
        current_date = datetime.now().strftime("%d %B %Y")
        c.setFont("Helvetica", 12)
        c.drawString(400, height - 160, f"Surakarta, {current_date}")
        c.drawString(400, height - 180, "Kepada Yth.")
        c.drawString(400, height - 200, "Bpk. Kepala Desa")
        c.drawString(400, height - 220, "Di Tempat")

        # Memberikan ruang antara tanggal dan isi surat
        space_between = 40  # Menambahkan ruang 40 pada posisi vertikal
        y_position_for_isi_surat = height - 240 - space_between

        # Isi Surat
        c.setFont("Helvetica-Bold", 12)
        c.drawString(100, y_position_for_isi_surat, "Judul:")
        c.setFont("Helvetica", 12)
        c.drawString(100, y_position_for_isi_surat - 20, pengaduan['judul'])  # Menampilkan isi judul

        c.setFont("Helvetica-Bold", 12)
        c.drawString(100, y_position_for_isi_surat - 40, "Alamat:")
        c.setFont("Helvetica", 12)
        c.drawString(100, y_position_for_isi_surat - 60, pengaduan['alamat'])  # Menampilkan isi alamat

        c.setFont("Helvetica-Bold", 12)
        c.drawString(100, y_position_for_isi_surat - 80, "Deskripsi:")
        c.setFont("Helvetica", 12)
        c.drawString(100, y_position_for_isi_surat - 100, pengaduan['deskripsi'])  # Menampilkan isi deskripsi

        # Menampilkan gambar di bagian bawah
        c.setFont("Helvetica-Bold", 12)
        c.drawString(100, y_position_for_isi_surat - 120, "Gambar:")

        # Menampilkan gambar
        try:
            c.drawImage(pengaduan['gambar'], 100, y_position_for_isi_surat - 240, width=200, height=100, mask='auto')  # Menampilkan gambar
        except Exception as e:
            print(f"Error menampilkan gambar: {e}")

        # Pengirim
        c.setFont("Helvetica-Bold", 12)
        c.drawString(100, y_position_for_isi_surat - 260, "Pengirim:")
        c.setFont("Helvetica", 12)
        c.drawString(100, y_position_for_isi_surat - 280, user_id)  # Menampilkan nama pengirim

        # Simpan PDF
        c.save()
        print(f"PDF telah disimpan sebagai {pdf_file_path}")  # Menampilkan jalur lengkap

        # Tampilkan dialog konfirmasi
        self.show_dialog("PDF berhasil dicetak!")
