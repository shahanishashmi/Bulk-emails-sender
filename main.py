import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox
from email_sender import send_emails
import pandas as pd
import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # when running in .exe
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
class EmailSenderApp:
    def __init__(self, master):
        master.iconbitmap(resource_path("icon.ico"))
        self.master = master
        master.title("Automated Email Sender by Anis Ahmad")
        master.geometry("500x550")
        # Load and display banner/logo image
        img = Image.open(resource_path("banner.jpg"))
        # Replace with your image file name
        img = img.resize((200, 100))  # Resize to fit window
        photo = ImageTk.PhotoImage(img)

        logo_label = tk.Label(master,image=photo)
        logo_label.image = photo  # Keep reference to avoid garbage collection
        logo_label.pack(pady=10)

        tk.Label(master, text="Your Gmail:").pack()
        self.sender_email = tk.Entry(master, width=50)
        self.sender_email.pack()

        tk.Label(master, text="App Password:").pack()
        self.app_password = tk.Entry(master, width=50, show="*")
        self.app_password.pack()

        tk.Label(master, text="Subject:").pack()
        self.subject_entry = tk.Entry(master, width=50)
        self.subject_entry.pack()

        tk.Label(master, text="Message:").pack()
        self.body_text = tk.Text(master, height=10, width=50)
        self.body_text.pack()

        tk.Button(master, text="Upload Recipients CSV", command=self.load_recipients).pack(pady=5)
        tk.Button(master, text="Attach File", command=self.attach_file).pack(pady=5)
        tk.Button(master, text="Send Emails", command=self.send).pack(pady=10)

        self.recipient_list = []
        self.attachment_path = None

    def load_recipients(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            df = pd.read_csv(file_path)
            if 'Email' not in df.columns:
                messagebox.showerror("Error", "CSV must have 'Email' column.")
                return
            self.recipient_list = df['Email'].dropna().tolist()
            messagebox.showinfo("Loaded", f"{len(self.recipient_list)} recipients loaded.")

    def attach_file(self):
        self.attachment_path = filedialog.askopenfilename()
        if self.attachment_path:
            messagebox.showinfo("Attached", "File attached successfully.")

    def send(self):
        sender = self.sender_email.get()
        password = self.app_password.get()
        subject = self.subject_entry.get()
        body = self.body_text.get("1.0", tk.END)

        if not all([sender, password, subject, body.strip(), self.recipient_list]):
            messagebox.showerror("Error", "Please fill all fields and load recipients.")
            return 

        success, failed = send_emails(
            sender, password, self.recipient_list, subject, body, self.attachment_path
        )

        messagebox.showinfo("Result", f"✅ Emails sent: {success}\n❌ Failed: {failed}")

root = tk.Tk()
app = EmailSenderApp(root)
root.mainloop()
