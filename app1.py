import tkinter as tk
from tkinter import scrolledtext
import serial
import threading

class ChatApp:
    def __init__(self, master, port):
        self.master = master
        self.master.title("ESP32 Chat1")

        self.chat_log = scrolledtext.ScrolledText(master, state='disabled', width=50, height=20)
        self.chat_log.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        self.message_entry = tk.Entry(master, width=40)
        self.message_entry.grid(row=1, column=0, padx=10, pady=10)
        self.message_entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(master, text="Send", command=self.send_message)
        self.send_button.grid(row=1, column=1, padx=10, pady=10)

        self.serial_port = serial.Serial(port, 115200, timeout=1)
        self.thread = threading.Thread(target=self.receive_message)
        self.thread.daemon = True
        self.thread.start()

    def send_message(self, event=None):
        message = self.message_entry.get()
        if message:
            self.serial_port.write((message + '\n').encode())
            self.chat_log.config(state='normal')
            self.chat_log.insert(tk.END, f"Me: {message}\n")
            self.chat_log.config(state='disabled')
            self.chat_log.yview(tk.END)
            self.message_entry.delete(0, tk.END)

    def receive_message(self):
        while True:
            if self.serial_port.in_waiting > 0:
                message = self.serial_port.readline().decode().strip()
                self.chat_log.config(state='normal')
                self.chat_log.insert(tk.END, f"Friend: {message}\n")
                self.chat_log.config(state='disabled')
                self.chat_log.yview(tk.END)

def main():
    root = tk.Tk()
    app = ChatApp(root, 'COM7')
    root.mainloop()

if __name__ == '__main__':
    main()
