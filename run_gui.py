import tkinter as tk, threading
from tkinter import filedialog, messagebox
import subprocess, os

def choose_photo():
    path = filedialog.askopenfilename(filetypes=[("Images","*.jpg *.png")])
    entry_input.delete(0, tk.END)
    entry_input.insert(0, path)

def start_process():
    inp = entry_input.get().strip()
    if not inp:
        messagebox.showerror("Error", "Choose a photo first!")
        return
    threading.Thread(target=lambda: subprocess.run([
        "python","run_cli.py",
        "--input", inp,
        "--output_face","output/restored.jpg",
        "--output_video","output/talk_hi.mp4"
    ])).start()
    messagebox.showinfo("Started","Processing... Check output folder.")

root = tk.Tk()
root.title("Old Photo Talker")
tk.Label(root, text="Old Photo:").grid(row=0, column=0)
entry_input = tk.Entry(root, width=50)
entry_input.grid(row=0, column=1)
tk.Button(root, text="Browse", command=choose_photo).grid(row=0, column=2)
tk.Button(root, text="Run", command=start_process).grid(row=1, column=1)
root.mainloop()
