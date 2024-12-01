import tkinter as tk
from tkinter import messagebox
from queue import Queue
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json 
import re


pertanyaan = [
    {
        "question": "Saat berada di tim, peran apa yang paling kamu suka?",
        "answers": ["Menjaga rekan tim dan melindungi mereka", "Menyerang dari jarak jauh", "Menghabisi musuh yang sendirian", "Menghancurkan musuh dengan skill sihir", "Menyembuhkan atau membantu tim lainnya"],
        "scores": [20, 10, 30, 25, 15]
    },
    {
        "question": "Kamu lebih suka bermain dengan cara:",
        "answers": ["Menjadi yang paling tahan lama di medan perang", "Menjaga jarak dan menembak musuh dari belakang", "Mencari kesempatan untuk menyerang musuh yang terpisah", "Memberikan damage besar dalam waktu singkat dengan skill", "Membantu tim dengan heal atau buff"],
        "scores": [20, 10, 30, 25, 15]
    },
    {
        "question": "Jika rekan timmu diserang, kamu akan:",
        "answers": ["Melawan musuh di depan untuk melindungi mereka", "Memberikan damage jarak jauh dari belakang", "Mencari kesempatan untuk menghabisi musuh yang lemah", "Menggunakan skill area untuk menghancurkan banyak musuh", "Membantu tim dengan heal dan buff"],
        "scores": [20, 10, 30, 25, 15]
    },
    {
        "question": "Pilih satu kemampuan yang paling kamu nikmati dalam permainan:",
        "answers": ["Kemampuan untuk bertahan hidup lebih lama dan menjadi tank", "Kemampuan untuk menyerang musuh dari jarak jauh", "Kemampuan untuk bergerak cepat dan membunuh musuh", "Kemampuan untuk memberikan damage besar dengan skill", "Kemampuan untuk menyembuhkan tim dan memberikan buff"],
        "scores": [20, 10, 30, 25, 15]
    },
    {
        "question": "Bagaimana cara kamu menentukan strategi permainan?",
        "answers": ["Menjaga pertahanan tim dan menjaga posisi di garis depan", "Menunggu kesempatan untuk memberikan damage besar dari belakang", "Mengincar musuh yang lemah dan menyerang dengan cepat", "Menggunakan skill untuk memporak-porandakan musuh dengan area damage", "Membantu tim dengan heal dan memberikan buff untuk memperkuat tim"],
        "scores": [20, 10, 30, 25, 15]
    },
    
]


pertanyaan_queue = Queue()


perhitungan_stack = [0, 0, 0, 0, 0]


users = {}


def simpan_data_pengguna():
    with open("users.json", "w") as f:
        json.dump(users, f)

def muat_data_pengguna():
    global users
    try:
        with open("users.json", "r") as f:
            users = json.load(f)
            print("Users loaded:", users)
    except FileNotFoundError:
        users = {}  
        
char_kecocokan = {
    "Tank": "Kamu lebih suka bertahan hidup lebih lama dan menjadi pelindung bagi tim.",
    "Marksman": "Kamu adalah penyerang jarak jauh yang handal.",
    "Assassin": "Kamu suka menyerang musuh yang lemah.",
    "Mage": "Kamu menyukai kekuatan sihir untuk menyerang.",
    "Support": "Kamu suka membantu tim dan memperkuat mereka."
}

#
def hitung_hasil():
    total_score = sum(perhitungan_stack)
    total_max_score = len(pertanyaan) * 20
    normalized_score = (total_score / total_max_score) * 100
    normalized_score = min(normalized_score, 100)

    max_score_index = perhitungan_stack.index(max(perhitungan_stack))
    karakteristik = ["Tank", "Marksman", "Assassin", "Mage", "Support"]
    dominasi_char = karakteristik[max_score_index]

    messagebox.showinfo("Hasil Tes Kepribadian ML", 
                        f"Karakteristik permainan Mobile Legends kamu adalah: {dominasi_char}\n"
                        f"Skor kamu: {total_score} / {total_max_score}\n"
                        f"Persentase: {normalized_score:.2f}%")

    tampilkan_dashboard(dominasi_char, total_score, total_max_score)


def tampilkan_dashboard(dominasi_char, total_score, max_score):
    for widget in frame.winfo_children():
        widget.pack_forget()

    result_label = tk.Label(frame, text=f"Karakteristik permainan kamu adalah: {dominasi_char}\n"
                                       f"Skor kamu: {total_score} / {max_score}\n"
                                       f"Persentase: {(total_score / max_score) * 100:.2f}%", font=("perpetua", 10), bg="lightblue")
    result_label.pack(pady=10, anchor="center")

    karakteristik = ["Tank", "Marksman", "Assassin", "Mage", "Support"]

    fig, ax = plt.subplots(figsize=(4, 2))
    ax.bar(karakteristik, perhitungan_stack, color='skyblue')

    ax.set_xlabel('Karakteristik', fontsize=8)
    ax.set_ylabel('Skor', fontsize=8)
    ax.set_title('Hasil Tes Kepribadian Mobile Legends', fontsize=10)

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=10, anchor="center")

    tampilan_penjelasan = tk.Label(frame, text=char_kecocokan[dominasi_char], font=("perpetua", 9), wraplength=400, bg="lightblue")
    tampilan_penjelasan.pack(pady=30, anchor="center")

    tombol_kembali = tk.Button(frame, text="Kembali ke Menu Utama", command=tampilkan_menu_utama, font=("perpetua", 10), width=20, height=1)
    tombol_kembali.pack(pady=10, anchor="center")

    tombol_restart = tk.Button(frame, text="Mulai Tes Lagi", command=mulai_tes, font=("perpetua", 10), width=20, height=1)
    tombol_restart.pack(pady=5, anchor="center")


def tampilkan_menu_login():
    for widget in frame.winfo_children():
        widget.pack_forget()

    login_label = tk.Label(frame, text="Masukkan Username dan Password Anda", font=("perpetua", 12), bg="lightblue")
    login_label.pack(pady=10, anchor="center")

    username_entry = tk.Entry(frame, font=("perpetua", 12))
    username_entry.pack(pady=10, anchor="center")

    password_entry = tk.Entry(frame, font=("perpetua", 12), show="*")
    password_entry.pack(pady=10, anchor="center")

    def login():
        username = username_entry.get()
        password = password_entry.get()
        print(f"Trying to login with Username: {username} and Password: {password}")
        if username in users and users[username]["password"] == password:
            messagebox.showinfo("Selamat Anda Login", f"Selamat datang, {username}!")
            tampilkan_menu_utama()
        else:
            messagebox.showerror("Error", "Username atau password salah!")

    login_button = tk.Button(frame, text="Login", font=("perpetua", 12), command=login)
    login_button.pack(pady=10, anchor="center")

    register_button = tk.Button(frame, text="Registrasi Pengguna Baru", font=("perpetua", 12), command=tampilkan_menu_registrasi)
    register_button.pack(pady=10, anchor="center")


def tampilkan_menu_registrasi():
    for widget in frame.winfo_children():
        widget.pack_forget()

    register_label = tk.Label(frame, text="Registrasi Pengguna Baru", font=("perpetua", 12), bg="lightblue")
    register_label.pack(pady=10, anchor="center")

    username_label = tk.Label(frame, text="Username", font=("perpetua", 10), bg="lightblue")
    username_label.pack(pady=5, anchor="center")
    username_entry = tk.Entry(frame, font=("perpetua", 12))
    username_entry.pack(pady=5, anchor="center")

    password_label = tk.Label(frame, text="Password", font=("perpetua", 10), bg="lightblue")
    password_label.pack(pady=5, anchor="center")
    password_entry = tk.Entry(frame, font=("perpetua", 12), show="*")
    password_entry.pack(pady=5, anchor="center")

    email_label = tk.Label(frame, text="Email", font=("perpetua", 10), bg="lightblue")
    email_label.pack(pady=5, anchor="center")
    email_entry = tk.Entry(frame, font=("perpetua", 12))
    email_entry.pack(pady=5, anchor="center")

    def validasi_email(email):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_regex, email) is not None

    def register():
        username = username_entry.get()
        password = password_entry.get()
        email = email_entry.get()

        if username and password and email:
            if username not in users:
                if validasi_email(email):
                    users[username] = {"password": password, "email": email}
                    simpan_data_pengguna()
                    messagebox.showinfo("Registrasi Berhasil", f"Selamat {username}, kamu telah berhasil mendaftar!")
                    tampilkan_menu_login     
                else:
                    messagebox.showerror("Error", "Email tidak valid! Masukkan email yang benar.")
            else:
                messagebox.showerror("Error", "Username sudah terdaftar!")
        else:
            messagebox.showerror("Error", "Username, password, dan email tidak boleh kosong!")

    register_button = tk.Button(frame, text="Registrasi", font=("perpetua", 12), command=register)
    register_button.pack(pady=10, anchor="center")

    tombol_kembali = tk.Button(frame, text="Kembali ke Login", font=("perpetua", 12), command=tampilkan_menu_login)
    tombol_kembali.pack(pady=5, anchor="center")


def tampilkan_menu_utama():
    for widget in frame.winfo_children():
        widget.pack_forget()

    welcome_label = tk.Label(frame, text="Selamat datang di uji coba role Anda", font=("perpetua", 30, "bold"), bg="lightblue")
    welcome_label.pack(pady=10, anchor="center")

    start_button = tk.Button(frame, text="Mulai Tes Kepribadian untuk memilih role", width=40, height=2, font=("perpetua", 10), command=mulai_tes)
    start_button.pack(pady=20, anchor="center")

    exit_button = tk.Button(frame, text="Keluar", width=25, height=2, font=("perpetua", 10), command=keluar_aplikasi)
    exit_button.pack(pady=10, anchor="center")


def keluar_aplikasi():
    root.quit()

# Fungsi untuk memulai tes
def mulai_tes():
    global perhitungan_stack, pertanyaan_queue
    perhitungan_stack = [0, 0, 0, 0, 0]
    pertanyaan_queue = Queue()
    for question in pertanyaan:
        pertanyaan_queue.put(question)

    for widget in frame.winfo_children():
        widget.pack_forget()

    global pertanyaan_label, answer_buttons
    pertanyaan_label = tk.Label(frame, text="", font=("perpetua", 10), wraplength=500, bg="lightblue")
    pertanyaan_label.pack(pady=15, anchor="center")

    answer_buttons = []
    for _ in range(5):
        button = tk.Button(frame, text="", width=80, height=3, font=("perpetua", 10))
        button.pack(pady=20, anchor="center")
        answer_buttons.append(button)

    tampilkan_pertanyaan_selanjutnya()


def tampilkan_pertanyaan_selanjutnya():
    if not pertanyaan_queue.empty():
        question = pertanyaan_queue.get()
        pertanyaan_label.config(text=question["question"])
        for i, answer in enumerate(question["answers"]):
            answer_buttons[i].config(text=answer, command=lambda idx=i: rekam_jawaban(idx))
    else:
        hitung_hasil()


def rekam_jawaban(answer_index):
    current_question = pertanyaan[len(perhitungan_stack) - sum(v == 0 for v in perhitungan_stack) - 1]
    perhitungan_stack[answer_index] += current_question["scores"][answer_index]

    tampilkan_pertanyaan_selanjutnya()


root = tk.Tk()
root.title("Tes Kepribadian Mobile Legends")
root.configure(bg="black")
root.geometry("800x600")

frame = tk.Frame(root, bg="grey")
frame.pack(fill='both', expand=True)


muat_data_pengguna()


tampilkan_menu_login()

root.mainloop()
