import customtkinter as ctk
from PIL import Image, ImageTk
import sqlite3
from tkinter import messagebox
import tkinter as tk
from tkcalendar import DateEntry
import datetime
from tkinter import ttk

# Define colors to match the image
bg_color = "#3E0A0A"  # Dark maroon
fg_color = "#FFFFFF"  # White
highlight_color = "#8C1C1C"  # Lighter maroon

# Initialize database
def initialize_db():
    conn = sqlite3.connect('university.db')
    c = conn.cursor()
    # Create tables
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
        grade TEXT NOT NULL,
        score REAL NOT NULL,
        FOREIGN KEY (nama_lengkap) REFERENCES mahasiswa(username)
    )
    ''')
    c.execute("""
        CREATE TABLE IF NOT EXISTS nilai (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_lengkap TEXT NOT NULL,
            nama_matkul TEXT NOT NULL,
            grade TEXT NOT NULL,
            score REAL NOT NULL,
            FOREIGN KEY (nama_lengkap) REFERENCES mahasiswa(username),
            FOREIGN KEY (nama_matkul) REFERENCES matkul(nama_matkul)
        );
    """)
    conn.commit()
    conn.close()

#data kosong
data = [

    ]

# Function to create the main window
def main_window():
    def open_registration_window(title):
        app.destroy()
        if title == "Registrasi Dosen":
            registrasi_dosen()
        elif title == "Registrasi Mahasiswa":
            registrasi_mahasiswa()

    def open_login_window():
        app.destroy()
        login_window()

    global app
    app = ctk.CTk()
    app.title("INSTITUT GADJAH INDONESIA")
    app.geometry("{0}x{1}+0+0".format(app.winfo_screenwidth(), app.winfo_screenheight()))
    app.configure(bg="white")

    fullscreen_frame = ctk.CTkFrame(app, fg_color="white", bg_color="white")
    fullscreen_frame.pack(fill="both", expand=True)

    center_frame = ctk.CTkFrame(fullscreen_frame, fg_color="white", bg_color="white")
    center_frame.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

    title_label = ctk.CTkLabel(center_frame, text="INSTITUT GADJAH INDONESIA", font=ctk.CTkFont(family="Helvetica", size=48, weight="bold"), text_color="black", bg_color="white")
    title_label.pack(pady=20)

    global logo_image_path
    logo_image_path = "logo.png"  # Path to the uploaded image
    logo_image = Image.open(logo_image_path)
    logo_image = logo_image.resize((300, 300), Image.LANCZOS)
    logo_photo = ImageTk.PhotoImage(logo_image)
    logo_label = ctk.CTkLabel(center_frame, image=logo_photo, text="", bg_color="white")
    logo_label.pack(pady=20)

    global button_font
    button_font = ctk.CTkFont(size=20)
    register_dosen_button = ctk.CTkButton(center_frame, text="Registrasi Dosen", fg_color="white", hover_color="light grey", border_width=2, border_color="#800000", text_color="#800000", font=button_font, width=300, height=60, bg_color="white", command=lambda: open_registration_window("Registrasi Dosen"))
    register_dosen_button.pack(pady=10)

    register_mahasiswa_button = ctk.CTkButton(center_frame, text="Registrasi Mahasiswa", hover_color="light grey", fg_color="white", border_width=2, border_color="#800000", text_color="#800000", font=button_font, width=300, height=60, bg_color="white", command=lambda: open_registration_window("Registrasi Mahasiswa"))
    register_mahasiswa_button.pack(pady=10)

    login_button = ctk.CTkButton(center_frame, text="Login", fg_color="#800000", hover_color="#500000", text_color="white", font=button_font, width=300, height=60, bg_color="white", command=open_login_window)
    login_button.pack(pady=10)

    app.mainloop()

# Function to create the registration window for dosen
def registrasi_dosen():
    def submit_and_return():
        nama_lengkap = nama_lengkap_entry.get()
        program_studi = program_studi_entry.get()
        jenis_kelamin = jk_entry.get()
        password = password_entry.get()
        
        # Mengambil huruf pertama dari setiap kata dalam program studi
        huruf_pertama_jurusan = ''.join([kata[0] for kata in program_studi.split()])
        first_name = nama_lengkap.split()[0]
        huruf_pertama_nama = ''.join([kata[0] for kata in nama_lengkap.split()])

        # Membuat username
        username_generated = f"{first_name}_{huruf_pertama_jurusan}"

        # Membuat NIM
        nidn = f"{huruf_pertama_jurusan}/{huruf_pertama_nama}"
        
        conn = sqlite3.connect('university.db')
        c = conn.cursor()
        c.execute('''
        INSERT INTO dosen (nama_lengkap, jenis_kelamin, nidn, program_studi, username, password)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (nama_lengkap, jenis_kelamin, nidn, program_studi, username_generated, password))
        conn.commit()
        conn.close()
        
        reg_center_frame.pack_forget()

        message_frame = ctk.CTkFrame(reg_fullscreen_frame, fg_color="white", bg_color="white", border_color="black", border_width=2)
        message_frame.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        message_frame.configure(width=450, height=200)
        message_frame.pack_propagate(False)
        
        message_label = ctk.CTkLabel(message_frame, text=f"Registrasi berhasil!\nUsername Anda: {username_generated}", font=ctk.CTkFont(family="Helvetica", size=25, weight="bold"), text_color="black", bg_color="white")
        message_label.pack(pady=20)

        back_button = ctk.CTkButton(message_frame, text="Kembali ke Menu Utama", fg_color="#800000", hover_color="#500000", text_color="white", font=button_font, width=250, height=60, bg_color="white", command=lambda: [reg_window.destroy(), main_window()])
        back_button.pack(pady=20)

    def back_to_main():
        reg_window.destroy()
        main_window()

    reg_window = ctk.CTk()
    reg_window.title("Registrasi Dosen")
    reg_window.geometry("{0}x{1}+0+0".format(reg_window.winfo_screenwidth(), reg_window.winfo_screenheight()))
    reg_window.configure(bg="white")
    
    reg_fullscreen_frame = ctk.CTkFrame(reg_window, fg_color="white", bg_color="white")
    reg_fullscreen_frame.pack(fill="both", expand=True)
    
    global reg_center_frame
    reg_center_frame = ctk.CTkFrame(reg_fullscreen_frame, fg_color="white", bg_color="white")
    reg_center_frame.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
    
    # Adding the back button with arrow icon
    back_button = ctk.CTkButton(reg_fullscreen_frame, text="← Back", fg_color="grey", hover_color="#500000", text_color="white", font=button_font, width=100, height=40, bg_color="white", command=back_to_main)
    back_button.place(x=20, y=20)

    reg_title_label = ctk.CTkLabel(reg_center_frame, text="INSTITUT GADJAH INDONESIA", font=ctk.CTkFont(family="Helvetica", size=48, weight="bold"), text_color="black", bg_color="white")
    reg_title_label.pack(pady=20)
    
    reg_logo_image = Image.open(logo_image_path)
    reg_logo_image = reg_logo_image.resize((300, 300), Image.LANCZOS)
    reg_logo_photo = ImageTk.PhotoImage(reg_logo_image)
    reg_logo_label = ctk.CTkLabel(reg_center_frame, image=reg_logo_photo, text="", bg_color="white")
    reg_logo_label.pack(pady=20)
    
    reg_form_title_label = ctk.CTkLabel(reg_center_frame, text="Registrasi Dosen", font=ctk.CTkFont(family="Helvetica", size=36, weight="bold"), text_color="black", bg_color="white")
    reg_form_title_label.pack(pady=20)
    
    nama_lengkap_entry = ctk.CTkEntry(reg_center_frame, placeholder_text="Nama Lengkap", width=400, height=40, fg_color="#FFFFFF", text_color="black")
    nama_lengkap_entry.pack(pady=10)

    jk_entry = ctk.CTkEntry(reg_center_frame, placeholder_text="Jenis Kelamin", width=400, height=40, fg_color="#FFFFFF", text_color="black")
    jk_entry.pack(pady=10)

    program_studi_entry = ctk.CTkEntry(reg_center_frame, placeholder_text="Program Studi", width=400, height=40, fg_color="#FFFFFF", text_color="black")
    program_studi_entry.pack(pady=10)

    password_entry = ctk.CTkEntry(reg_center_frame, placeholder_text="Password", width=400, height=40, fg_color="#FFFFFF", text_color="black", show='*')
    password_entry.pack(pady=10)
    
    submit_button = ctk.CTkButton(reg_center_frame, text="Sign Up", fg_color="#800000", hover_color="#500000", text_color="white", font=button_font, width=300, height=60, bg_color="white", command=submit_and_return)
    submit_button.pack(pady=20)

    reg_window.mainloop()

# Function to create the registration window for mahasiswa
def registrasi_mahasiswa():
    def submit_and_return():
        nama_lengkap = nama_lengkap_entry.get()
        angkatan = angkatan_entry.get()
        program_studi = program_studi_entry.get()
        password = password_entry.get()
        jenis_kelamin = jk_entry.get()

        # Mengambil dua angka terakhir dari angkatan
        dua_tahun_terakhir = str(angkatan)[-2:]

        # Mengambil huruf pertama dari setiap kata dalam program studi
        huruf_pertama_jurusan = ''.join([kata[0] for kata in program_studi.split()])

        huruf_pertama_nama = ''.join([kata[0] for kata in nama_lengkap.split()])
        
        # Mengambil nama pertama
        first_name = nama_lengkap.split()[0]

        # Membuat username
        username_generated = f"{first_name}_{angkatan}"

        # Membuat NIM
        nim = f"{dua_tahun_terakhir}/{huruf_pertama_jurusan}/{huruf_pertama_nama}"

        
        conn = sqlite3.connect('university.db')
        c = conn.cursor()

        c.execute('''
        INSERT INTO mahasiswa (nama_lengkap, jenis_kelamin, angkatan, program_studi, username, password, nim)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (nama_lengkap, jenis_kelamin, angkatan, program_studi, username_generated, password, nim))
        conn.commit()
        conn.close()
        
        reg_center_frame.pack_forget()

        message_frame = ctk.CTkFrame(reg_fullscreen_frame, fg_color="white", bg_color="white", border_color="black", border_width=2)
        message_frame.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        message_frame.configure(width=450, height=200)
        message_frame.pack_propagate(False)
        
        message_label = ctk.CTkLabel(message_frame, text=f"Registrasi berhasil!\nUsername Anda: {username_generated}", font=ctk.CTkFont(family="Helvetica", size=25, weight="bold"), text_color="black", bg_color="white")
        message_label.pack(pady=20)

        back_button = ctk.CTkButton(message_frame, text="Kembali ke Menu Utama", fg_color="#800000", hover_color="#500000", text_color="white", font=button_font, width=250, height=60, bg_color="white", command=lambda: [reg_window.destroy(), main_window()])
        back_button.pack(pady=20)

    def back_to_main():
        reg_window.destroy()
        main_window()

    reg_window = ctk.CTk()
    reg_window.title("Registrasi Mahasiswa")
    reg_window.geometry("{0}x{1}+0+0".format(reg_window.winfo_screenwidth(), reg_window.winfo_screenheight()))
    reg_window.configure(bg="white")
    
    reg_fullscreen_frame = ctk.CTkFrame(reg_window, fg_color="white", bg_color="white")
    reg_fullscreen_frame.pack(fill="both", expand=True)
    
    global reg_center_frame
    reg_center_frame = ctk.CTkFrame(reg_fullscreen_frame, fg_color="white", bg_color="white")
    reg_center_frame.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
    
    # Adding the back button with arrow icon
    back_button = ctk.CTkButton(reg_fullscreen_frame, text="← Back", fg_color="grey", hover_color="#500000", text_color="white", font=button_font, width=100, height=40, bg_color="white", command=back_to_main)
    back_button.place(x=20, y=20)

    reg_title_label = ctk.CTkLabel(reg_center_frame, text="INSTITUT GADJAH INDONESIA", font=ctk.CTkFont(family="Helvetica", size=48, weight="bold"), text_color="black", bg_color="white")
    reg_title_label.pack(pady=20)
    
    reg_logo_image = Image.open(logo_image_path)
    reg_logo_image = reg_logo_image.resize((300, 300), Image.LANCZOS)
    reg_logo_photo = ImageTk.PhotoImage(reg_logo_image)
    reg_logo_label = ctk.CTkLabel(reg_center_frame, image=reg_logo_photo, text="", bg_color="white")
    reg_logo_label.pack(pady=20)
    
    reg_form_title_label = ctk.CTkLabel(reg_center_frame, text="Registrasi Mahasiswa", font=ctk.CTkFont(family="Helvetica", size=36, weight="bold"), text_color="black", bg_color="white")
    reg_form_title_label.pack(pady=20)
    
    nama_lengkap_entry = ctk.CTkEntry(reg_center_frame, placeholder_text="Nama Lengkap", width=400, height=40, fg_color="#FFFFFF", text_color="black")
    nama_lengkap_entry.pack(pady=10)

    jk_entry = ctk.CTkEntry(reg_center_frame, placeholder_text="Jenis Kelamin", width=400, height=40, fg_color="#FFFFFF", text_color="black")
    jk_entry.pack(pady=10)

    angkatan_entry = ctk.CTkEntry(reg_center_frame, placeholder_text="Angkatan", width=400, height=40, fg_color="#FFFFFF", text_color="black")
    angkatan_entry.pack(pady=10)

    program_studi_entry = ctk.CTkEntry(reg_center_frame, placeholder_text="Program Studi", width=400, height=40, fg_color="#FFFFFF", text_color="black")
    program_studi_entry.pack(pady=10)

    password_entry = ctk.CTkEntry(reg_center_frame, placeholder_text="Password", width=400, height=40, fg_color="#FFFFFF", text_color="black", show='*')
    password_entry.pack(pady=10)
    
    submit_button = ctk.CTkButton(reg_center_frame, text="Sign Up", fg_color="#800000", hover_color="#500000", text_color="white", font=button_font, width=300, height=60, bg_color="white", command=submit_and_return)
    submit_button.pack(pady=20)

    reg_window.mainloop()

# Function to create the login window
def login_window():
    def verify_login():
        username = username_entry.get()
        password = password_entry.get()
        
        conn = sqlite3.connect('university.db')
        c = conn.cursor()
        
        # Verify login for dosen
        c.execute('''
        SELECT * FROM dosen WHERE username = ? AND password = ?
        ''', (username, password))
        dosen_result = c.fetchone()
        
        # Verify login for mahasiswa
        c.execute('''
        SELECT * FROM mahasiswa WHERE username = ? AND password = ?
        ''', (username, password))
        mahasiswa_result = c.fetchone()
        
        conn.close()
        
        if dosen_result:
            messagebox.showinfo("Login Berhasil", "Selamat datang, Dosen!")
            login_window.destroy()  # Close login window
            show_dosen_dashboard(username)
        elif mahasiswa_result:
            messagebox.showinfo("Login Berhasil", "Selamat datang, Mahasiswa!")
            login_window.destroy()  # Close login window
            show_dashboard(username)
        else:
            messagebox.showerror("Login Gagal", "Username atau password salah.")

    def back_to_main():
        login_window.destroy()
        main_window()

    login_window = ctk.CTk()
    login_window.title("Login")
    login_window.geometry("{0}x{1}+0+0".format(login_window.winfo_screenwidth(), login_window.winfo_screenheight()))
    login_window.configure(bg="white")

    login_fullscreen_frame = ctk.CTkFrame(login_window, fg_color="white", bg_color="white")
    login_fullscreen_frame.pack(fill="both", expand=True)
    
    global login_center_frame
    login_center_frame = ctk.CTkFrame(login_fullscreen_frame, fg_color="white", bg_color="white")
    login_center_frame.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
    
    # Adding the back button with arrow icon
    back_button = ctk.CTkButton(login_fullscreen_frame, text="← Back", fg_color="grey", hover_color="#500000", text_color="white", font=button_font, width=100, height=40, bg_color="white", command=back_to_main)
    back_button.place(x=20, y=20)

    login_title_label = ctk.CTkLabel(login_center_frame, text="INSTITUT GADJAH INDONESIA", font=ctk.CTkFont(family="Helvetica", size=48, weight="bold"), text_color="black", bg_color="white")
    login_title_label.pack(pady=20)
    
    login_logo_image = Image.open(logo_image_path)
    login_logo_image = login_logo_image.resize((300, 300), Image.LANCZOS)
    login_logo_photo = ImageTk.PhotoImage(login_logo_image)
    login_logo_label = ctk.CTkLabel(login_center_frame, image=login_logo_photo, text="", bg_color="white")
    login_logo_label.pack(pady=20)
    
    login_form_title_label = ctk.CTkLabel(login_center_frame, text="Login", font=ctk.CTkFont(family="Helvetica", size=36, weight="bold"), text_color="black", bg_color="white")
    login_form_title_label.pack(pady=20)
    
    username_entry = ctk.CTkEntry(login_center_frame, placeholder_text="Username", width=400, height=40, fg_color="#FFFFFF", text_color="black")
    username_entry.pack(pady=10)
    
    password_entry = ctk.CTkEntry(login_center_frame, placeholder_text="Password", width=400, height=40, fg_color="#FFFFFF", text_color="black", show='*')
    password_entry.pack(pady=10)
    
    login_button = ctk.CTkButton(login_center_frame, text="Login", fg_color="#800000", hover_color="#500000", text_color="white", font=button_font, width=300, height=60, bg_color="white", command=verify_login)
    login_button.pack(pady=20)

    login_window.mainloop()

def get_student_data(username):
    # Koneksi ke database
    conn = sqlite3.connect('university.db')
    cursor = conn.cursor()

    # Query untuk mengambil data mahasiswa berdasarkan username
    cursor.execute("SELECT * FROM mahasiswa WHERE username=?", (username,))
    student_data = cursor.fetchone()  # Mengambil satu baris hasil

    conn.close()  # Tutup koneksi setelah selesai

    return student_data

def get_dosen_data(username):
    # Koneksi ke database
    conn = sqlite3.connect('university.db')
    cursor = conn.cursor()

    # Query untuk mengambil data mahasiswa berdasarkan username
    cursor.execute("SELECT * FROM dosen WHERE username=?", (username,))
    dosen_data = cursor.fetchone()  # Mengambil satu baris hasil

    conn.close()  # Tutup koneksi setelah selesai

    return dosen_data

# Function to show the dashboard after successful login
def show_dashboard(username):
    global content_frame
    global nav_frame
    # Create the main window
    app = ctk.CTk()
    app.geometry("{0}x{1}+0+0".format(app.winfo_screenwidth(), app.winfo_screenheight()))
    app.title("Sistem Akademik Universitas")

    # Define colors to match the image
    bg_color = "#3E0A0A"  # Dark maroon
    fg_color = "#FFFFFF"  # White
    highlight_color = "#8C1C1C"  # Lighter maroon

    # Configure the main app colors
    app.configure(bg="#FFFFFF")

    #data kosong
    data = []

    # Left navigation frame
    global nav_frame
    nav_frame = ctk.CTkFrame(app, width=250, corner_radius=0, fg_color=bg_color)
    nav_frame.pack(side="left", fill="y")

    logo_image_path = "logo.png"  # Path to the uploaded image
    logo_image = Image.open(logo_image_path)
    logo_image = logo_image.resize((220, 220), Image.LANCZOS)  # Resize image to be larger
    logo_photo = ImageTk.PhotoImage(logo_image)
    logo_label = tk.Label(nav_frame, image=logo_photo, anchor="center", bg=bg_color)
    logo_label.pack(pady=10)

    # University name
    university_name_label = ctk.CTkLabel(nav_frame, text="INSTITUT GADJAH INDONESIA", anchor="center", font=("Arial", 14, "bold"), text_color=fg_color)
    university_name_label.pack(pady=10)

    # Left navigation user label
    student_data = get_student_data(username)
    user_label = ctk.CTkLabel(nav_frame, text=f"{student_data[1]} (Mahasiswa)", anchor="w", text_color=fg_color, font=("Arial", 14))
    user_label.pack(pady=20, padx=20)


    buttons = [
            ("Dashboard", show_dashboard_content),
            ("Pengisian KRS", lambda: show_pengisian_krs(content_frame, username)),
            ("Kartu Rencana Studi", show_kartu_rencana_studi),
            ("Jadwal Kuliah", show_jadwal_kuliah),
            ("Hasil Studi", show_hasil_studi),
            ("Kehadiran Mahasiswa", show_kehadiran_mahasiswa)
        ]

    highlight_color = "#8C1C1C"  # Gantilah dengan warna yang Anda inginkan

    for button_text, command in buttons:
        btn = ctk.CTkButton(nav_frame, text=button_text, anchor="w", fg_color=highlight_color, hover_color="#c41212", font=("Arial", 20), command=command)
        btn.pack(fill="x", pady=5, padx=10)

    # Add logout button at the bottom left
    logout_button = ctk.CTkButton(nav_frame, text="Log Out", fg_color=highlight_color, hover_color="#c41212", font=("Arial", 14), command=lambda: [app.destroy(), main_window()])
    logout_button.pack(side="bottom", fill="x", pady=10, padx=10)

    # Right content frame
    content_frame = ctk.CTkFrame(app, corner_radius=0, fg_color="#FFFFFF")
    content_frame.pack(side="right", fill="both", expand=True)

    # Show the initial dashboard content
    show_dashboard_content(username)

    app.mainloop()
    
def show_dashboard_content(username):
    # Clear existing content in the content_frame
    for widget in content_frame.winfo_children():
        widget.destroy()

    # Fetch student data
    student_data = get_student_data(username)

    if student_data:
        # Dashboard content
        dashboard_label = ctk.CTkLabel(content_frame, text="Dashboard Mahasiswa", font=("Arial", 20, "bold"), text_color=bg_color)
        dashboard_label.pack(pady=10)

        # Student info
        info_frame = ctk.CTkFrame(content_frame, fg_color="#FFFFFF")
        info_frame.pack(pady=10, padx=10, fill="x")

        student_info = [
            ("Nama", student_data[1]),
            ("Jenis Kelamin", student_data[7]),
            ("Angkatan", student_data[2]),
            ("Program Studi", student_data[3]),
            ("Username", student_data[4]),
            ("NIM", student_data[6]),
            ("Dosen Pembimbing", "Dr. Naufal Gumiwang")
        ]

        for key, value in student_info:
            info_row = ctk.CTkFrame(info_frame, fg_color="#FFFFFF")
            info_row.pack(fill="x", pady=2)
            key_label = ctk.CTkLabel(info_row, text=f"{key} :", width=15, anchor="w", text_color="black")
            key_label.pack(side="left", padx=5)
            value_label = ctk.CTkLabel(info_row, text=value, anchor="w", text_color="black")
            value_label.pack(side="left", padx=5)
    else:
        # Handle case where student_data is None or empty
        error_label = ctk.CTkLabel(content_frame, text="Data Mahasiswa Tidak Ditemukan", font=("Arial", 16, "bold"), text_color="red")
        error_label.pack(pady=20)

    # Add new content for Pengisian KRS
    krs_title = ctk.CTkLabel(content_frame, text="Timeline semester", font=("Arial", 20, "bold"), text_color=bg_color)
    krs_title.pack(pady=10)

    table_frame = ctk.CTkFrame(content_frame, corner_radius=10, fg_color="#FFFFFF")
    table_frame.pack(pady=10, padx=10, fill="x")

    # Table header
    columns = ["Kode", "Tanggal Mulai", "Tanggal Selesai"]
    header_bg_color = "#5C0A0A"
    header_text_color = "#FFFFFF"
    for col in columns:
        col_label = ctk.CTkLabel(table_frame, text=col, anchor="w", fg_color=header_bg_color, text_color=header_text_color, width=10)
        col_label.grid(row=0, column=columns.index(col), padx=1, pady=5, sticky="nsew")

    # Sample data for the table (You can add more rows as needed)
    data = [
        ["Batas Akhir Entry Nilai","01 APR 2024", "30 JUN 2024"],
        ["Minggu Tenang", "03 JUN 2024", "08 JUN 2024"],
        ["Kegiatan Belajar Mengajar/Kuliah", "05 FEB 2024","31 MAY 2024"],
        ["Ujian Akhir Semester (UAS)", "10 JUN 2024", "21 JUN 2024"],
        ["Pengisian Perubahan KRS (KPRS)", "12 FEB 2024", "23 FEB 2024"],
        ["Ujian Tengah Semester (UTS)", "25 MAR 2024", "05 APR 2024"],
        ["Pengisian Kartu Rencana Studi (KRS)", "29 JAN 2024", "31 JAN 2024"],
    ]

    # Create table cells and fill with data
    for i, row_data in enumerate(data, start=1):
        for j, val in enumerate(row_data):
            cell = ctk.CTkLabel(table_frame, text=val, anchor="w", fg_color="#FFFFFF", text_color="#000000")
            cell.grid(row=i, column=j, padx=1, pady=5, sticky="nsew")

    # Configure column weights for responsive design
    for i in range(len(columns)):
        table_frame.columnconfigure(i, weight=1)

# Function to show the dashboard after successful login for dosen
def show_dosen_dashboard(username):
    global content_frame
    # Create the main window
    app = ctk.CTk()
    app.geometry("{0}x{1}+0+0".format(app.winfo_screenwidth(), app.winfo_screenheight()))
    app.title("Sistem Akademik Universitas")

    # Define colors to match the image
    bg_color = "#3E0A0A"  # Dark maroon
    fg_color = "#FFFFFF"  # White
    highlight_color = "#8C1C1C"  # Lighter maroon

    # Configure the main app colors
    app.configure(bg="#FFFFFF")

    # Left navigation frame
    nav_frame = ctk.CTkFrame(app, width=250, corner_radius=0, fg_color=bg_color)
    nav_frame.pack(side="left", fill="y")

    logo_image_path = "logo.png"  # Path to the uploaded image
    logo_image = Image.open(logo_image_path)
    logo_image = logo_image.resize((220, 220), Image.LANCZOS)  # Resize image to be larger
    logo_photo = ImageTk.PhotoImage(logo_image)
    logo_label = tk.Label(nav_frame, image=logo_photo, anchor="center", bg=bg_color)
    logo_label.pack(pady=10)

    # University name
    university_name_label = ctk.CTkLabel(nav_frame, text="INSTITUT GADJAH INDONESIA", anchor="center", font=("Arial", 14, "bold"), text_color=fg_color)
    university_name_label.pack(pady=10)

    # Left navigation user label
    dosen_data = get_dosen_data(username)
    user_label = ctk.CTkLabel(nav_frame, text=f"{dosen_data[1]} (Dosen)", anchor="w", text_color=fg_color, font=("Arial", 14))
    user_label.pack(pady=20, padx=20)

    # Update the buttons list
    buttons = [
        ("Dashboard", show_dashboard),
        ("Jadwal Kuliah", show_jadwal_kuliah),
        ("Kehadiran Mahasiswa", show_kehadiran_mahasiswa_dosen),
        ("Penilaian", show_penilaian),
        ("KRS", show_krs_dosen)
    ]

    # Create buttons
    for button_text, command in buttons:
        btn = ctk.CTkButton(nav_frame, text=button_text, anchor="w", fg_color=highlight_color, hover_color="#c41212", font=("Arial", 20), command=command)
        btn.pack(fill="x", pady=5, padx=10)

    # Add logout button at the bottom left
    logout_button = ctk.CTkButton(nav_frame, text="Log Out", fg_color=highlight_color, hover_color="#c41212", font=("Arial", 14), command=lambda: [app.destroy(), main_window()])
    logout_button.pack(side="bottom", fill="x", pady=10, padx=10)

    # Right content frame
    content_frame = ctk.CTkFrame(app, corner_radius=0, fg_color="#FFFFFF")
    content_frame.pack(side="right", fill="both", expand=True)

    # Initial content to display
    show_dosen_dashboard_content(username)

    # Show the initial dashboard content
    app.mainloop()

def show_dosen_dashboard_content(username):
    # Clear existing content in the content_frame
    for widget in content_frame.winfo_children():
        widget.destroy()

    # Fetch dosen data
    dosen_data = get_dosen_data(username)

    if dosen_data:
        # Dashboard content
        dashboard_label = ctk.CTkLabel(content_frame, text="Dashboard Dosen", font=("Arial", 20, "bold"), text_color=bg_color)
        dashboard_label.pack(pady=10)

        # Dosen info
        info_frame = ctk.CTkFrame(content_frame, fg_color="#FFFFFF")
        info_frame.pack(pady=10, padx=10, fill="x")

        dosen_info = [
            ("Nama", dosen_data[1]),
            ("Jenis Kelamin", dosen_data[6]),
            ("NIDN", dosen_data[2]),
            ("Program Studi", dosen_data[3]),
            ("Username", dosen_data[4])
        ]

        for key, value in dosen_info:
            info_row = ctk.CTkFrame(info_frame, fg_color="#FFFFFF")
            info_row.pack(fill="x", pady=2)
            key_label = ctk.CTkLabel(info_row, text=f"{key} :", width=15, anchor="w", text_color="black")
            key_label.pack(side="left", padx=5)
            value_label = ctk.CTkLabel(info_row, text=value, anchor="w", text_color="black")
            value_label.pack(side="left", padx=5)

        # Add new content for Pengisian KRS
    krs_title = ctk.CTkLabel(content_frame, text="Timeline semester", font=("Arial", 20, "bold"), text_color=bg_color)
    krs_title.pack(pady=10)

    table_frame = ctk.CTkFrame(content_frame, corner_radius=10, fg_color="#FFFFFF")
    table_frame.pack(pady=10, padx=10, fill="x")

    # Table header
    columns = ["Kode", "Tanggal Mulai", "Tanggal Selesai"]
    header_bg_color = "#5C0A0A"
    header_text_color = "#FFFFFF"
    for col in columns:
        col_label = ctk.CTkLabel(table_frame, text=col, anchor="w", fg_color=header_bg_color, text_color=header_text_color, width=10)
        col_label.grid(row=0, column=columns.index(col), padx=1, pady=5, sticky="nsew")

    # Sample data for the table (You can add more rows as needed)
    data = [
        ["Batas Akhir Entry Nilai","01 APR 2024", "30 JUN 2024"],
        ["Minggu Tenang", "03 JUN 2024", "08 JUN 2024"],
        ["Kegiatan Belajar Mengajar/Kuliah", "05 FEB 2024", "31 MAY 2024"],
        ["Ujian Akhir Semester (UAS)", "10 JUN 2024", "21 JUN 2024"],
        ["Pengisian Perubahan KRS (KPRS)", "12 FEB 2024", "23 FEB 2024"],
        ["Ujian Tengah Semester (UTS)", "25 MAR 2024", "05 APR 2024"],
        ["Pengisian Kartu Rencana Studi (KRS)", "29 JAN 2024", "31 JAN 2024"],
    ]

    # Create table cells and fill with data
    for i, row_data in enumerate(data, start=1):
        for j, val in enumerate(row_data):
            cell = ctk.CTkLabel(table_frame, text=val, anchor="w", fg_color="#FFFFFF", text_color="#000000")
            cell.grid(row=i, column=j, padx=1, pady=5, sticky="nsew")

    # Configure column weights for responsive design
    for i in range(len(columns)):
        table_frame.columnconfigure(i, weight=1)

def get_courses_for_program(program_studi):
    conn = sqlite3.connect('university.db')
    c = conn.cursor()
    c.execute("SELECT kode, nama_matkul, sks, nama_dosen, jadwal, ruang_kuliah FROM matkul WHERE program_studi = ?", (program_studi,))
    courses = c.fetchall()
    conn.close()
    return courses

data = []  # This will store the selected courses\

def simpan_krs_mahasiswa(nama_lengkap, matkul_list):
    conn = sqlite3.connect('university.db')
    c = conn.cursor()
    for matkul in matkul_list:
        kode_matkul, nama_matkul, sks = matkul[0], matkul[1], matkul[2]
        c.execute("INSERT INTO krs_mahasiswa (nama_lengkap, kode_matkul, nama_matkul, sks) VALUES (?, ?, ?, ?)", (nama_lengkap, kode_matkul, nama_matkul, sks))
    conn.commit()
    conn.close()

def show_pengisian_krs(content_frame, username):
    # Fetch student's program_studi from the database
    conn = sqlite3.connect('university.db')
    c = conn.cursor()
    c.execute("SELECT program_studi FROM mahasiswa WHERE username = ?", (username,))
    program_studi = c.fetchone()[0]
    conn.close()

    # Fetch courses for the student's program_studi
    data_pilihan = get_courses_for_program(program_studi)

    def add_to_table():
        selected_course = course_combo.get()
        selected_course_data = next((item for item in data_pilihan if item[1] == selected_course), None)
        if selected_course_data:
            new_row = list(selected_course_data)
            new_row.append("")  # Placeholder for Action column
            data.append(new_row)
            update_table()
            update_total_sks()

    def delete_row(row_index):
        data.pop(row_index)
        update_table()
        update_total_sks()

    def update_table():
        # Clear existing table rows
        for widget in table_frame.winfo_children():
            if isinstance(widget, ctk.CTkLabel) or isinstance(widget, ctk.CTkButton):
                widget.destroy()

        # Add table header
        for col in columns:
            col_label = ctk.CTkLabel(table_frame, text=col, anchor="w", fg_color=header_bg_color, text_color=header_text_color, width=10)
            col_label.grid(row=0, column=columns.index(col), padx=1, pady=5, sticky="nsew")

        # Add table data
        for i, row in enumerate(data, start=1):
            for j, val in enumerate(row):
                cell = ctk.CTkLabel(table_frame, text=val, anchor="w", fg_color="#FFFFFF", text_color="#000000")
                cell.grid(row=i, column=j, padx=1, pady=5, sticky="nsew")
                if j == len(row) - 1:  # Action column
                    del_btn = ctk.CTkButton(table_frame, text="🗑️", width=10, fg_color="#FFFFFF", text_color="#000000", command=lambda r=i-1: delete_row(r))
                    del_btn.grid(row=i, column=j, padx=1, pady=5)

    def update_total_sks():
        total_sks = sum(row[2] for row in data)
        total_sks_value.configure(text=str(total_sks))

    def submit_krs():
        simpan_krs_mahasiswa(username, data)

    # Clear existing content in the content_frame
    for widget in content_frame.winfo_children():
        widget.destroy()

    # Add new content
    krs_title = ctk.CTkLabel(content_frame, text="Pengisian Kartu Rencana Studi", font=("Arial", 20, "bold"), text_color="#5C0A0A")
    krs_title.pack(pady=10)

    # Add notification section
    notif_frame = ctk.CTkFrame(content_frame, corner_radius=10, fg_color="#FFFFFF")
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

    # Configure column weights for responsive design
    notif_frame.columnconfigure(0, weight=1)
    notif_frame.columnconfigure(1, weight=1)
    notif_frame.columnconfigure(2, weight=2)

    table_frame = ctk.CTkFrame(content_frame, corner_radius=10, fg_color="#FFFFFF")
    table_frame.pack(pady=10, padx=10, fill="x")

    # Table header
    columns = ["Kode", "Mata Kuliah", "SKS", "Pengajar", "Jadwal", "Ruang Kuliah", "Aksi"]
    header_bg_color = "#5C0A0A"
    header_text_color = "#FFFFFF"

    data = []

    # Input form
    form_frame = ctk.CTkFrame(content_frame, corner_radius=10, fg_color="#FFFFFF")
    form_frame.pack(pady=10, padx=10, fill="x")

    ctk.CTkLabel(form_frame, text="Pilih Mata Kuliah:", anchor="w", fg_color="#FFFFFF", text_color="#000000").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    course_combo = ctk.CTkComboBox(form_frame, values=[item[1] for item in data_pilihan], fg_color="#FFFFFF", text_color="#000000")
    course_combo.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    add_btn = ctk.CTkButton(form_frame, text="Tambah", fg_color="#3E0A0A", command=add_to_table)
    add_btn.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

    # Total SKS frame
    total_sks_frame = ctk.CTkFrame(content_frame, fg_color="#FFFFFF")
    total_sks_frame.pack(pady=10, padx=10, fill="x")

    total_sks_label = ctk.CTkLabel(total_sks_frame, text="Total SKS yang Diambil:", anchor="w", fg_color="#FFFFFF", text_color="#000000")
    total_sks_label.grid(row=0, column=0, padx=(0, 5), pady=5, sticky="w")

    total_sks_value = ctk.CTkLabel(total_sks_frame, text="0", anchor="w", fg_color="#FFFFFF", text_color="#000000")
    total_sks_value.grid(row=0, column=1, padx=(0, 5), pady=5, sticky="w")

    total_sks_frame.columnconfigure(0, weight=0)
    total_sks_frame.columnconfigure(1, weight=0)


    for i in range(len(columns)):
        table_frame.columnconfigure(i, weight=1)

    # Tombol submit untuk menyimpan KRS
    submit_btn = ctk.CTkButton(content_frame, text="Submit", fg_color="#3E0A0A", command=submit_krs)
    submit_btn.pack(pady=20)

    # Initial table update
    update_table()

def dapatkan_krs_mahasiswa():
    conn = sqlite3.connect('university.db')
    c = conn.cursor()
    c.execute("SELECT id, nama_lengkap, kode_matkul, nama_matkul, sks, status_approval FROM krs_mahasiswa")
    data_krs = c.fetchall()
    conn.close()
    return data_krs

def show_krs_dosen():
    # Clear existing content in the content_frame
    for widget in content_frame.winfo_children():
        widget.destroy()

    krs_title = ctk.CTkLabel(content_frame, text="KRS", font=("Arial", 20, "bold"), text_color=bg_color)
    krs_title.pack(pady=10)

    table_frame = ctk.CTkFrame(content_frame, corner_radius=10, fg_color="#FFFFFF")
    table_frame.pack(pady=10, padx=10, fill="x")

    # Table header
    columns = ["No.", "Nama Mahasiswa", "Kode Matkul", "Nama Matkul", "SKS", "Status Approval", "Approve", "Tidak Approve"]
    header_bg_color = "#5C0A0A"
    header_text_color = "#FFFFFF"
    for col in columns:
        col_label = ctk.CTkLabel(table_frame, text=col, anchor="w", fg_color=header_bg_color, text_color=header_text_color, width=10)
        col_label.grid(row=0, column=columns.index(col), padx=1, pady=5, sticky="nsew")

    data_krs = dapatkan_krs_mahasiswa()

    # Create table cells and fill with data
    for i, row_data in enumerate(data_krs, start=1):
        for j, val in enumerate(row_data):
            cell = ctk.CTkLabel(table_frame, text=val, anchor="w", fg_color="#FFFFFF", text_color="#000000")
            cell.grid(row=i, column=j, padx=1, pady=5, sticky="nsew")

        krs_id = row_data[0]  # Assuming the KRS ID is the first element in row_data

        # Add approve and disapprove buttons in the last columns
        approve_btn = ctk.CTkButton(table_frame, text="Approve", fg_color="#3E8E41", text_color="#FFFFFF",
                                    command=lambda k=krs_id: update_approval_status(k, "Approved"))
        approve_btn.grid(row=i, column=len(columns) - 2, padx=1, pady=5)

        disapprove_btn = ctk.CTkButton(table_frame, text="Tidak Approve", fg_color="#E8453C", text_color="#FFFFFF",
                                       command=lambda k=krs_id: update_approval_status(k, "Tidak Approved"))
        disapprove_btn.grid(row=i, column=len(columns) - 1, padx=1, pady=5)

    # Configure column weights for responsive design
    for i in range(len(columns)):
        table_frame.columnconfigure(i, weight=1)

def update_approval_status(krs_id, status):
    conn = sqlite3.connect('university.db')
    c = conn.cursor()
    c.execute("UPDATE krs_mahasiswa SET status_approval = ? WHERE id = ?", (status, krs_id))
    conn.commit()
    conn.close()
    print(f"Updated KRS ID {krs_id} to status {status}")  # Debug statement
    # Refresh the KRS display after updating the status
    show_krs_dosen()

def show_kartu_rencana_studi():
    # Clear existing content in the content_frame
    for widget in content_frame.winfo_children():
        widget.destroy()

    # Add new content for Pengisian KRS
    krs_title = ctk.CTkLabel(content_frame, text="Menampilkan Kartu Rencana Studi", font=("Arial", 20, "bold"), text_color="#5C0A0A")
    krs_title.pack(pady=10)

    table_frame = ctk.CTkFrame(content_frame, corner_radius=10, fg_color="#FFFFFF")
    table_frame.pack(pady=10, padx=10, fill="x")

    # Table header
    columns = ["Kode", "Mata Kuliah", "SKS", "Approval"]
    header_bg_color = "#5C0A0A"
    header_text_color = "#FFFFFF"
    for col in columns:
        col_label = ctk.CTkLabel(table_frame, text=col, anchor="w", fg_color=header_bg_color, text_color=header_text_color, width=10)
        col_label.grid(row=0, column=columns.index(col), padx=1, pady=5, sticky="nsew")

    conn = sqlite3.connect('university.db')
    c = conn.cursor()
    c.execute("SELECT nama_lengkap, kode_matkul, nama_matkul, sks, status_approval FROM krs_mahasiswa")
    data_krs = c.fetchall()
    conn.close()

    # Create table cells and fill with data
    for i, row_data in enumerate(data_krs, start=1):
        for j, val in enumerate(row_data[1:]):
            cell = ctk.CTkLabel(table_frame, text=val, anchor="w", fg_color="#FFFFFF", text_color="#000000")
            cell.grid(row=i, column=j, padx=1, pady=5, sticky="nsew")

    # Configure column weights for responsive design
    for i in range(len(columns)):
        table_frame.columnconfigure(i, weight=1)

def show_jadwal_kuliah():
    # Clear existing content in the content_frame
    for widget in content_frame.winfo_children():
        widget.destroy()

    jadwal_title = ctk.CTkLabel(content_frame, text="Jadwal Kuliah", font=("Arial", 20, "bold"), text_color=bg_color)
    jadwal_title.pack(pady=10)

    jadwal_info = ctk.CTkLabel(content_frame, text="Pilih Mata Kuliah:", font=("Arial", 16), text_color=bg_color)
    jadwal_info.pack(pady=10)

    # Connect to the database and fetch class options
    conn = sqlite3.connect('university.db')
    c = conn.cursor()
    c.execute("SELECT DISTINCT nama_matkul FROM matkul")
    lesson_options = [row[0] for row in c.fetchall()]
    conn.close()

    selected_lesson = ctk.StringVar(value=lesson_options[0])

    lesson_dropdown = ctk.CTkComboBox(content_frame, values=lesson_options, variable=selected_lesson, font=("Arial", 14), text_color="black", fg_color="white")
    lesson_dropdown.pack(pady=10)

    def show_schedule_today():
        # Clear existing content in the schedule_frame
        for widget in schedule_frame.winfo_children():
            widget.destroy()

        # Get the current day of the week
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

        # Connect to the database and fetch today's class options
        conn = sqlite3.connect('university.db')
        c = conn.cursor()
        c.execute("SELECT kode, nama_matkul, sks, jadwal, ruang_kuliah, nama_dosen FROM matkul WHERE jadwal LIKE ?", (today_day + '%',))
        courses_data = c.fetchall()
        conn.close()

        # Display Date Header
        today_date = datetime.date.today().strftime("%d/%m/%Y")
        date_frame = ctk.CTkFrame(schedule_frame, fg_color=highlight_color)
        date_frame.pack(fill="x", padx=10, pady=5)
        date_label = ctk.CTkLabel(date_frame, text=f"Jadwal Hari Ini ({today_date})", font=("Arial", 14, "bold"), text_color=fg_color)
        date_label.pack(pady=5)

        if not courses_data:
            no_class_label = ctk.CTkLabel(date_frame, text="No classes scheduled", text_color=fg_color)
            no_class_label.pack()
        else:
            # Create headers for the course schedule
            headers = ["Kode", "Mata Kuliah", "SKS", "Jadwal Kuliah", "Ruang", "Dosen"]

            # Create header frame
            header_frame = ctk.CTkFrame(schedule_frame, fg_color=highlight_color)
            header_frame.pack(fill="x")
            for header in headers:
                header_label = ctk.CTkLabel(header_frame, text=header, anchor="w", text_color=fg_color, padx=5, pady=5)
                header_label.pack(side="left", expand=True, fill="x")

            # Create rows for the course schedule
            for course in courses_data:
                row_frame = ctk.CTkFrame(schedule_frame, fg_color="#FFFFFF")
                row_frame.pack(fill="x", padx=5, pady=2)
                
                for value in course:
                    cell_label = ctk.CTkLabel(row_frame, text=value, anchor="w", text_color="black", padx=5, pady=5)
                    cell_label.pack(side="left", expand=True, fill="x")

    def show_schedule_weekly():
        # Clear existing content in the schedule_frame
        for widget in schedule_frame.winfo_children():
            widget.destroy()

        # Get the current week dates
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

        # Connect to the database and fetch weekly class options
        conn = sqlite3.connect('university.db')
        c = conn.cursor()
        c.execute("SELECT kode, nama_matkul, sks, jadwal, ruang_kuliah, nama_dosen FROM matkul")
        courses_data = c.fetchall()
        conn.close()

        # Create a dictionary to store courses by day
        schedule_data = {day: [] for day in week_days}
        for course in courses_data:
            day_of_week = course[3].split(',')[0]
            if day_of_week in schedule_data:
                schedule_data[day_of_week].append(course)

        # Display weekly schedule
        for date, day in zip(dates, week_days):
            date_frame = ctk.CTkFrame(schedule_frame, fg_color=highlight_color)
            date_frame.pack(fill="x", padx=10, pady=5)
            date_label = ctk.CTkLabel(date_frame, text=f"{day} ({date})", font=("Arial", 14, "bold"), text_color=fg_color)
            date_label.pack(pady=5)

            if not schedule_data[day]:
                no_class_label = ctk.CTkLabel(date_frame, text="No classes scheduled", text_color=fg_color)
                no_class_label.pack()
            else:
                # Create headers for the course schedule
                headers = ["Kode", "Mata Kuliah", "SKS", "Jadwal Kuliah", "Ruang", "Dosen"]

                # Create header frame
                header_frame = ctk.CTkFrame(schedule_frame, fg_color=highlight_color)
                header_frame.pack(fill="x")
                for header in headers:
                    header_label = ctk.CTkLabel(header_frame, text=header, anchor="w", text_color=fg_color, padx=5, pady=5)
                    header_label.pack(side="left", expand=True, fill="x")

                # Create rows for the course schedule
                for course in schedule_data[day]:
                    row_frame = ctk.CTkFrame(schedule_frame, fg_color="#FFFFFF")
                    row_frame.pack(fill="x", padx=5, pady=2)
                    
                    for value in course:
                        cell_label = ctk.CTkLabel(row_frame, text=value, anchor="w", text_color="black", padx=5, pady=5)
                        cell_label.pack(side="left", expand=True, fill="x")

    # Button to show today's schedule
    show_schedule_today_button = ctk.CTkButton(content_frame, text="Tampilkan Jadwal Hari Ini", fg_color=highlight_color, text_color=fg_color, font=("Arial", 14), command=show_schedule_today)
    show_schedule_today_button.pack(pady=10)

    # Button to show weekly schedule
    show_schedule_weekly_button = ctk.CTkButton(content_frame, text="Tampilkan Jadwal Mingguan", fg_color=highlight_color, text_color=fg_color, font=("Arial", 14), command=show_schedule_weekly)
    show_schedule_weekly_button.pack(pady=10)

    # Frame to display schedule
    global schedule_frame
    schedule_frame = ctk.CTkFrame(content_frame, fg_color="#FFFFFF")
    schedule_frame.pack(fill="both", expand=True)

def show_hasil_studi():
    # Clear existing content in the content_frame
    for widget in content_frame.winfo_children():
        widget.destroy()

    # Add new content for Pengisian KRS
    krs_title = ctk.CTkLabel(content_frame, text="Hasil Studi Mahasiswa", font=("Arial", 20, "bold"), text_color=bg_color)
    krs_title.pack(pady=10)

    table_frame = ctk.CTkFrame(content_frame, corner_radius=10, fg_color="#FFFFFF")
    table_frame.pack(pady=10, padx=10, fill="x")

    # Table header
    columns = ['ID', 'Nama Lengkap', 'Nama Matkul', 'Grade', 'Score']
    header_bg_color = "#5C0A0A"
    header_text_color = "#FFFFFF"
    for col in columns:
        col_label = ctk.CTkLabel(table_frame, text=col, anchor="w", fg_color=header_bg_color, text_color=header_text_color, width=10)
        col_label.grid(row=0, column=columns.index(col), padx=1, pady=5, sticky="nsew")

    # Connect to the database and fetch data from the table nilai
    conn = sqlite3.connect('university.db')
    c = conn.cursor()
    c.execute("SELECT * FROM nilai WHERE nama_lengkap = 'Bintang Berlian Pratama' ")
    data = c.fetchall()
    conn.close()

    # Create table cells and fill with data
    total_score = 0
    total_sks = 0
    for i, row_data in enumerate(data, start=1):
        for j, val in enumerate(row_data):
            cell = ctk.CTkLabel(table_frame, text=val, anchor="w", fg_color="#FFFFFF", text_color="#000000")
            cell.grid(row=i, column=j, padx=1, pady=5, sticky="nsew")
            
            if j == 4 and val is not None:  # Score column
                total_score += val
                total_sks += 1  # Assuming each score corresponds to one SKS; adjust if necessary

    # Calculate IP Semester
    if total_sks > 0:
        ip_semester = total_score / total_sks
    else:
        ip_semester = 0.0

    # Additional table for IP Semester, IP Kumulatif, and Status Akademik
    additional_table_frame = ctk.CTkFrame(content_frame, corner_radius=10, fg_color="#FFFFFF")
    additional_table_frame.pack(pady=10, padx=10, fill="x")

    additional_labels = ['IP Semester', 'IP Kumulatif', 'Status Akademik']
    additional_entries = {}

    for i, label in enumerate(additional_labels):
        row_label = ctk.CTkLabel(additional_table_frame, text=label, anchor="w", fg_color="#FFFFFF", text_color="#000000")
        row_label.grid(row=i, column=0, padx=1, pady=5, sticky="nsew")

        entry = ctk.CTkEntry(additional_table_frame, fg_color="#FFFFFF", text_color="#000000")
        entry.grid(row=i, column=1, padx=1, pady=5, sticky="nsew")
        entry.configure(state="readonly")
        additional_entries[label] = entry

    # Set IP Semester value
    additional_entries['IP Semester'].configure(state="normal")
    additional_entries['IP Semester'].insert(0, f"{ip_semester:.2f}")
    additional_entries['IP Semester'].configure(state="readonly")

    # Assuming IP Kumulatif is the same as IP Semester for this example
    additional_entries['IP Kumulatif'].configure(state="normal")
    additional_entries['IP Kumulatif'].insert(0, f"{ip_semester:.2f}")
    additional_entries['IP Kumulatif'].configure(state="readonly")

    # Status Akademik example logic
    if ip_semester >= 3.00:
        status = "Baik"
    elif ip_semester >= 2.00:
        status = "Cukup"
    else:
        status = "Kurang"
    additional_entries['Status Akademik'].configure(state="normal")
    additional_entries['Status Akademik'].insert(0, status)
    additional_entries['Status Akademik'].configure(state="readonly")

    # Configure column weights for responsive design
    for i in range(len(columns)):
        table_frame.columnconfigure(i, weight=1)
    for i in range(2):  # Two columns in the additional table
        additional_table_frame.columnconfigure(i, weight=1)

def show_kehadiran_mahasiswa():
    # Clear existing content in the content_frame
    for widget in content_frame.winfo_children():
        widget.destroy()

    # Add new content for Pengisian KRS
    krs_title = ctk.CTkLabel(content_frame, text="Menampilkan Halaman kehadiran Mahasiswa", font=("Arial", 20, "bold"), text_color=bg_color)
    krs_title.pack(pady=10)

    table_frame = ctk.CTkFrame(content_frame, corner_radius=10, fg_color="#FFFFFF")
    table_frame.pack(pady=10, padx=10, fill="x")

    # Connect to the database and fetch approved KRS data
    conn = sqlite3.connect('university.db')
    c = conn.cursor()
    c.execute("SELECT kode_matkul, nama_matkul, sks FROM krs_mahasiswa WHERE status_approval = 'Approved'")
    data = c.fetchall()

    # Table header
    columns = ["Kode", "Mata Kuliah", "SKS", "Jumlah Kehadiran (%)"]
    header_bg_color = "#5C0A0A"
    header_text_color = "#FFFFFF"
    for col in columns:
        col_label = ctk.CTkLabel(table_frame, text=col, anchor="w", fg_color=header_bg_color, text_color=header_text_color, width=10)
        col_label.grid(row=0, column=columns.index(col), padx=1, pady=5, sticky="nsew")

    # Create table cells and fill with data
    for i, row_data in enumerate(data, start=1):
        kode_matkul, nama_matkul, sks = row_data

        # Calculate attendance percentage
        c.execute("SELECT COUNT(*) FROM kehadiran WHERE kode_matkul = ? AND kehadiran = 'Hadir'", (kode_matkul,))
        total_hadir = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM kehadiran WHERE kode_matkul = ?", (kode_matkul,))
        total_pertemuan = c.fetchone()[0]
        if total_pertemuan > 0:
            kehadiran_persen = (total_hadir / total_pertemuan) * 100
        else:
            kehadiran_persen = 0

        row_data_with_kehadiran = row_data + (f"{kehadiran_persen:.2f}%",)
        for j, val in enumerate(row_data_with_kehadiran):
            cell = ctk.CTkLabel(table_frame, text=val, anchor="w", fg_color="#FFFFFF", text_color="#000000")
            cell.grid(row=i, column=j, padx=1, pady=5, sticky="nsew")

    conn.close()

    # Configure column weights for responsive design
    for i in range(len(columns)):
        table_frame.columnconfigure(i, weight=1)

    # Frame for the table summary
    summary_frame = ctk.CTkFrame(content_frame, corner_radius=10, fg_color="#FFFFFF")
    summary_frame.pack(pady=10, padx=10, fill="x")

    # Table header
    header_frame = ctk.CTkFrame(summary_frame, fg_color="#5C0A0A")
    header_frame.grid(row=0, column=0, columnspan=3, sticky="nsew")

    header_label = ctk.CTkLabel(header_frame, text="Kehadiran Mahasiswa", font=ctk.CTkFont(size=14, weight="bold"), text_color="#FFFFFF")
    header_label.pack(padx=5, pady=5, anchor="w")

    # Table content for summary
    notif_data = [
        ("Total Kehadiran", "0"),
        ("Total Ketidakhadiran", "0"),
        ("Persentase Kehadiran", "0%"),
    ]

    # Fetch attendance summary data from the database
    conn = sqlite3.connect('university.db')
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM kehadiran WHERE kehadiran = 'Hadir'")
    total_kehadiran = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM kehadiran WHERE kehadiran = 'Tidak Hadir'")
    total_tidak_hadir = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM kehadiran WHERE kehadiran = 'Izin'")
    total_izin = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM kehadiran WHERE kehadiran = 'Sakit'")
    total_sakit = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM kehadiran WHERE kehadiran = 'Alfa'")
    total_alfa = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM kehadiran")
    total_record = c.fetchone()[0]
    if total_record > 0:
        persentase_kehadiran = (total_kehadiran / total_record) * 100
    else:
        persentase_kehadiran = 0

    notif_data = [
        ("Total Kehadiran", total_kehadiran),
        ("Total Ketidakhadiran", total_tidak_hadir),
        ("Persentase Kehadiran", f"{persentase_kehadiran:.2f}%"),
    ]

    conn.close()

    for i, (key, value) in enumerate(notif_data, start=1):
        key_label = ctk.CTkLabel(summary_frame, text=key, anchor="w", fg_color="#FFFFFF", text_color="#000000")
        key_label.grid(row=i, column=0, padx=5, pady=5, sticky="nsew")
        
        value_label = ctk.CTkLabel(summary_frame, text=value, anchor="w", fg_color="#FFFFFF", text_color="#000000")
        value_label.grid(row=i, column=1, padx=5, pady=5, sticky="nsew", columnspan=2)

    # Configure column weights for responsive design
    summary_frame.columnconfigure(0, weight=1)
    summary_frame.columnconfigure(1, weight=1)
    summary_frame.columnconfigure(2, weight=2)

def show_kehadiran_mahasiswa_dosen():
    # Clear existing content in the content_frame
    for widget in content_frame.winfo_children():
        widget.destroy()

    kehadiran_title = ctk.CTkLabel(content_frame, text="Kehadiran Mahasiswa", font=("Arial", 20, "bold"), text_color=bg_color)
    kehadiran_title.pack(pady=10)
 
    kehadiran_info = ctk.CTkLabel(content_frame, text="Pilih Kelas:", font=("Arial", 16), text_color=bg_color)
    kehadiran_info.pack(pady=10)

    # Connect to the database and fetch class options
    conn = sqlite3.connect('university.db')
    c = conn.cursor()
    c.execute("SELECT nama_matkul, kode FROM matkul")
    class_options = [(row[0], row[1]) for row in c.fetchall()]
    conn.close()

    # Create a dropdown to select class
    selected_class = ctk.StringVar(value=class_options[0][0])
    selected_class_code = ctk.StringVar(value=class_options[0][1])

    class_dropdown = ctk.CTkComboBox(content_frame, values=[option[0] for option in class_options], variable=selected_class, font=("Arial", 14), text_color="black", fg_color="white")
    class_dropdown.pack(pady=10)

    def update_selected_class_code(*args):
        for option in class_options:
            if option[0] == selected_class.get():
                selected_class_code.set(option[1])
                break

    selected_class.trace("w", update_selected_class_code)

    def show_students():
        # Clear existing content in the student_frame
        for widget in student_frame.winfo_children():
            widget.destroy()

        conn = sqlite3.connect('university.db')
        c = conn.cursor()
        c.execute("SELECT nim, nama_lengkap FROM mahasiswa")
        students = c.fetchall()
        conn.close()

        # Assume highlight_color and fg_color are defined elsewhere
        highlight_color = "#5C0A0A"
        fg_color = "#FFFFFF"

        headers = ["NIM", "Nama", "Tanggal", "Kehadiran"]

        # Create the table frame
        table_frame = ctk.CTkFrame(student_frame, corner_radius=10, fg_color="#FFFFFF")
        table_frame.pack(pady=10, padx=10, fill="x")

        # Create headers
        header_frame = ctk.CTkFrame(table_frame, fg_color=highlight_color)
        header_frame.pack(fill="x")
        for header in headers:
            header_label = ctk.CTkLabel(header_frame, text=header, anchor="w", fg_color=highlight_color, text_color=fg_color, width=10)
            header_label.pack(side="left", padx=1, pady=5, fill="x", expand=True)

        # Create rows
        student_entries = []
        for student in students:
            student_row = ctk.CTkFrame(table_frame, fg_color="#FFFFFF")
            student_row.pack(fill="x")

            nim_label = ctk.CTkLabel(student_row, text=student[0], anchor="w", text_color="black", width=10)
            nim_label.pack(side="left", padx=1, pady=5, fill="x", expand=True)

            name_label = ctk.CTkLabel(student_row, text=student[1], anchor="w", text_color="black", width=10)
            name_label.pack(side="left", padx=1, pady=5, fill="x", expand=True)

            date_entry = DateEntry(student_row, width=12, background='darkblue', foreground='white', borderwidth=2)
            date_entry.pack(side="left", padx=1, pady=5, fill="x", expand=True)

            presence_var = ctk.StringVar(value="Hadir")
            presence_dropdown = ctk.CTkComboBox(student_row, values=["Hadir", "Tidak Hadir"], variable=presence_var, width=10, text_color="black", fg_color="white")
            presence_dropdown.pack(side="left", padx=1, pady=5, fill="x", expand=True)

            student_entries.append((nim_label, name_label, date_entry, presence_dropdown))

        # Save button to submit attendance
        save_button = ctk.CTkButton(student_frame, text="Simpan Kehadiran", fg_color=highlight_color, text_color=fg_color, font=("Arial", 14), command=lambda: save_attendance(student_entries, selected_class_code.get()))
        save_button.pack(pady=10)

    def save_attendance(student_entries, kode_matkul):
        # Connect to the database
        conn = sqlite3.connect('university.db')
        c = conn.cursor()

        # Create table kehadiran if it doesn't exist
        c.execute('''
            CREATE TABLE IF NOT EXISTS kehadiran (
                nim TEXT,
                nama_lengkap TEXT,
                tanggal TEXT,
                kehadiran TEXT,
                kode_matkul TEXT
            )
        ''')

        attendance_records = []
        for entry in student_entries:
            student_nim = entry[0].cget("text")
            student_name = entry[1].cget("text")
            selected_date = entry[2].get_date().strftime('%Y-%m-%d')
            presence = entry[3].get()
            attendance_records.append((student_nim, student_name, selected_date, presence, kode_matkul))

        # Insert attendance records into the database
        c.executemany('INSERT INTO kehadiran (nim, nama_lengkap, tanggal, kehadiran, kode_matkul) VALUES (?, ?, ?, ?, ?)', attendance_records)
        conn.commit()
        conn.close()

        print(f"Attendance records saved: {attendance_records}")

    # Button to show students
    show_students_button = ctk.CTkButton(content_frame, text="Tampilkan Mahasiswa", fg_color=highlight_color, text_color=fg_color, font=("Arial", 14), command=show_students)
    show_students_button.pack(pady=10)

    # Frame to display students
    student_frame = ctk.CTkFrame(content_frame, fg_color="#FFFFFF")
    student_frame.pack(fill="both", expand=True)

def show_penilaian():
    # Clear existing content in the content_frame
    for widget in content_frame.winfo_children():
        widget.destroy()

    # Add title
    penilaian_title = ctk.CTkLabel(content_frame, text="Penilaian", font=("Arial", 20, "bold"), text_color=bg_color)
    penilaian_title.pack(pady=10)

    # Frame for class and lesson selection
    selection_frame = ctk.CTkFrame(content_frame, fg_color="#FFFFFF")
    selection_frame.pack(pady=10, padx=10, fill="x")

    # Connect to the database and fetch class options
    conn = sqlite3.connect('university.db')
    c = conn.cursor()
    c.execute("SELECT nama_matkul FROM matkul")
    class_options = [row[0] for row in c.fetchall()]
    conn.close()

    if not class_options:
        class_options = ["No classes available"]
    selected_class = ctk.StringVar(value=class_options[0])

    # Create label and dropdown in the same frame
    lesson_label = ctk.CTkLabel(selection_frame, text="Pilih Mata Kuliah:", font=("Arial", 14), text_color=bg_color)
    lesson_label.pack(side="left", padx=5, pady=5)
    lesson_dropdown = ctk.CTkComboBox(selection_frame, values=class_options, variable=selected_class, font=("Arial", 14), text_color="black", fg_color="white")
    lesson_dropdown.pack(side="left", padx=5, pady=5)

    def save_penilaian():
        # Iterate over student rows and collect grades
        for row_frame in student_rows:
            student_name = row_frame.student_label.cget("text")
            grade = row_frame.grade_dropdown.get()

            # Calculate numeric score from grade (example scale)
            grade_to_score = {
                "A": 4.0, "A-": 3.7, "A/B": 3.5,
                "B+": 3.3, "B": 3.0, "B-": 2.7, "B/C": 2.5,
                "C+": 2.3, "C": 2.0, "C-": 1.7, "C/D": 1.5,
                "D+": 1.3, "D": 1.0, "E": 0.0
            }
            score = grade_to_score.get(grade, 0.0)

            print(f"Updating: {student_name}, Grade: {grade}, Score: {score}, Class: {selected_class.get()}")

            try:
                # Update database with grade and score
                conn = sqlite3.connect('university.db')
                c = conn.cursor()
                c.execute("""
                    INSERT INTO nilai (nama_lengkap, nama_matkul, grade, score)
                    VALUES (?, ?, ?, ?)
                """, (student_name, selected_class.get(), grade, score))
                conn.commit()
                conn.close()
                print("Update successful")
            except sqlite3.Error as e:
                print(f"An error occurred: {e}")

    def show_student_table():
        global student_rows
        student_rows = []
        # Clear existing content in the student_frame
        for widget in student_frame.winfo_children():
            widget.destroy()

        conn = sqlite3.connect('university.db')
        c = conn.cursor()
        c.execute("SELECT nama_lengkap FROM mahasiswa")
        students = c.fetchall()
        conn.close()

        # Create headers
        header_frame = ctk.CTkFrame(student_frame, fg_color=highlight_color)
        header_frame.pack(fill="x")
        headers = ["Nama", "Nilai"]
        for header in headers:
            header_label = ctk.CTkLabel(header_frame, text=header, anchor="w", text_color=fg_color)
            header_label.pack(side="left", padx=5, pady=5, expand=True)

        # Create rows for each student
        grade_options = ["A", "A-", "A/B", "B+", "B", "B-", "B/C", "C+", "C", "C-", "C/D", "D+", "D", "E"]
        for student in students:
            row_frame = ctk.CTkFrame(student_frame, fg_color="#FFFFFF")
            row_frame.pack(fill="x")
            student_label = ctk.CTkLabel(row_frame, text=student[0], anchor="w", text_color="black")
            student_label.pack(side="left", padx=5, pady=5, expand=True)

            grade_dropdown = ctk.CTkComboBox(row_frame, values=grade_options, font=("Arial", 14),
                                             fg_color="white", text_color="black", dropdown_fg_color=highlight_color,
                                             dropdown_hover_color="#FF4500", dropdown_text_color="black")
            grade_dropdown.pack(side="left", padx=5, pady=5, expand=True)

            row_frame.student_label = student_label
            row_frame.grade_dropdown = grade_dropdown
            student_rows.append(row_frame)

        # Add save button
        save_button = ctk.CTkButton(student_frame, text="Simpan", command=save_penilaian, fg_color=highlight_color, hover_color="#c41212", font=("Arial", 14))
        save_button.pack(pady=10)

    # Button to show student table
    show_button = ctk.CTkButton(content_frame, text="Tampilkan Mahasiswa", command=show_student_table, fg_color=highlight_color, hover_color="#c41212", font=("Arial", 14))
    show_button.pack(pady=10)

    # Frame to hold student table
    student_frame = ctk.CTkFrame(content_frame, fg_color="#FFFFFF")
    student_frame.pack(pady=10, padx=10, fill="both", expand=True)

# Sample data for class schedules
schedule_data = {
    "14/12/2025": [],
    "13/12/2025": []
}

def show_jadwal_kuliah():
    # Clear existing content in the content_frame
    for widget in content_frame.winfo_children():
        widget.destroy()

    jadwal_title = ctk.CTkLabel(content_frame, text="Jadwal Kuliah", font=("Arial", 20, "bold"), text_color=bg_color)
    jadwal_title.pack(pady=10)

    def show_schedule_today():
        # Clear existing content in the schedule_frame
        for widget in schedule_frame.winfo_children():
            widget.destroy()

        # Get the current day of the week
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

        # Connect to the database and fetch today's class options
        conn = sqlite3.connect('university.db')
        c = conn.cursor()
        c.execute("SELECT kode, nama_matkul, sks, jadwal, ruang_kuliah, nama_dosen FROM matkul WHERE jadwal LIKE ?", (today_day + '%',))
        courses_data = c.fetchall()
        conn.close()

        # Display Date Header
        today_date = datetime.date.today().strftime("%d/%m/%Y")
        date_frame = ctk.CTkFrame(schedule_frame, fg_color=highlight_color)
        date_frame.pack(fill="x", padx=10, pady=5)
        date_label = ctk.CTkLabel(date_frame, text=f"Jadwal Hari Ini ({today_date})", font=("Arial", 14, "bold"), text_color=fg_color)
        date_label.pack(pady=5)

        if not courses_data:
            no_class_label = ctk.CTkLabel(date_frame, text="No classes scheduled", text_color=fg_color)
            no_class_label.pack()
        else:
            # Create headers for the course schedule
            headers = ["Kode", "Mata Kuliah", "SKS", "Jadwal Kuliah", "Ruang", "Dosen"]

            # Create header frame
            header_frame = ctk.CTkFrame(schedule_frame, fg_color=highlight_color)
            header_frame.pack(fill="x")
            for header in headers:
                header_label = ctk.CTkLabel(header_frame, text=header, anchor="w", text_color=fg_color, padx=5, pady=5)
                header_label.pack(side="left", expand=True, fill="x")

            # Create rows for the course schedule
            for course in courses_data:
                row_frame = ctk.CTkFrame(schedule_frame, fg_color="#FFFFFF")
                row_frame.pack(fill="x", padx=5, pady=2)
                
                for value in course:
                    cell_label = ctk.CTkLabel(row_frame, text=value, anchor="w", text_color="black", padx=5, pady=5)
                    cell_label.pack(side="left", expand=True, fill="x")

    def show_schedule_weekly():
        # Clear existing content in the schedule_frame
        for widget in schedule_frame.winfo_children():
            widget.destroy()

        # Get the current week dates
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

        # Connect to the database and fetch weekly class options
        conn = sqlite3.connect('university.db')
        c = conn.cursor()
        c.execute("SELECT kode, nama_matkul, sks, jadwal, ruang_kuliah, nama_dosen FROM matkul")
        courses_data = c.fetchall()
        conn.close()

        # Create a dictionary to store courses by day
        schedule_data = {day: [] for day in week_days}
        for course in courses_data:
            day_of_week = course[3].split(',')[0]
            if day_of_week in schedule_data:
                schedule_data[day_of_week].append(course)

        # Display weekly schedule
        for date, day in zip(dates, week_days):
            date_frame = ctk.CTkFrame(schedule_frame, fg_color=highlight_color)
            date_frame.pack(fill="x", padx=10, pady=5)
            date_label = ctk.CTkLabel(date_frame, text=f"{day} ({date})", font=("Arial", 14, "bold"), text_color=fg_color)
            date_label.pack(pady=5)

            if not schedule_data[day]:
                no_class_label = ctk.CTkLabel(date_frame, text="No classes scheduled", text_color=fg_color)
                no_class_label.pack()
            else:
                # Create headers for the course schedule
                headers = ["Kode", "Mata Kuliah", "SKS", "Jadwal Kuliah", "Ruang", "Dosen"]

                # Create header frame
                header_frame = ctk.CTkFrame(schedule_frame, fg_color=highlight_color)
                header_frame.pack(fill="x")
                for header in headers:
                    header_label = ctk.CTkLabel(header_frame, text=header, anchor="w", text_color=fg_color, padx=5, pady=5)
                    header_label.pack(side="left", expand=True, fill="x")

                # Create rows for the course schedule
                for course in schedule_data[day]:
                    row_frame = ctk.CTkFrame(schedule_frame, fg_color="#FFFFFF")
                    row_frame.pack(fill="x", padx=5, pady=2)
                    
                    for value in course:
                        cell_label = ctk.CTkLabel(row_frame, text=value, anchor="w", text_color="black", padx=5, pady=5)
                        cell_label.pack(side="left", expand=True, fill="x")

    # Define button dimensions
    button_width = 200  # Adjust as needed
    button_height = 40  # Adjust as needed

    # Frame for today's schedule button
    today_button_frame = ctk.CTkFrame(content_frame, fg_color=bg_color, width=button_width, height=button_height)
    today_button_frame.pack(pady=10, padx=20, anchor="center")
    today_button_frame.pack_propagate(False)

    # Button to show today's schedule
    show_schedule_today_button = ctk.CTkButton(today_button_frame, text="Tampilkan Jadwal Hari Ini", fg_color=highlight_color, text_color=fg_color, font=("Arial", 14), command=show_schedule_today, width=button_width, height=button_height)
    show_schedule_today_button.pack(fill="both", expand=True)

    # Frame for weekly schedule button
    weekly_button_frame = ctk.CTkFrame(content_frame, fg_color=bg_color, width=button_width, height=button_height)
    weekly_button_frame.pack(pady=10, padx=20, anchor="center")
    weekly_button_frame.pack_propagate(False)

    # Button to show weekly schedule
    show_schedule_weekly_button = ctk.CTkButton(weekly_button_frame, text="Tampilkan Jadwal Mingguan", fg_color=highlight_color, text_color=fg_color, font=("Arial", 14), command=show_schedule_weekly, width=button_width, height=button_height)
    show_schedule_weekly_button.pack(fill="both", expand=True)

    # Frame to display schedule
    global schedule_frame
    schedule_frame = ctk.CTkFrame(content_frame, fg_color="#FFFFFF")
    schedule_frame.pack(fill="both", expand=True)

# Initialize the database
initialize_db()

# Start the main application window
main_window()
