# model
import customtkinter as ctk
from PIL import Image, ImageTk
import sqlite3
from tkinter import messagebox
import tkinter as tk
from tkcalendar import DateEntry
from tkinter import Tk
import datetime
        
class Model:
    def __init__(self, db_name='university.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.initialize_db()
        self.logo_image_path = "logo.png"

    def get_logo_image_path(self):
        return self.logo_image_path
        
    def initialize_db():
        conn = sqlite3.connect('university.db')
        c = conn.cursor()
        c.execute('''
        CREATE TABLE IF NOT EXISTS dosen (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_lengkap TEXT NOT NULL,
            jenis_kelamin TEXT NOT NULL,
            nidn TEXT NOT NULL,
            program_studi TEXT NOT NULL,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
        ''')
        c.execute('''
        CREATE TABLE IF NOT EXISTS mahasiswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_lengkap TEXT NOT NULL,
            jenis_kelamin TEXT NOT NULL,
            angkatan TEXT NOT NULL,
            program_studi TEXT NOT NULL,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            nim TEXT NOT NULL
        )
        ''')
        c.execute('''
        CREATE TABLE IF NOT EXISTS matkul (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kode TEXT NOT NULL,
            nama_matkul TEXT NOT NULL,
            sks INTEGER NOT NULL,
            nama_dosen INTEGER NOT NULL,
            jadwal TEXT NOT NULL,
            ruang_kuliah TEXT NOT NULL,
            program_studi TEXT NOT NULL,
            FOREIGN KEY (nama_dosen) REFERENCES dosen(id)
        )
        ''')
        c.execute('''
        CREATE TABLE IF NOT EXISTS krs_mahasiswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_lengkap TEXT NOT NULL,
            kode_matkul TEXT NOT NULL,
            nama_matkul TEXT NOT NULL,
            sks INTEGER NOT NULL,
            status_approval TEXT DEFAULT 'Pending',  -- Kolom untuk status persetujuan (Pending, Approved, Rejected)
            FOREIGN KEY (nama_lengkap) REFERENCES mahasiswa(username)
        )
        ''')
        c.execute('''
        CREATE TABLE IF NOT EXISTS kehadiran (
            nim TEXT,
            nama_lengkap TEXT,
            tanggal TEXT,
            kehadiran TEXT,
            kode_matkul TEXT
        )
        ''')
        conn.commit()
        conn.close()

    def insert_dosen(self, nama_lengkap, nidn, program_studi, username, password):
        conn = sqlite3.connect('university.db')
        c = conn.cursor()
        c.execute('''
        INSERT INTO dosen (nama_lengkap, nidn, program_studi, username, password)
        VALUES (?, ?, ?, ?, ?)
        ''', (nama_lengkap, nidn, program_studi, username, password))
        conn.commit()
        conn.close()

    def insert_mahasiswa(self, nama_lengkap, angkatan, program_studi, username, password, nim):
        conn = sqlite3.connect('university.db')
        c = conn.cursor()
        c.execute('''
        INSERT INTO mahasiswa (nama_lengkap, angkatan, program_studi, username, password, nim)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (nama_lengkap, angkatan, program_studi, username, password, nim))
        conn.commit()
        conn.close()

    def verify_login(self, username, password):
        conn = sqlite3.connect('university.db')
        c = conn.cursor()
        c.execute('SELECT * FROM dosen WHERE username = ? AND password = ?', (username, password))
        dosen_result = c.fetchone()
        c.execute('SELECT * FROM mahasiswa WHERE username = ? AND password = ?', (username, password))
        mahasiswa_result = c.fetchone()
        conn.close()
        return dosen_result, mahasiswa_result

    def get_student_data(self, username):
            conn = sqlite3.connect('university.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM mahasiswa WHERE username=?", (username,))
            student_data = cursor.fetchone()
            conn.close()
            return student_data

    def get_dosen_data(self, username):
            conn = sqlite3.connect('university.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM dosen WHERE username=?", (username,))
            dosen_data = cursor.fetchone()
            conn.close()
            return dosen_data
        
    def get_lessons(self):
            conn = sqlite3.connect('university.db')
            c = conn.cursor()
            c.execute("SELECT DISTINCT nama_matkul FROM matkul")
            lessons = [row[0] for row in c.fetchall()]
            conn.close()
            return lessons

    def get_courses_by_day(self, day):
            conn = sqlite3.connect('university.db')
            c = conn.cursor()
            c.execute("SELECT kode, nama_matkul, sks, jadwal, ruang_kuliah, nama_dosen FROM matkul WHERE jadwal LIKE ?", (day + '%',))
            courses = c.fetchall()
            conn.close()
            return courses

    def get_all_courses(self):
            conn = sqlite3.connect('university.db')
            c = conn.cursor()
            c.execute("SELECT kode, nama_matkul, sks, jadwal, ruang_kuliah, nama_dosen FROM matkul")
            courses = c.fetchall()
            conn.close()
            return courses
        
    def dapatkan_krs_mahasiswa(self):
            """
            Fetch KRS data for students.
            """
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute('''
                SELECT krs.id, m.nama_matkul, m.sks, m.jadwal, d.nama_dosen, krs.status_approval
                FROM krs_mahasiswa krs
                JOIN matkul m ON krs.matkul_id = m.id
                JOIN dosen d ON m.nama_dosen = d.id
            ''')
            krs_data = c.fetchall()
            conn.close()
            return krs_data

    def dapatkan_matkul_tersedia(self):
            """
            Fetch available courses.
            """
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("SELECT nama_matkul FROM matkul")
            lessons = [row[0] for row in c.fetchall()]
            conn.close()
            return lessons

    def dapatkan_kode_dosen(self):
            """
            Fetch lecturer codes.
            """
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("SELECT id, kode_dosen FROM dosen")
            dosen_codes = c.fetchall()
            conn.close()
            return dosen_codes

    def dapatkan_nama_dosen(self):
            """
            Fetch lecturer names.
            """
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("SELECT id, nama_dosen FROM dosen")
            dosen_names = c.fetchall()
            conn.close()
            return dosen_names

    def dapatkan_matkul_dosen(self, dosen_name):
            """
            Fetch courses for a specific lecturer.
            """
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("SELECT * FROM matkul WHERE nama_dosen = ?", (dosen_name,))
            courses = c.fetchall()
            conn.close()
            return courses

    def dapatkan_semua_mahasiswa(self):
            """
            Fetch all students.
            """
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("SELECT * FROM mahasiswa")
            students = c.fetchall()
            conn.close()
            return students

    def update_approval_status(self, krs_id, status):
            """
            Update the approval status of a KRS entry.
            """
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("UPDATE krs_mahasiswa SET status_approval = ? WHERE id = ?", (status, krs_id))
            conn.commit()
            conn.close()

    def get_courses_for_program(self, program_studi):
        self.cursor.execute("SELECT kode, nama_matkul, sks, nama_dosen, jadwal, ruang_kuliah FROM matkul WHERE program_studi = ?", (program_studi,))
        courses = self.cursor.fetchall()
        return courses

    def get_program_studi(self, username):
        self.cursor.execute("SELECT program_studi FROM mahasiswa WHERE username = ?", (username,))
        program_studi = self.cursor.fetchone()[0]
        return program_studi

    def simpan_krs_mahasiswa(self, nama_lengkap, matkul_list):
        for matkul in matkul_list:
            kode_matkul, nama_matkul, sks = matkul[0], matkul[1], matkul[2]
            self.cursor.execute("INSERT INTO krs_mahasiswa (nama_lengkap, kode_matkul, nama_matkul, sks) VALUES (?, ?, ?, ?)", (nama_lengkap, kode_matkul, nama_matkul, sks))
        self.conn.commit()

    def get_krs_mahasiswa(self):
        self.cursor.execute("SELECT * FROM krs_mahasiswa")
        data_krs = self.cursor.fetchall()
        return data_krs

    def update_approval_status(self, krs_id, status):
        self.cursor.execute("UPDATE krs_mahasiswa SET status_approval = ? WHERE id = ?", (status, krs_id))
        self.conn.commit()

    def close(self):
        self.conn.close()

class KRSModel:
    def get_krs_data(self):
        conn = sqlite3.connect('university.db')
        c = conn.cursor()
        c.execute("SELECT kode, nama_matkul, sks, kelas, pengajar, approval FROM krs_mahasiswa WHERE status_approval = 'Approved'")
        data = c.fetchall()
        conn.close()
        return data

class JadwalModel:
    def get_lesson_options(self):
        conn = sqlite3.connect('university.db')
        c = conn.cursor()
        c.execute("SELECT DISTINCT nama_matkul FROM matkul")
        lessons = [row[0] for row in c.fetchall()]
        conn.close()
        return lessons

    def get_schedule_today(self, day):
        conn = sqlite3.connect('university.db')
        c = conn.cursor()
        c.execute("SELECT kode, nama_matkul, sks, jadwal, ruang_kuliah, nama_dosen FROM matkul WHERE jadwal LIKE ?", (day + '%',))
        courses = c.fetchall()
        conn.close()
        return courses

    def get_weekly_schedule(self):
        conn = sqlite3.connect('university.db')
        c = conn.cursor()
        c.execute("SELECT kode, nama_matkul, sks, jadwal, ruang_kuliah, nama_dosen FROM matkul")
        courses = c.fetchall()
        conn.close()
        return courses

class HasilStudiModel:
    def get_hasil_studi_data(self):
        conn = sqlite3.connect('university.db')
        c = conn.cursor()
        c.execute("SELECT kode_matkul, nama_matkul, sks, grade, score FROM krs_mahasiswa WHERE status_approval = 'Approved'")
        data = c.fetchall()
        conn.close()
        return data

class KehadiranModel:
    def get_kehadiran_data(self):
        conn = sqlite3.connect('university.db')
        c = conn.cursor()
        c.execute("SELECT kode_matkul, nama_matkul, sks FROM krs_mahasiswa WHERE status_approval = 'Approved'")
        data = c.fetchall()
        conn.close()
        return data

    def get_kehadiran_summary(self):
        conn = sqlite3.connect('university.db')
        c = conn.cursor()
        summary = {}
        c.execute("SELECT COUNT(*) FROM kehadiran WHERE kehadiran = 'Hadir'")
        summary['total_hadir'] = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM kehadiran WHERE kehadiran = 'Tidak Hadir'")
        summary['total_tidak_hadir'] = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM kehadiran WHERE kehadiran = 'Izin'")
        summary['total_izin'] = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM kehadiran WHERE kehadiran = 'Sakit'")
        summary['total_sakit'] = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM kehadiran WHERE kehadiran = 'Alfa'")
        summary['total_alfa'] = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM kehadiran")
        summary['total_record'] = c.fetchone()[0]
        conn.close()
        return summary

def fetch_classes(self):
    conn = sqlite3.connect(self.db_path)
    c = conn.cursor()
    c.execute("SELECT nama_matkul, kode FROM matkul")
    class_options = [(row[0], row[1]) for row in c.fetchall()]
    conn.close()
    return class_options

def fetch_students(self):
    conn = sqlite3.connect(self.db_path)
    c = conn.cursor()
    c.execute("SELECT nim, nama_lengkap FROM mahasiswa")
    students = c.fetchall()
    conn.close()
    return students

def save_attendance(self, attendance_records):
    conn = sqlite3.connect(self.db_path)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS kehadiran (
            nim TEXT,
            nama_lengkap TEXT,
            tanggal TEXT,
            kehadiran TEXT,
            kode_matkul TEXT
        )
    ''')
    c.executemany('INSERT INTO kehadiran (nim, nama_lengkap, tanggal, kehadiran, kode_matkul) VALUES (?, ?, ?, ?, ?)', attendance_records)
    conn.commit()
    conn.close()

def fetch_student_names(self):
    conn = sqlite3.connect(self.db_path)
    c = conn.cursor()
    c.execute("SELECT nama_lengkap FROM mahasiswa")
    students = c.fetchall()
    conn.close()
    return students

def update_grades(self, penilaian_data, course_code):
    conn = sqlite3.connect(self.db_path)
    c = conn.cursor()
    for student_name, grade, score in penilaian_data:
        c.execute("""
            UPDATE krs_mahasiswa 
            SET grade = ?, score = ? 
            WHERE nama_lengkap = ? AND kode_matkul = ?
        """, (grade, score, student_name, course_code))
    conn.commit()
    conn.close()

def get_distinct_lessons(self):
    self.connect()
    self.c.execute("SELECT DISTINCT nama_matkul FROM matkul")
    lessons = [row[0] for row in self.c.fetchall()]
    self.disconnect()
    return lessons

def get_courses_for_day(self, day):
    self.connect()
    self.c.execute("SELECT kode, nama_matkul, sks, jadwal, ruang_kuliah, nama_dosen FROM matkul WHERE jadwal LIKE ?", (day + '%',))
    courses = self.c.fetchall()
    self.disconnect()
    return courses

def get_all_courses(self):
    self.connect()
    self.c.execute("SELECT kode, nama_matkul, sks, jadwal, ruang_kuliah, nama_dosen FROM matkul")
    courses = self.c.fetchall()
    self.disconnect()
    return courses

bg_color = "#3E0A0A"
fg_color = "#FFFFFF"
highlight_color = "#8C1C1C"

# view
class View:
    def __init__(self, controller):
        self.controller = controller
        self.app = ctk.CTk()
        self.app.title("UNIVERSITAS INDOSAT")
        self.app.geometry("{0}x{1}+0+0".format(self.app.winfo_screenwidth(), self.app.winfo_screenheight()))
        self.app.configure(bg="white")
        self.fullscreen_frame = ctk.CTkFrame(self.app, fg_color="white", bg_color="white")
        self.fullscreen_frame.pack(fill="both", expand=True)
        self.center_frame = ctk.CTkFrame(self.fullscreen_frame, fg_color="white", bg_color="white")
        self.center_frame.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
        self.title_label = ctk.CTkLabel(self.center_frame, text="UNIVERSITAS INDOSAT", font=ctk.CTkFont(family="Helvetica", size=48, weight="bold"), text_color="black", bg_color="white")
        self.title_label.pack(pady=20)
        logo_image_path = "logo.png"
        logo_image = Image.open(logo_image_path)
        logo_image = logo_image.resize((300, 300), Image.LANCZOS)
        self.logo_photo = ImageTk.PhotoImage(logo_image)
        self.logo_label = ctk.CTkLabel(self.center_frame, image=self.logo_photo, text="", bg_color="white")
        self.logo_label.pack(pady=20)
        button_font = ctk.CTkFont(size=20)
        self.register_dosen_button = ctk.CTkButton(self.center_frame, text="Registrasi Dosen", fg_color="white", hover_color="light grey", border_width=2, border_color="#800000", text_color="#800000", font=button_font, width=300, height=60, bg_color="white", command=lambda: self.controller.open_registration_window("Registrasi Dosen"))
        self.register_dosen_button.pack(pady=10)
        self.register_mahasiswa_button = ctk.CTkButton(self.center_frame, text="Registrasi Mahasiswa", hover_color="light grey", fg_color="white", border_width=2, border_color="#800000", text_color="#800000", font=button_font, width=300, height=60, bg_color="white", command=lambda: self.controller.open_registration_window("Registrasi Mahasiswa"))
        self.register_mahasiswa_button.pack(pady=10)
        self.login_button = ctk.CTkButton(self.center_frame, text="Login", fg_color="#800000", hover_color="#500000", text_color="white", font=button_font, width=300, height=60, bg_color="white", command=self.controller.open_login_window)
        self.login_button.pack(pady=10)
     
    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def show_pengisian_krs(self, username, data_pilihan):
        self.clear_frame(self.content_frame)

        krs_title = ctk.CTkLabel(self.content_frame, text="Pengisian Kartu Rencana Studi", font=("Arial", 20, "bold"), text_color="#5C0A0A")
        krs_title.pack(pady=10)

        notif_frame = ctk.CTkFrame(self.content_frame, corner_radius=10, fg_color="#FFFFFF")
        notif_frame.pack(pady=10, padx=10, fill="x")

        header_frame = ctk.CTkFrame(notif_frame, fg_color="#5C0A0A")
        header_frame.grid(row=0, column=0, columnspan=3, sticky="nsew")

        header_label = ctk.CTkLabel(header_frame, text="Notifikasi", font=ctk.CTkFont(size=14, weight="bold"), text_color="#FFFFFF")
        header_label.pack(padx=5, pady=5, anchor="w")

        notif_data = [
            ("Batas Waktu Pengisian KRS", "30-08-2025"),
            ("Informasi Tambahan", "Pastikan Anda menyelesaikan pengisian KRS sebelum batas waktu yang ditentukan."),
        ]

        for i, (key, value) in enumerate(notif_data, start=1):
            key_label = ctk.CTkLabel(notif_frame, text=key, anchor="w", fg_color="#FFFFFF", text_color="#000000")
            key_label.grid(row=i, column=0, padx=5, pady=5, sticky="nsew")
            
            value_label = ctk.CTkLabel(notif_frame, text=value, anchor="w", fg_color="#FFFFFF", text_color="#000000")
            value_label.grid(row=i, column=1, padx=5, pady=5, sticky="nsew", columnspan=2)

        notif_frame.columnconfigure(0, weight=1)
        notif_frame.columnconfigure(1, weight=1)
        notif_frame.columnconfigure(2, weight=2)

        table_frame = ctk.CTkFrame(self.content_frame, corner_radius=10, fg_color="#FFFFFF")
        table_frame.pack(pady=10, padx=10, fill="x")

        columns = ["Kode", "Mata Kuliah", "SKS", "Pengajar", "Jadwal", "Ruang Kuliah", "Status", "Aksi"]
        header_bg_color = "#5C0A0A"
        header_text_color = "#FFFFFF"

        data = []

        form_frame = ctk.CTkFrame(self.content_frame, corner_radius=10, fg_color="#FFFFFF")
        form_frame.pack(pady=10, padx=10, fill="x")

        ctk.CTkLabel(form_frame, text="Pilih Mata Kuliah:", anchor="w", fg_color="#FFFFFF", text_color="#000000").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        course_combo = ctk.CTkComboBox(form_frame, values=[item[1] for item in data_pilihan], fg_color="#FFFFFF", text_color="#000000")
        course_combo.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        def add_to_table():
            selected_course = course_combo.get()
            selected_course_data = next((item for item in data_pilihan if item[1] == selected_course), None)
            if selected_course_data:
                new_row = list(selected_course_data)
                new_row.append("")  # Placeholder for Action column
                data.append(new_row)
                update_table()
                update_total_sks()

        add_btn = ctk.CTkButton(form_frame, text="Tambah", fg_color="#3E0A0A", command=add_to_table)
        add_btn.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        total_sks_frame = ctk.CTkFrame(self.content_frame, fg_color="#FFFFFF")
        total_sks_frame.pack(pady=10, padx=10, fill="x")

        total_sks_label = ctk.CTkLabel(total_sks_frame, text="Total SKS yang Diambil", anchor="w", fg_color="#FFFFFF", text_color="#000000")
        total_sks_label.grid(row=0, column=0, padx=1, pady=5, sticky="w")

        total_sks_value = ctk.CTkLabel(total_sks_frame, text="0", anchor="e", fg_color="#FFFFFF", text_color="#000000")
        total_sks_value.grid(row=0, column=1, padx=1, pady=5, sticky="e")

        total_sks_frame.columnconfigure(0, weight=1)
        total_sks_frame.columnconfigure(1, weight=0)

        def delete_row(row_index):
            data.pop(row_index)
            update_table()
            update_total_sks()

        def update_table():
            for widget in table_frame.winfo_children():
                if isinstance(widget, ctk.CTkLabel) or isinstance(widget, ctk.CTkButton):
                    widget.destroy()

            for col in columns:
                col_label = ctk.CTkLabel(table_frame, text=col, anchor="w", fg_color=header_bg_color, text_color=header_text_color, width=10)
                col_label.grid(row=0, column=columns.index(col), padx=1, pady=5, sticky="nsew")

            for i, row in enumerate(data, start=1):
                for j, val in enumerate(row):
                    cell = ctk.CTkLabel(table_frame, text=val, anchor="w", fg_color="#FFFFFF", text_color="#000000")
                    cell.grid(row=i, column=j, padx=1, pady=5, sticky="nsew")
                    if j == len(row) - 1:
                        del_btn = ctk.CTkButton(table_frame, text="🗑️", width=10, fg_color="#FFFFFF", text_color="#000000", command=lambda r=i-1: delete_row(r))
                        del_btn.grid(row=i, column=j, padx=1, pady=5)

        def update_total_sks():
            total_sks = sum(row[2] for row in data)
            total_sks_value.configure(text=str(total_sks))

        def submit_krs():
            self.controller.submit_krs(username, data)

        submit_btn = ctk.CTkButton(self.content_frame, text="Submit", fg_color="#3E0A0A", command=submit_krs)
        submit_btn.pack(pady=20)

        update_table()

    def show_krs_dosen(self, data_krs):
        self.clear_frame(self.content_frame)

        krs_title = ctk.CTkLabel(self.content_frame, text="KRS", font=("Arial", 20, "bold"), text_color="#5C0A0A")
        krs_title.pack(pady=10)

        table_frame = ctk.CTkFrame(self.content_frame, corner_radius=10, fg_color="#FFFFFF")
        table_frame.pack(pady=10, padx=10, fill="x")

        columns = ["No.", "Nama Mahasiswa", "Kode Matkul", "Nama Matkul", "SKS", "Status Approval", "Approve", "Tidak Approve"]
        header_bg_color = "#5C0A0A"
        header_text_color = "#FFFFFF"
        for col in columns:
            col_label = ctk.CTkLabel(table_frame, text=col, anchor="w", fg_color=header_bg_color, text_color=header_text_color, width=10)
            col_label.grid(row=0, column=columns.index(col), padx=1, pady=5, sticky="nsew")

        for i, row_data in enumerate(data_krs, start=1):
            for j, val in enumerate(row_data):
                cell = ctk.CTkLabel(table_frame, text=val, anchor="w", fg_color="#FFFFFF", text_color="#000000")
                cell.grid(row=i, column=j, padx=1, pady=5, sticky="nsew")

            krs_id = row_data[0]

            approve_btn = ctk.CTkButton(table_frame, text="Approve", fg_color="#3E8E41", text_color="#FFFFFF",
                                        command=lambda k=krs_id: self.controller.update_approval_status(k, "Approved"))
            approve_btn.grid(row=i, column=len(columns) - 2, padx=1, pady=5)

            disapprove_btn = ctk.CTkButton(table_frame, text="Tidak Approve", fg_color="#E8453C", text_color="#FFFFFF",
                                           command=lambda k=krs_id: self.controller.update_approval_status(k, "Tidak Approved"))
            disapprove_btn.grid(row=i, column=len(columns) - 1, padx=1, pady=5)

        for i in range(len(columns)):
            table_frame.columnconfigure(i, weight=1)

    def show_kartu_rencana_studi(self, data_krs):
        self.clear_frame(self.content_frame)

        krs_title = ctk.CTkLabel(self.content_frame, text="Menampilkan Kartu Rencana Studi", font=("Arial", 20, "bold"), text_color="#5C0A0A")
        krs_title.pack(pady=10)

        table_frame = ctk.CTkFrame(self.content_frame, corner_radius=10, fg_color="#FFFFFF")
        table_frame.pack(pady=10, padx=10, fill="x")

        columns = ["Kode", "Mata Kuliah", "SKS", "Kelas", "Pengajar", "Approval"]
        header_bg_color = "#5C0A0A"
        header_text_color = "#FFFFFF"
        for col in columns:
            col_label = ctk.CTkLabel(table_frame, text=col, anchor="w", fg_color=header_bg_color, text_color=header_text_color, width=10)
            col_label.grid(row=0, column=columns.index(col), padx=1, pady=5, sticky="nsew")

        for i, row_data in enumerate(data_krs, start=1):
            for j, val in enumerate(row_data[1:]):
                cell = ctk.CTkLabel(table_frame, text=val, anchor="w", fg_color="#FFFFFF", text_color="#000000")
                cell.grid(row=i, column=j, padx=1, pady=5, sticky="nsew")

        for i in range(len(columns)):
            table_frame.columnconfigure(i, weight=1)

class RegistrationView:
    def __init__(self, controller, title, fields, submit_callback):
        self.controller = controller
        self.reg_window = ctk.CTk()
        self.reg_window.title(title)
        self.reg_window.geometry("{0}x{1}+0+0".format(self.reg_window.winfo_screenwidth(), self.reg_window.winfo_screenheight()))
        self.reg_window.configure(bg="white")
        self.reg_fullscreen_frame = ctk.CTkFrame(self.reg_window, fg_color="white", bg_color="white")
        self.reg_fullscreen_frame.pack(fill="both", expand=True)
        self.reg_center_frame = ctk.CTkFrame(self.reg_fullscreen_frame, fg_color="white", bg_color="white")
        self.reg_center_frame.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
        back_button = ctk.CTkButton(self.reg_fullscreen_frame, text="← Back", fg_color="grey", hover_color="#500000", text_color="white", font=ctk.CTkFont(size=20), width=100, height=40, bg_color="white", command=self.controller.back_to_main)
        back_button.place(x=20, y=20)
        reg_title_label = ctk.CTkLabel(self.reg_center_frame, text="UNIVERSITAS INDOSAT", font=ctk.CTkFont(family="Helvetica", size=48, weight="bold"), text_color="black", bg_color="white")
        reg_title_label.pack(pady=20)
        logo_image_path = "logo.png"
        logo_image = Image.open(logo_image_path)
        logo_image = logo_image.resize((300, 300), Image.LANCZOS)
        self.logo_photo = ImageTk.PhotoImage(logo_image)
        reg_logo_label = ctk.CTkLabel(self.reg_center_frame, image=self.logo_photo, text="", bg_color="white")
        reg_logo_label.pack(pady=20)
        reg_form_title_label = ctk.CTkLabel(self.reg_center_frame, text=title, font=ctk.CTkFont(family="Helvetica", size=36, weight="bold"), text_color="black", bg_color="white")
        reg_form_title_label.pack(pady=20)
        self.entries = {}
        for field in fields:
            entry = ctk.CTkEntry(self.reg_center_frame, placeholder_text=field, width=400, height=40, fg_color="#FFFFFF", text_color="black")
            entry.pack(pady=10)
            self.entries[field] = entry
        submit_button = ctk.CTkButton(self.reg_center_frame, text="Sign Up", fg_color="#800000", hover_color="#500000", text_color="white", font=ctk.CTkFont(size=20), width=300, height=60, bg_color="white", command=submit_callback)
        submit_button.pack(pady=20)

    def show_message(self, message, callback):
        self.reg_center_frame.pack_forget()
        message_frame = ctk.CTkFrame(self.reg_fullscreen_frame, fg_color="white", bg_color="white", border_color="black", border_width=2)
        message_frame.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
        message_frame.configure(width=450, height=200)
        message_frame.pack_propagate(False)
        message_label = ctk.CTkLabel(message_frame, text=message, font=ctk.CTkFont(family="Helvetica", size=25, weight="bold"), text_color="black", bg_color="white")
        message_label.pack(pady=20)
        back_button = ctk.CTkButton(message_frame, text="Kembali ke Menu Utama", fg_color="#800000", hover_color="#500000", text_color="white", font=ctk.CTkFont(size=20), width=250, height=60, bg_color="white", command=callback)
        back_button.pack(pady=20)

    def get_entry_data(self):
        return {field: entry.get() for field, entry in self.entries.items()}

    def close(self):
        self.reg_window.destroy()

class LoginView:
    def __init__(self, root, controller):
        self.controller = controller
        self.root = root
        self.root.title("Login")
        self.root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
        self.root.configure(bg="white")

        login_fullscreen_frame = ctk.CTkFrame(root, fg_color="white", bg_color="white")
        login_fullscreen_frame.pack(fill="both", expand=True)

        self.login_center_frame = ctk.CTkFrame(login_fullscreen_frame, fg_color="white", bg_color="white")
        self.login_center_frame.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        back_button = ctk.CTkButton(login_fullscreen_frame, text="← Back", fg_color="grey", hover_color="#500000", text_color="white", font=("Arial", 14), width=100, height=40, bg_color="white", command=self.controller.back_to_main)
        back_button.place(x=20, y=20)

        login_title_label = ctk.CTkLabel(self.login_center_frame, text="UNIVERSITAS INDOSAT", font=ctk.CTkFont(family="Helvetica", size=48, weight="bold"), text_color="black", bg_color="white")
        login_title_label.pack(pady=20)

        login_logo_image = Image.open("logo.png")
        login_logo_image = login_logo_image.resize((300, 300), Image.LANCZOS)
        login_logo_photo = ImageTk.PhotoImage(login_logo_image)
        login_logo_label = ctk.CTkLabel(self.login_center_frame, image=login_logo_photo, text="", bg_color="white")
        login_logo_label.pack(pady=20)

        login_form_title_label = ctk.CTkLabel(self.login_center_frame, text="Login", font=ctk.CTkFont(family="Helvetica", size=36, weight="bold"), text_color="black", bg_color="white")
        login_form_title_label.pack(pady=20)

        self.username_entry = ctk.CTkEntry(self.login_center_frame, placeholder_text="Username", width=400, height=40, fg_color="#FFFFFF", text_color="black")
        self.username_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(self.login_center_frame, placeholder_text="Password", width=400, height=40, fg_color="#FFFFFF", text_color="black", show='*')
        self.password_entry.pack(pady=10)

        login_button = ctk.CTkButton(self.login_center_frame, text="Login", fg_color="#800000", hover_color="#500000", text_color="white", font=("Arial", 20), width=300, height=60, bg_color="white", command=self.verify_login)
        login_button.pack(pady=20)

    def verify_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.controller.verify_login(username, password)

class DashboardView:
    def __init__(self, root, controller, username):
        self.controller = controller
        self.username = username
        self.root = root
        self.root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
        self.root.title("Sistem Akademik Universitas")

        bg_color = "#3E0A0A"
        fg_color = "#FFFFFF"
        highlight_color = "#8C1C1C"

        self.root.configure(bg="#FFFFFF")

        self.nav_frame = ctk.CTkFrame(self.root, width=250, corner_radius=0, fg_color=bg_color)
        self.nav_frame.pack(side="left", fill="y")

        logo_image = Image.open("logo.png")
        logo_image = logo_image.resize((220, 220), Image.LANCZOS)
        logo_photo = ImageTk.PhotoImage(logo_image)
        logo_label = tk.Label(self.nav_frame, image=logo_photo, anchor="center", bg=bg_color)
        logo_label.pack(pady=10)

        university_name_label = ctk.CTkLabel(self.nav_frame, text="Universitas Indosat", anchor="center", font=("Arial", 14, "bold"), text_color=fg_color)
        university_name_label.pack(pady=10)

        student_data = self.controller.get_student_data(username)
        user_label = ctk.CTkLabel(self.nav_frame, text=f"{student_data[1]} (Mahasiswa)", anchor="w", text_color=fg_color, font=("Arial", 14))
        user_label.pack(pady=20, padx=20)

        buttons = [
            ("Dashboard", lambda: self.controller.show_dashboard_content(self.content_frame, username)),
            ("Pengisian KRS", lambda: self.controller.show_pengisian_krs(self.content_frame, username)),
            ("Kartu Rencana Studi", lambda: self.controller.show_kartu_rencana_studi(self.content_frame, username)),
            ("Jadwal Kuliah", lambda: self.controller.show_jadwal_kuliah(self.content_frame, username)),
            ("Hasil Studi", lambda: self.controller.show_hasil_studi(self.content_frame, username)),
            ("Kehadiran Mahasiswa", lambda: self.controller.show_kehadiran_mahasiswa(self.content_frame, username))
        ]

        for button_text, command in buttons:
            btn = ctk.CTkButton(self.nav_frame, text=button_text, anchor="w", fg_color=highlight_color, hover_color="#c41212", font=("Arial", 20), command=command)
            btn.pack(fill="x", pady=5, padx=10)

        self.content_frame = ctk.CTkFrame(self.root, corner_radius=0, fg_color="#FFFFFF")
        self.content_frame.pack(side="right", fill="both", expand=True)

        top_frame = ctk.CTkFrame(self.content_frame, fg_color="#FFFFFF")
        top_frame.pack(fill="x", pady=10, padx=10)

        logout_button = ctk.CTkButton(top_frame, text="Log Out", fg_color="#FFFFFF", text_color="#000000", hover_color="light grey", font=("Arial", 14), command=self.controller.logout)
        logout_button.pack(side="right", padx=10, pady=10)

        self.controller.show_dashboard_content(self.content_frame, username)

class KRSView:
    def display_krs(self, frame, data):
        # Clear existing content in the frame
        for widget in frame.winfo_children():
            widget.destroy()

        title = ctk.CTkLabel(frame, text="Menampilkan Kartu Rencana Studi", font=("Arial", 20, "bold"), text_color="#5C0A0A")
        title.pack(pady=10)

        table_frame = ctk.CTkFrame(frame, corner_radius=10, fg_color="#FFFFFF")
        table_frame.pack(pady=10, padx=10, fill="x")

        columns = ["Kode", "Mata Kuliah", "SKS", "Kelas", "Pengajar", "Approval"]
        header_bg_color = "#5C0A0A"
        header_text_color = "#FFFFFF"
        for col in columns:
            col_label = ctk.CTkLabel(table_frame, text=col, anchor="w", fg_color=header_bg_color, text_color=header_text_color, width=10)
            col_label.grid(row=0, column=columns.index(col), padx=1, pady=5, sticky="nsew")

        for i, row_data in enumerate(data, start=1):
            for j, val in enumerate(row_data):
                cell = ctk.CTkLabel(table_frame, text=val, anchor="w", fg_color="#FFFFFF", text_color="#000000")
                cell.grid(row=i, column=j, padx=1, pady=5, sticky="nsew")

        for i in range(len(columns)):
            table_frame.columnconfigure(i, weight=1)

class JadwalView:
    def display_jadwal(self, frame, lessons):
        for widget in frame.winfo_children():
            widget.destroy()

        title = ctk.CTkLabel(frame, text="Jadwal Kuliah", font=("Arial", 20, "bold"), text_color=bg_color)
        title.pack(pady=10)

        info = ctk.CTkLabel(frame, text="Pilih Mata Kuliah:", font=("Arial", 16), text_color=bg_color)
        info.pack(pady=10)

        selected_lesson = ctk.StringVar(value=lessons[0])
        lesson_dropdown = ctk.CTkComboBox(frame, values=lessons, variable=selected_lesson, font=("Arial", 14), text_color="black", fg_color="white")
        lesson_dropdown.pack(pady=10)
        return selected_lesson, lesson_dropdown

    def display_schedule(self, frame, title_text, courses, headers):
        for widget in frame.winfo_children():
            widget.destroy()

        date_frame = ctk.CTkFrame(frame, fg_color=highlight_color)
        date_frame.pack(fill="x", padx=10, pady=5)
        date_label = ctk.CTkLabel(date_frame, text=title_text, font=("Arial", 14, "bold"), text_color=fg_color)
        date_label.pack(pady=5)

        if not courses:
            no_class_label = ctk.CTkLabel(date_frame, text="No classes scheduled", text_color=fg_color)
            no_class_label.pack()
        else:
            header_frame = ctk.CTkFrame(frame, fg_color=highlight_color)
            header_frame.pack(fill="x")
            for header in headers:
                header_label = ctk.CTkLabel(header_frame, text=header, anchor="w", text_color=fg_color, padx=5, pady=5)
                header_label.pack(side="left", expand=True, fill="x")

            for course in courses:
                row_frame = ctk.CTkFrame(frame, fg_color="#FFFFFF")
                row_frame.pack(fill="x", padx=5, pady=2)
                for value in course:
                    cell_label = ctk.CTkLabel(row_frame, text=value, anchor="w", text_color="black", padx=5, pady=5)
                    cell_label.pack(side="left", expand=True, fill="x")

class HasilStudiView:
    def display_hasil_studi(self, frame, data, ip_semester, ip_kumulatif, status):
        for widget in frame.winfo_children():
            widget.destroy()

        title = ctk.CTkLabel(frame, text="Hasil Studi Mahasiswa", font=("Arial", 20, "bold"), text_color=bg_color)
        title.pack(pady=10)

        table_frame = ctk.CTkFrame(frame, corner_radius=10, fg_color="#FFFFFF")
        table_frame.pack(pady=10, padx=10, fill="x")

        columns = ['Kode', 'Mata Kuliah', 'SKS', 'Grade', 'Score']
        header_bg_color = "#5C0A0A"
        header_text_color = "#FFFFFF"
        for col in columns:
            col_label = ctk.CTkLabel(table_frame, text=col, anchor="w", fg_color=header_bg_color, text_color=header_text_color, width=10)
            col_label.grid(row=0, column=columns.index(col), padx=1, pady=5, sticky="nsew")

        for i, row_data in enumerate(data, start=1):
            for j, val in enumerate(row_data):
                cell = ctk.CTkLabel(table_frame, text=val, anchor="w", fg_color="#FFFFFF", text_color="#000000")
                cell.grid(row=i, column=j, padx=1, pady=5, sticky="nsew")

        additional_table_frame = ctk.CTkFrame(frame, corner_radius=10, fg_color="#FFFFFF")
        additional_table_frame.pack(pady=10, padx=10, fill="x")

        additional_labels = ['IP Semester', 'IP Kumulatif', 'Status Akademik']
        additional_entries = {'IP Semester': ip_semester, 'IP Kumulatif': ip_kumulatif, 'Status Akademik': status}

        for i, label in enumerate(additional_labels):
            label_widget = ctk.CTkLabel(additional_table_frame, text=label, anchor="w", fg_color=header_bg_color, text_color=header_text_color, width=10)
            label_widget.grid(row=0, column=i, padx=1, pady=5, sticky="nsew")
            entry_widget = ctk.CTkLabel(additional_table_frame, text=additional_entries[label], anchor="w", fg_color="#FFFFFF", text_color="#000000")
            entry_widget.grid(row=1, column=i, padx=1, pady=5, sticky="nsew")

        for i in range(len(additional_labels)):
            additional_table_frame.columnconfigure(i, weight=1)

class KehadiranView:
    def display_kehadiran(self, frame, data):
        for widget in frame.winfo_children():
            widget.destroy()

        title = ctk.CTkLabel(frame, text="Kehadiran Mahasiswa", font=("Arial", 20, "bold"), text_color="#5C0A0A")
        title.pack(pady=10)

        table_frame = ctk.CTkFrame(frame, corner_radius=10, fg_color="#FFFFFF")
        table_frame.pack(pady=10, padx=10, fill="x")

        columns = ['Kode Mata Kuliah', 'Nama Mata Kuliah', 'SKS']
        header_bg_color = "#5C0A0A"
        header_text_color = "#FFFFFF"
        for col in columns:
            col_label = ctk.CTkLabel(table_frame, text=col, anchor="w", fg_color=header_bg_color, text_color=header_text_color, width=10)
            col_label.grid(row=0, column=columns.index(col), padx=1, pady=5, sticky="nsew")

        for i, row_data in enumerate(data, start=1):
            for j, val in enumerate(row_data):
                cell = ctk.CTkLabel(table_frame, text=val, anchor="w", fg_color="#FFFFFF", text_color="#000000")
                cell.grid(row=i, column=j, padx=1, pady=5, sticky="nsew")

        for i in range(len(columns)):
            table_frame.columnconfigure(i, weight=1)

    def display_kehadiran_summary(self, frame, summary):
        total_hadir = summary['total_hadir']
        total_tidak_hadir = summary['total_tidak_hadir']
        total_izin = summary['total_izin']
        total_sakit = summary['total_sakit']
        total_alfa = summary['total_alfa']
        total_record = summary['total_record']
        
        for widget in frame.winfo_children():
            widget.destroy()

        summary_title = ctk.CTkLabel(frame, text="Summary Kehadiran", font=("Arial", 16, "bold"), text_color="#5C0A0A")
        summary_title.pack(pady=5)

        summary_labels = {
            "Hadir": total_hadir,
            "Tidak Hadir": total_tidak_hadir,
            "Izin": total_izin,
            "Sakit": total_sakit,
            "Alfa": total_alfa,
            "Total Record": total_record,
        }

        for label, value in summary_labels.items():
            label_widget = ctk.CTkLabel(frame, text=f"{label}: {value}", font=("Arial", 14), text_color="#5C0A0A")
            label_widget.pack(pady=2)

#edit
class ViewKehadiranMahasiswaDosen:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.content_frame = ctk.CTkFrame(self.root)
        self.content_frame.pack(fill="both", expand=True)
        self.student_frame = ctk.CTkFrame(self.content_frame, fg_color="#FFFFFF")

    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def show_kehadiran_mahasiswa_dosen(self):
        self.clear_frame(self.content_frame)
        kehadiran_title = ctk.CTkLabel(self.content_frame, text="Kehadiran Mahasiswa", font=("Arial", 20, "bold"), text_color=bg_color)
        kehadiran_title.pack(pady=10)
        kehadiran_info = ctk.CTkLabel(self.content_frame, text="Pilih Kelas:", font=("Arial", 16), text_color=bg_color)
        kehadiran_info.pack(pady=10)

        class_options = self.controller.fetch_classes()
        selected_class = ctk.StringVar(value=class_options[0][0])
        selected_class_code = ctk.StringVar(value=class_options[0][1])

        class_dropdown = ctk.CTkComboBox(self.content_frame, values=[option[0] for option in class_options], variable=selected_class, font=("Arial", 14), text_color="black", fg_color="white")
        class_dropdown.pack(pady=10)

        def update_selected_class_code(*args):
            for option in class_options:
                if option[0] == selected_class.get():
                    selected_class_code.set(option[1])
                    break

        selected_class.trace("w", update_selected_class_code)

        show_students_button = ctk.CTkButton(self.content_frame, text="Tampilkan Mahasiswa", fg_color=highlight_color, text_color=fg_color, font=("Arial", 14), command=self.controller.show_students)
        show_students_button.pack(pady=10)

        self.student_frame = ctk.CTkFrame(self.content_frame, fg_color="#FFFFFF")
        self.student_frame.pack(fill="both", expand=True)

    def display_students(self, students):
        self.clear_frame(self.student_frame)
        headers = ["NIM", "Nama", "Tanggal", "Kehadiran"]
        header_frame = ctk.CTkFrame(self.student_frame, fg_color=highlight_color)
        header_frame.pack(fill="x")
        for header in headers:
            header_label = ctk.CTkLabel(header_frame, text=header, anchor="w", text_color=fg_color)
            header_label.pack(side="left", padx=5, pady=5, expand=True)

        student_entries = []
        for student in students:
            student_row = ctk.CTkFrame(self.student_frame, fg_color="#FFFFFF")
            student_row.pack(fill="x")
            nim_label = ctk.CTkLabel(student_row, text=student[0], anchor="w", text_color="black")
            nim_label.pack(side="left", padx=5, pady=5, expand=True)
            name_label = ctk.CTkLabel(student_row, text=student[1], anchor="w", text_color="black")
            name_label.pack(side="left", padx=5, pady=5, expand=True)
            date_entry = DateEntry(student_row, width=12, background='darkblue', foreground='white', borderwidth=2)
            date_entry.pack(side="left", padx=5, pady=5)
            presence_var = ctk.StringVar(value="Hadir")
            presence_dropdown = ctk.CTkComboBox(student_row, values=["Hadir", "Tidak Hadir"], variable=presence_var, width=120, text_color="black")
            presence_dropdown.pack(side="left", padx=5, pady=5)
            student_entries.append((nim_label, name_label, date_entry, presence_dropdown))

        # save_button = ctk.CTkButton(self.student_frame, text="Simpan Kehadiran", fg_color=highlight_color, text_color=fg_color, font=("Arial", 14), command=lambda: self.controller.save_attendance(student_entries, selected_class_code.get()))
        # save_button.pack(pady=10)

    def show_penilaian(self):
        self.clear_frame(self.content_frame)
        penilaian_title = ctk.CTkLabel(self.content_frame, text="Penilaian", font=("Arial", 20, "bold"), text_color=bg_color)
        penilaian_title.pack(pady=10)
        selection_frame = ctk.CTkFrame(self.content_frame, fg_color="#FFFFFF")
        selection_frame.pack(pady=10, padx=10, fill="x")

        class_options = self.controller.fetch_class_names()
        selected_class = ctk.StringVar(value=class_options[0])
        lesson_label = ctk.CTkLabel(selection_frame, text="Pilih Mata Kuliah:", font=("Arial", 14), text_color=bg_color)
        lesson_label.pack(side="left", padx=5, pady=5)
        lesson_dropdown = ctk.CTkComboBox(selection_frame, values=class_options, variable=selected_class, font=("Arial", 14), text_color="black", fg_color="white")
        lesson_dropdown.pack(side="left", padx=5, pady=5)

        show_button = ctk.CTkButton(self.content_frame, text="Tampilkan Mahasiswa", command=self.controller.show_student_table, fg_color=highlight_color, hover_color="#c41212", font=("Arial", 14))
        show_button.pack(pady=10)

        self.student_frame = ctk.CTkFrame(self.content_frame, fg_color="#FFFFFF")
        self.student_frame.pack(pady=10, padx=10, fill="both", expand=True)

    def display_student_table(self, students):
        self.clear_frame(self.student_frame)
        headers = ["Nama", "Nilai"]
        header_frame = ctk.CTkFrame(self.student_frame, fg_color=highlight_color)
        header_frame.pack(fill="x")
        for header in headers:
            header_label = ctk.CTkLabel(header_frame, text=header, anchor="w", text_color=fg_color)
            header_label.pack(side="left", padx=5, pady=5, expand=True)

        grade_options = ["A", "A-", "A/B", "B+", "B", "B-", "B/C", "C+", "C", "C-", "C/D", "D+", "D", "E"]
        for student in students:
            row_frame = ctk.CTkFrame(self.student_frame, fg_color="#FFFFFF")
            row_frame.pack(fill="x")
            student_label = ctk.CTkLabel(row_frame, text=student[0], anchor="w", text_color="black")
            student_label.pack(side="left", padx=5, pady=5, expand=True)
            grade_dropdown = ctk.CTkComboBox(row_frame, values=grade_options, font=("Arial", 14))
            grade_dropdown.pack(side="left", padx=5, pady=5, expand=True)

        save_button = ctk.CTkButton(self.student_frame, text="Simpan", command=self.controller.save_penilaian, fg_color=highlight_color, hover_color="#c41212", font=("Arial", 14))
        save_button.pack(pady=10)

#edit2
class ScheduleView:
    def __init__(self, root, controller=None):
        self.root = root
        self.controller = controller
        self.bg_color = "white"
        self.highlight_color = "#4CAF50"
        self.fg_color = "white"
        self.create_widgets()

    def create_widgets(self):
        self.content_frame = ctk.CTkFrame(self.root)
        self.content_frame.pack(fill="both", expand=True)
        
        self.jadwal_title = ctk.CTkLabel(self.content_frame, text="Jadwal Kuliah", font=("Arial", 20, "bold"), text_color=self.bg_color)
        self.jadwal_title.pack(pady=10)

        self.jadwal_info = ctk.CTkLabel(self.content_frame, text="Pilih Mata Kuliah:", font=("Arial", 16), text_color=self.bg_color)
        self.jadwal_info.pack(pady=10)

        self.lesson_dropdown = ctk.CTkComboBox(self.content_frame, font=("Arial", 14), text_color="black", fg_color="white")
        self.lesson_dropdown.pack(pady=10)

        self.show_schedule_today_button = ctk.CTkButton(self.content_frame, text="Tampilkan Jadwal Hari Ini", fg_color=self.highlight_color, text_color=self.fg_color, font=("Arial", 14), command=self.controller.show_schedule_today if self.controller else None)
        self.show_schedule_today_button.pack(pady=10)

        self.show_schedule_weekly_button = ctk.CTkButton(self.content_frame, text="Tampilkan Jadwal Mingguan", fg_color=self.highlight_color, text_color=self.fg_color, font=("Arial", 14), command=self.controller.show_schedule_weekly if self.controller else None)
        self.show_schedule_weekly_button.pack(pady=10)

        self.schedule_frame = ctk.CTkFrame(self.content_frame, fg_color="#FFFFFF")
        self.schedule_frame.pack(fill="both", expand=True)

    def update_lessons(self, lessons):
        self.lesson_dropdown.configure(values=lessons)
        if lessons:
            self.lesson_dropdown.set(lessons[0])

    def clear_schedule(self):
        for widget in self.schedule_frame.winfo_children():
            widget.destroy()

    def display_date_header(self, date_str):
        date_frame = ctk.CTkFrame(self.schedule_frame, fg_color=self.highlight_color)
        date_frame.pack(fill="x", padx=10, pady=5)
        date_label = ctk.CTkLabel(date_frame, text=date_str, font=("Arial", 14, "bold"), text_color=self.fg_color)
        date_label.pack(pady=5)
        return date_frame

    def display_no_classes(self, date_frame):
        no_class_label = ctk.CTkLabel(date_frame, text="No classes scheduled", text_color=self.fg_color)
        no_class_label.pack()

    def display_schedule_headers(self):
        headers = ["Kode", "Mata Kuliah", "SKS", "Jadwal Kuliah", "Ruang", "Dosen"]
        header_frame = ctk.CTkFrame(self.schedule_frame, fg_color=self.highlight_color)
        header_frame.pack(fill="x")
        for header in headers:
            header_label = ctk.CTkLabel(header_frame, text=header, anchor="w", text_color=self.fg_color, padx=5, pady=5)
            header_label.pack(side="left", expand=True, fill="x")

    def display_schedule_row(self, course):
        row_frame = ctk.CTkFrame(self.schedule_frame, fg_color="#FFFFFF")
        row_frame.pack(fill="x", padx=5, pady=2)
        for value in course:
            cell_label = ctk.CTkLabel(row_frame, text=value, anchor="w", text_color="black", padx=5, pady=5)
            cell_label.pack(side="left", expand=True, fill="x")

# control
class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.main_view = View(self)
        self.main_view.show()
        self.root = Tk()
        self.login_view = LoginView(self.root, self)

    def start(self):
        self.view.root.mainloop()
        
    def run(self):
        self.root.mainloop()

    def open_registration_window(self, title):
        fields = []
        submit_callback = None
        if "Dosen" in title:
            fields = ["Nama Lengkap", "Jenis Kelamin", "NIDN", "Program Studi", "Username", "Password"]
            submit_callback = self.submit_dosen_registration
        elif "Mahasiswa" in title:
            fields = ["Nama Lengkap", "Jenis Kelamin", "Angkatan", "Program Studi", "Username", "Password", "NIM"]
            submit_callback = self.submit_mahasiswa_registration
        self.reg_view = RegistrationView(self, title, fields, submit_callback)

    def back_to_main(self):
        self.reg_view.close()
        self.main_view.show()

    def submit_dosen_registration(self):
        data = self.reg_view.get_entry_data()
        self.insert_dosen(data["Nama Lengkap"], data["Jenis Kelamin"], data["NIDN"], data["Program Studi"], data["Username"], data["Password"])
        self.reg_view.show_message("Pendaftaran Dosen Berhasil!", self.back_to_main)

    def submit_mahasiswa_registration(self):
        data = self.reg_view.get_entry_data()
        self.insert_mahasiswa(data["Nama Lengkap"], data["Jenis Kelamin"], data["Angkatan"], data["Program Studi"], data["Username"], data["Password"], data["NIM"])
        self.reg_view.show_message("Pendaftaran Mahasiswa Berhasil!", self.back_to_main)

    def open_login_window(self):
        self.root.destroy()
        self.root = Tk()
        self.login_view = LoginView(self.root, self)
        self.run()

    def verify_login(self, username, password):
        dosen_result, mahasiswa_result = self.verify_login(username, password)
        if dosen_result:
            messagebox.showinfo("Login Berhasil", "Selamat datang, Dosen!")
            self.root.destroy()
            self.show_dosen_dashboard(username)
        elif mahasiswa_result:
            messagebox.showinfo("Login Berhasil", "Selamat datang, Mahasiswa!")
            self.root.destroy()
            self.show_dashboard(username)
        else:
            messagebox.showerror("Login Gagal", "Username atau password salah.")

    def show_dashboard(self, username):
        self.root = Tk()
        self.dashboard_view = DashboardView(self.root, self, username)
        self.run()

    def show_dosen_dashboard(self, username):
        # Implementasi dashboard dosen
        pass

    def get_student_data(self, username):
        return self.get_student_data(username)

    def get_dosen_data(self, username):
        return self.get_dosen_data(username)

    def logout(self):
        self.root.destroy()
        self.root = Tk()
        self.login_view = LoginView(self.root, self)
        self.run()

    def show_dashboard_content(self, content_frame, username):
        for widget in content_frame.winfo_children():
            widget.destroy()
        dashboard_label = ctk.CTkLabel(content_frame, text="Dashboard", font=ctk.CTkFont(size=30, weight="bold"))
        dashboard_label.pack(pady=20)

    def show_pengisian_krs(self, content_frame, username):
        for widget in content_frame.winfo_children():
            widget.destroy()
        krs_label = ctk.CTkLabel(content_frame, text="Pengisian KRS", font=ctk.CTkFont(size=30, weight="bold"))
        krs_label.pack(pady=20)
        # Implementasi konten pengisian KRS

    def show_kartu_rencana_studi(self, content_frame, username):
        for widget in content_frame.winfo_children():
            widget.destroy()
        krs_label = ctk.CTkLabel(content_frame, text="Kartu Rencana Studi", font=ctk.CTkFont(size=30, weight="bold"))
        krs_label.pack(pady=20)
        # Implementasi konten Kartu Rencana Studi

    def show_jadwal_kuliah(self, content_frame, username):
        for widget in content_frame.winfo_children():
            widget.destroy()
        jadwal_label = ctk.CTkLabel(content_frame, text="Jadwal Kuliah", font=ctk.CTkFont(size=30, weight="bold"))
        jadwal_label.pack(pady=20)
        # Implementasi konten Jadwal Kuliah

    def show_hasil_studi(self, content_frame, username):
        for widget in content_frame.winfo_children():
            widget.destroy()
        hasil_label = ctk.CTkLabel(content_frame, text="Hasil Studi", font=ctk.CTkFont(size=30, weight="bold"))
        hasil_label.pack(pady=20)
        # Implementasi konten Hasil Studi

    def show_kehadiran_mahasiswa(self, content_frame, username):
        for widget in content_frame.winfo_children():
            widget.destroy()
        kehadiran_label = ctk.CTkLabel(content_frame, text="Kehadiran Mahasiswa", font=ctk.CTkFont(size=30, weight="bold"))
        kehadiran_label.pack(pady=20)
        # Implementasi konten Kehadiran Mahasiswa
    
#edit
    def fetch_classes(self):
        return self.model.fetch_classes()

    def show_students(self):
        students = self.model.fetch_students()
        self.view.display_students(students)

    def save_attendance(self, student_entries, kode_matkul):
        attendance_records = []
        for entry in student_entries:
            student_nim = entry[0].cget("text")
            student_name = entry[1].cget("text")
            selected_date = entry[2].get_date().strftime('%Y-%m-%d')
            presence = entry[3].get()
            attendance_records.append((student_nim, student_name, selected_date, presence, kode_matkul))
        self.model.save_attendance(attendance_records)
        print(f"Attendance records saved: {attendance_records}")

    def fetch_class_names(self):
        class_options = self.model.fetch_classes()
        return [option[0] for option in class_options]

    def show_student_table(self):
        students = self.model.fetch_student_names()
        self.view.display_student_table(students)

    def save_penilaian(self):
        penilaian_data = []
        course_code = self.view.lesson_dropdown.get()
        for row_frame in self.view.student_frame.winfo_children():
            student_label = None
            grade_dropdown = None
            for child in row_frame.winfo_children():
                if isinstance(child, ctk.CTkLabel):
                    student_label = child
                elif isinstance(child, ctk.CTkComboBox):
                    grade_dropdown = child
            if student_label and grade_dropdown:
                student_name = student_label.cget('text')
                grade = grade_dropdown.get()
                grade_to_score = {
                    "A": 4.00, "A-": 3.75, "A/B": 3.50, "B+": 3.25, "B": 3.00, "B-": 2.75,
                    "B/C": 2.50, "C+": 2.25, "C": 2.00, "C-": 1.75, "C/D": 1.50, "D+": 1.25,
                    "D": 1.00, "E": 0.00
                }
                score = grade_to_score.get(grade, 0.00)
                penilaian_data.append((student_name, grade, score))
        self.model.update_grades(penilaian_data, course_code)

    def submit_krs(self, username, matkul_list):
        program_studi = self.model.get_program_studi(username)
        self.model.simpan_krs_mahasiswa(username, matkul_list)
        self.view.show_kartu_rencana_studi(self.model.get_krs_mahasiswa())

    def update_approval_status(self, krs_id, status):
        self.model.update_approval_status(krs_id, status)
        self.view.show_krs_dosen(self.model.get_krs_mahasiswa())

#main
# if __name__ == "__main__":
#     model = Model()
#     view = View(Controller(model, None))
#     controller = Controller(model, view)
#     view.controller = controller
#     controller.start()

class KRSController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def display_krs(self, frame):
        data = self.model.get_krs_data()
        self.view.display_krs(frame, data)

class JadwalController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def display_lesson_options(self, frame):
        lessons = self.model.get_lesson_options()
        return self.view.display_jadwal(frame, lessons)

    def display_schedule_today(self, frame):
        day = datetime.datetime.now().strftime('%A')
        courses = self.model.get_schedule_today(day)
        headers = ["Kode", "Mata Kuliah", "SKS", "Jadwal", "Ruang Kuliah", "Nama Dosen"]
        self.view.display_schedule(frame, f"Jadwal Hari Ini: {day}", courses, headers)

    def display_weekly_schedule(self, frame):
        courses = self.model.get_weekly_schedule()
        headers = ["Kode", "Mata Kuliah", "SKS", "Jadwal", "Ruang Kuliah", "Nama Dosen"]
        self.view.display_schedule(frame, "Jadwal Mingguan", courses, headers)

class HasilStudiController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def display_hasil_studi(self, frame):
        data = self.model.get_hasil_studi_data()
        # Contoh nilai tetap untuk tambahan data hasil studi
        ip_semester = "3.5"
        ip_kumulatif = "3.4"
        status = "Aktif"
        self.view.display_hasil_studi(frame, data, ip_semester, ip_kumulatif, status)

class KehadiranController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def display_kehadiran(self, frame):
        data = self.model.get_kehadiran_data()
        self.view.display_kehadiran(frame, data)
    
    def display_kehadiran_summary(self, frame):
        summary = self.model.get_kehadiran_summary()
        self.view.display_kehadiran_summary(frame, summary)

class ScheduleController:
    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.initialize()

    def initialize(self):
        lessons = self.model.get_distinct_lessons()
        self.view.update_lessons(lessons)

    def show_schedule_today(self):
        self.view.clear_schedule()
        today_day = datetime.datetime.today().strftime('%A')
        days_translation = {
            'Monday': 'Senin',
            'Tuesday': 'Selasa',
            'Wednesday': 'Rabu',
            'Thursday': 'Kamis',
            'Friday': 'Jumat',
            'Saturday': 'Sabtu',
            'Sunday': 'Minggu'
        }
        today_day = days_translation[today_day]
        courses_data = self.model.get_courses_for_day(today_day)
        today_date = datetime.date.today().strftime("%d/%m/%Y")
        date_frame = self.view.display_date_header(f"Jadwal Hari Ini ({today_date})")
        if not courses_data:
            self.view.display_no_classes(date_frame)
        else:
            self.view.display_schedule_headers()
            for course in courses_data:
                self.view.display_schedule_row(course)

    def show_schedule_weekly(self):
        self.view.clear_schedule()
        today = datetime.date.today()
        start_week = today - datetime.timedelta(days=today.weekday())
        dates = [(start_week + datetime.timedelta(days=i)).strftime("%d/%m/%Y") for i in range(7)]
        days_translation = {
            'Monday': 'Senin',
            'Tuesday': 'Selasa',
            'Wednesday': 'Rabu',
            'Thursday': 'Kamis',
            'Friday': 'Jumat',
            'Saturday': 'Sabtu',
            'Sunday': 'Minggu'
        }
        week_days = list(days_translation.values())
        courses_data = self.model.get_all_courses()
        schedule_data = {day: [] for day in week_days}
        for course in courses_data:
            day_of_week = course[3].split(',')[0]
            if day_of_week in schedule_data:
                schedule_data[day_of_week].append(course)
        for date, day in zip(dates, week_days):
            date_frame = self.view.display_date_header(f"{day} ({date})")
            if not schedule_data[day]:
                self.view.display_no_classes(date_frame)
            else:
                self.view.display_schedule_headers()
                for course in schedule_data[day]:
                    self.view.display_schedule_row(course)
                    
#main
import customtkinter as ctk
# from models import KRSModel, JadwalModel, HasilStudiModel, KehadiranModel
# from views import KRSView, JadwalView, HasilStudiView, KehadiranView
# from controllers import KRSController, JadwalController, HasilStudiController, KehadiranController

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sistem Informasi Mahasiswa")
        self.geometry("800x600")

        self.krs_model = KRSModel()
        self.krs_view = KRSView()
        self.krs_controller = KRSController(self.krs_model, self.krs_view)

        self.jadwal_model = JadwalModel()
        self.jadwal_view = JadwalView()
        self.jadwal_controller = JadwalController(self.jadwal_model, self.jadwal_view)

        self.hasil_studi_model = HasilStudiModel()
        self.hasil_studi_view = HasilStudiView()
        self.hasil_studi_controller = HasilStudiController(self.hasil_studi_model, self.hasil_studi_view)

        self.kehadiran_model = KehadiranModel()
        self.kehadiran_view = KehadiranView()
        self.kehadiran_controller = KehadiranController(self.kehadiran_model, self.kehadiran_view)

        self.container = ctk.CTkFrame(self)  # Initialize container frame
        self.container.pack(fill="both", expand=True)

        self.frames = {}
        self.create_frames()

        self.show_frame("KRSFrame")  # Show initial frame

    def create_frames(self):
        # Import your frame classes here

        for F in (KRSFrame, JadwalFrame, HasilStudiFrame, KehadiranFrame):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


class KRSFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.controller.krs_controller.display_krs(self)

class JadwalFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.controller.jadwal_controller.display_lesson_options(self)

class HasilStudiFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.controller.hasil_studi_controller.display_hasil_studi(self)

class KehadiranFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.controller.kehadiran_controller.display_kehadiran(self)
        self.controller.kehadiran_controller.display_kehadiran_summary(self)

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
