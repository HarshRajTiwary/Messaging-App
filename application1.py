import tkinter as tk
from tkinter import scrolledtext, ttk
import serial
import serial.tools.list_ports
import threading

class ChatApp:
    def __init__(self, master):
        self.master = master
        self.master.title("ESP32 Chat Application")

        # Chat log
        self.chat_log = scrolledtext.ScrolledText(master, state='disabled', width=50, height=20)
        self.chat_log.grid(row=0, column=0, padx=10, pady=10, columnspan=3)

        # Message entry and send button
        self.message_entry = tk.Entry(master, width=40)
        self.message_entry.grid(row=1, column=0, padx=10, pady=10)
        self.message_entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(master, text="Send", command=self.send_message)
        self.send_button.grid(row=1, column=1, padx=10, pady=10)

        # Port selection
        self.port_label = tk.Label(master, text="Select Port:")
        self.port_label.grid(row=2, column=0, padx=10, pady=10)

        self.port_combobox = ttk.Combobox(master, values=self.get_available_ports(), state='readonly')
        self.port_combobox.grid(row=2, column=1, padx=10, pady=10)
        self.port_combobox.bind("<<ComboboxSelected>>", self.connect_to_port)

        # Connection status
        self.status_label = tk.Label(master, text="Not Connected", fg="red")
        self.status_label.grid(row=2, column=2, padx=10, pady=10)

        # Initialize variables
        self.serial_port = None
        self.thread = None
        self.running = False

    def get_available_ports(self):
        """Fetch a list of available COM ports."""
        ports = serial.tools.list_ports.comports()
        return [port.device for port in ports]

    def connect_to_port(self, event=None):
        """Connect to the selected COM port."""
        selected_port = self.port_combobox.get()
        if self.serial_port:
            self.serial_port.close()

        try:
            self.serial_port = serial.Serial(selected_port, 115200, timeout=1)
            self.status_label.config(text="Connected", fg="green")
            self.running = True

            # Start receiving messages
            if not self.thread or not self.thread.is_alive():
                self.thread = threading.Thread(target=self.receive_message)
                self.thread.daemon = True
                self.thread.start()
        except serial.SerialException:
            self.status_label.config(text="Connection Failed", fg="red")

    def send_message(self, event=None):
        """Send a message via the serial port."""
        if self.serial_port and self.serial_port.is_open:
            message = self.message_entry.get()
            if message:
                self.serial_port.write((message + '\n').encode())
                self.chat_log.config(state='normal')
                self.chat_log.insert(tk.END, f"Me: {message}\n")
                self.chat_log.config(state='disabled')
                self.chat_log.yview(tk.END)
                self.message_entry.delete(0, tk.END)

    def receive_message(self):
        """Continuously read messages from the serial port."""
        while self.running:
            if self.serial_port and self.serial_port.in_waiting > 0:
                try:
                    message = self.serial_port.readline().decode().strip()
                    self.chat_log.config(state='normal')
                    self.chat_log.insert(tk.END, f"Friend: {message}\n")
                    self.chat_log.config(state='disabled')
                    self.chat_log.yview(tk.END)
                except Exception as e:
                    print(f"Error reading message: {e}")
                    break

    def close_app(self):
        """Handle app closure and cleanup."""
        self.running = False
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
        self.master.destroy()

def main():
    root = tk.Tk()
    app = ChatApp(root)
    root.protocol("WM_DELETE_WINDOW", app.close_app)  # Graceful app closure
    root.mainloop()

if __name__ == '__main__':
    main()
