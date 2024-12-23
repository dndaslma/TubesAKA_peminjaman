import flet as ft
import random
import time
import sys

sys.setrecursionlimit(1000000)

class DataPeminjam:
    def __init__(self, id, nama, status):
        self.id = id
        self.nama = nama
        self.status = status

class PeminjamData:
    def __init__(self):
        self.peminjam_data = []
    
    def proses_pencarian_iteratif(self, status, n):
        start_time = time.time() 
        hasil = []
        for i in range(n):
            if self.peminjam_data[i].status == status:
                hasil.append(f"ID: {self.peminjam_data[i].id}, Nama: {self.peminjam_data[i].nama}, Status: {self.peminjam_data[i].status}")
        end_time = time.time() 
        execution_time = end_time - start_time  
        return hasil
    
    def proses_pencarian_rekursif(self, status, n, i=0, hasil=None):
        if hasil is None:
            hasil = []
        if i >= n:
            return hasil
        start_time = time.time()  
        if self.peminjam_data[i].status == status:
            hasil.append(f"ID: {self.peminjam_data[i].id}, Nama: {self.peminjam_data[i].nama}, Status: {self.peminjam_data[i].status}")
        hasil =  self.proses_pencarian_rekursif(status, n, i + 1, hasil)
        end_time = time.time()  
        execution_time = end_time - start_time  
        return hasil

def main(page: ft.Page):
    page.bgcolor = "#F5F5DC"
    page.title = "Data Peminjaman Buku"
    page.padding = 20

    data = PeminjamData()

    input_method_dropdown = ft.Dropdown(
        label="Metode Input Data",
        options=[ft.dropdown.Option("Manual"), ft.dropdown.Option("Random")],
        width=200,
        bgcolor="#8B4513",
        color="white",
    )

    random_count_input = ft.TextField(
        label="Jumlah Data Random",
        width=150,
        bgcolor="#8B4513",
        color="white",
        border_color="#BEBEBE",
        visible=True,
    )

    id_input = ft.TextField(label="ID (unik)", width=150, bgcolor="#8B4513", color="white", border_color="#BEBEBE")
    nama_input = ft.TextField(label="Nama", width=150, bgcolor="#8B4513", color="white", border_color="#BEBEBE")
    status_dropdown = ft.Dropdown(
        label="Status",
        options=[ft.dropdown.Option("terlambat"), ft.dropdown.Option("tidak terlambat")],
        width=150,
        bgcolor="#8B4513",
        color="white",
    )
    status_search_input = ft.TextField(label="Status yang dicari?", width=250, bgcolor="#8B4513", color="white", border_color="#BEBEBE")
    metode_dropdown = ft.Dropdown(
        label="Pilih Algoritma",
        options=[ft.dropdown.Option("Iteratif"), ft.dropdown.Option("Rekursif")],
        width=200,
        bgcolor="#8B4513",
        color="white",
    )

    hasil_list = ft.ListView(
        expand=True,
        spacing=10,
        height=300, 
    )

    hapus_button = ft.ElevatedButton(
        "Hapus Hasil", on_click=lambda e: hapus_hasil(), bgcolor="#8B4513", color="white", visible=True
    )
    lihat_data_button = ft.ElevatedButton(
        "Lihat Semua Data", on_click=lambda e: lihat_semua_data(), bgcolor="#8B4513", color="white", visible=True
    )

    def update_input_visibility(e):
        random_count_input.visible = input_method_dropdown.value == "Random"
        id_input.visible = nama_input.visible = status_dropdown.visible = input_method_dropdown.value == "Manual"
        page.update()

    def tambah_peminjam(e):
        if input_method_dropdown.value == "Manual":
            id_value = id_input.value.strip()
            nama = nama_input.value.strip()
            status = status_dropdown.value

            if not id_value or not nama or not status:
                hasil_list.controls.append(ft.Text("ID, nama, dan status harus diisi!", color="red"))
            elif any(peminjam.id == id_value for peminjam in data.peminjam_data):
                hasil_list.controls.append(ft.Text("ID sudah digunakan! Harap gunakan ID lain.", color="red"))
            else:
                data.peminjam_data.append(DataPeminjam(id_value, nama, status))
                hasil_list.controls.append(ft.Text(f"Data ditambahkan: ID: {id_value}, Nama: {nama}, Status: {status}", color="green"))
                id_input.value = ""
                nama_input.value = ""
                status_dropdown.value = None
        elif input_method_dropdown.value == "Random":
            try:
                count = int(random_count_input.value)
                if count <= 0:
                    hasil_list.controls.append(ft.Text("Jumlah data harus lebih dari 0.", color="red"))
                else:
                    for _ in range(count):
                        random_id = str(random.randint(1000, 9999))
                        random_name = f"User{random.randint(1, 100)}"
                        random_status = random.choice(["terlambat", "tidak terlambat"])
                        data.peminjam_data.append(DataPeminjam(random_id, random_name, random_status))
                    hasil_list.controls.append(ft.Text(f"{count} data random berhasil ditambahkan.", color="green"))
                    random_count_input.value = ""
            except ValueError:
                hasil_list.controls.append(ft.Text("Masukkan jumlah data yang valid!", color="red"))
        page.update()

    def cari_status(e):
        hasil_list.controls.clear()  
        status = status_search_input.value.strip().lower()
        metode = metode_dropdown.value

        if not status or not metode:
            hasil_list.controls.append(ft.Text("Silakan isi status dan pilih metode!", color="red"))
        elif status not in ["terlambat", "tidak terlambat"]:
            hasil_list.controls.append(ft.Text("Status tidak valid!", color="red"))
        else:
            n = len(data.peminjam_data)

            start_time = time.time()

            if metode == "Iteratif":
                hasil_pencarian = data.proses_pencarian_iteratif(status, n)
            else:
                hasil_pencarian = data.proses_pencarian_rekursif(status, n)

            end_time = time.time()

            execution_time = end_time - start_time

            hasil_list.controls.append(ft.Text(f"Waktu eksekusi: {execution_time:.6f} detik", color="blue"))

            if hasil_pencarian:
                for idx, hasil in enumerate(hasil_pencarian, 1): 
                    hasil_list.controls.append(ft.Text(f"{idx}. {hasil}", color="#8B4513"))
            else:
                hasil_list.controls.append(ft.Text("Tidak ada peminjam dengan status tersebut.", color="red"))
        
            page.update()  


    def hapus_hasil():
        hasil_list.controls.clear()
        page.update()

    def lihat_semua_data():
        hasil_list.controls.clear()
        for idx, peminjam in enumerate(data.peminjam_data, 1): 
            hasil_list.controls.append(ft.Text(f"{idx}. ID: {peminjam.id}, Nama: {peminjam.nama}, Status: {peminjam.status}", color="#8B4513"))
        page.update()

    tambah_button = ft.ElevatedButton("Tambah Data", on_click=tambah_peminjam, bgcolor="#8B4513", color="white", style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)))
    cari_button = ft.ElevatedButton("Cari", on_click=cari_status, bgcolor="#8B4513", color="white", style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)))

    tambah_data_layout = ft.Column(
        [
            ft.Row([ft.Text("Tambah Data", style="headlineMedium", color="black")], alignment="center"),
            ft.Row([input_method_dropdown, random_count_input], alignment="center", spacing=10),
            ft.Row([id_input, nama_input, status_dropdown], alignment="center", spacing=10),
            ft.Row([tambah_button], alignment="center"),
        ],
        spacing=20,
        alignment="center",
    )

    pencarian_layout = ft.Column(
        [
            ft.Row([ft.Text("Pencarian Data", style="headlineMedium", color="black")], alignment="center"),
            ft.Row([status_search_input, metode_dropdown, cari_button], alignment="center", spacing=10),
            ft.Row([hapus_button, lihat_data_button], alignment="center", spacing=10),
        ],
        spacing=20,
        alignment="center",
    )

    page.add(
        ft.Column(
            [
                tambah_data_layout,
                pencarian_layout,
                ft.Container(content=hasil_list, height=300, expand=True, bgcolor="#FFFFFF", padding=10),
            ],
            spacing=30,
            alignment="center",
        )
    )

ft.app(target=main)
