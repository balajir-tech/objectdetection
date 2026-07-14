import tkinter as tk
from tkinter import messagebox
import subprocess

# -------- Login Function --------
def login():
    username = entry_username.get()
    password = entry_password.get()

    if username == "admin" and password == "admin":
        messagebox.showinfo("Login Success", "Welcome!")
        login_window.destroy()
        open_main_window()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

# -------- Open YOLO Image Voice --------
def open_yolo_image_voice():
    subprocess.Popen(["python", "yolo_image_voice.py"])

# -------- Open YOLO Webcam --------
def open_yolo_webcam():
    subprocess.Popen(["python", "yolo_webcam.py"])

# -------- Main Window --------
def open_main_window():
    main_window = tk.Tk()
    main_window.title("YOLO Dashboard")
    main_window.geometry("300x200")

    btn1 = tk.Button(main_window, text="Run YOLO Image Voice", command=open_yolo_image_voice)
    btn1.pack(pady=20)

    btn2 = tk.Button(main_window, text="Run YOLO Webcam", command=open_yolo_webcam)
    btn2.pack(pady=20)

    main_window.mainloop()

# -------- Login Window --------
login_window = tk.Tk()
login_window.title("Login")
login_window.geometry("300x200")

tk.Label(login_window, text="Username").pack()
entry_username = tk.Entry(login_window)
entry_username.pack()

tk.Label(login_window, text="Password").pack()
entry_password = tk.Entry(login_window, show="*")
entry_password.pack()

tk.Button(login_window, text="Login", command=login).pack(pady=10)

login_window.mainloop()
