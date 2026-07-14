import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess

# ---------------- RUN YOLO FILES ----------------
def open_yolo_image_voice():
    subprocess.Popen(["python", "yolo_image_voice.py"])

def open_yolo_webcam():
    subprocess.Popen(["python", "yolo_webcam.py"])

# ---------------- SHOW LOGIN PAGE ----------------
def show_login():
    dashboard_frame.pack_forget()
    login_frame.pack(expand=True)

# ---------------- LOGIN FUNCTION ----------------
def login():
    username = entry_username.get()
    password = entry_password.get()

    if username == "admin" and password == "admin":
        login_frame.pack_forget()
        dashboard_frame.pack(expand=True)
    else:
        messagebox.showerror("Login Failed", "Invalid Username or Password")

# ---------------- MAIN WINDOW ----------------
root = tk.Tk()
root.title("Computer Vision Model")
root.attributes('-fullscreen', True)

# Background Image
bg_image = Image.open("background.jpeg")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
bg_image = bg_image.resize((screen_width, screen_height))
bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# ================= TITLE =================
title_label = tk.Label(root,
                       text="Computer Vision Model For Obstacles Detection and Audio Guidence",
                       font=("Arial", 28, "bold"),
                       bg="#000000",
                       fg="white",
                       pady=20)
title_label.pack(fill="x")

# ================= LOGIN FRAME =================
login_frame = tk.Frame(root, bg="skyblue", bd=5)

tk.Label(login_frame, text="LOGIN", font=("Arial", 22, "bold"), bg="white").pack(pady=20)

tk.Label(login_frame, text="Username", font=("Arial", 14), bg="white").pack()
entry_username = tk.Entry(login_frame, font=("Arial", 14))
entry_username.pack(pady=10)

tk.Label(login_frame, text="Password", font=("Arial", 14), bg="white").pack()
entry_password = tk.Entry(login_frame, show="*", font=("Arial", 14))
entry_password.pack(pady=10)

tk.Button(login_frame, text="Login",
          font=("Arial", 14, "bold"),
          bg="#4CAF50", fg="white",
          width=15,
          command=login).pack(pady=20)

login_frame.pack(expand=True)

# ================= DASHBOARD FRAME =================
dashboard_frame = tk.Frame(root, bg="skyblue", bd=5)

tk.Label(dashboard_frame,
         text="Dashboard",
         font=("Arial", 22, "bold"),
         bg="white").pack(pady=30)

tk.Button(dashboard_frame,
          text="Run Image Voice",
          font=("Arial", 16, "bold"),
          bg="#4CAF50", fg="white",
          width=25, height=2,
          command=open_yolo_image_voice).pack(pady=20)

tk.Button(dashboard_frame,
          text="Run Webcam",
          font=("Arial", 16, "bold"),
          bg="#2196F3", fg="white",
          width=25, height=2,
          command=open_yolo_webcam).pack(pady=20)

# -------- Back to Home Button --------
tk.Button(dashboard_frame,
          text="Back to Home",
          font=("Arial", 14, "bold"),
          bg="#f44336", fg="white",
          width=15,
          command=show_login).pack(pady=40)

# Exit fullscreen with ESC
root.bind("<Escape>", lambda e: root.destroy())

root.mainloop()
