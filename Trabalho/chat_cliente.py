import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

HOST = "192.168.137.23"
PORT = 5000

class ChatClient:
    def __init__(self, master):
        self.master = master
        master.title("Chat via Sockets")

        # Caixa de mensagens (área grande)
        self.chat_area = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=50, height=20, state='disabled')
        self.chat_area.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        # Campo de entrada
        self.entry = tk.Entry(master, width=40)
        self.entry.grid(row=1, column=0, padx=5, pady=5)
        self.entry.bind("<Return>", self.send_message)

        # Botão enviar
        self.send_button = tk.Button(master, text="Enviar", command=self.send_message)
        self.send_button.grid(row=1, column=1, padx=5, pady=5)

        # Conectar ao servidor
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((HOST, PORT))

        # Thread para receber mensagens
        threading.Thread(target=self.receive_messages, daemon=True).start()

    def receive_messages(self):
        while True:
            try:
                msg = self.sock.recv(1024).decode()
                self.add_message(msg)
            except:
                break

    def send_message(self, event=None):
        msg = self.entry.get()
        if msg.strip() == "":
            return

        self.sock.send(msg.encode())
        self.add_message(f"Você: {msg}")
        self.entry.delete(0, tk.END)

    def add_message(self, msg):
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, msg + "\n")
        self.chat_area.yview(tk.END)
        self.chat_area.config(state='disabled')

root = tk.Tk()
client = ChatClient(root)
root.mainloop()
