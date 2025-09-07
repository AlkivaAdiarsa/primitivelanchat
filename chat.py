import socket
import threading
import tkinter as tk
from tkinter import simpledialog, scrolledtext, messagebox

PORT = 6000
clients = []   # for server mode
running = True

# ---------------- SERVER ----------------
def handle_client(conn, addr, chat_box):
    global clients
    clients.append(conn)
    chat_box.insert(tk.END, f"[NEW] {addr} connected\n")
    chat_box.yview(tk.END)

    try:
        while running:
            msg = conn.recv(1024)
            if not msg:
                break
            broadcast = f"{addr[0]}: {msg.decode()}"
            chat_box.insert(tk.END, broadcast + "\n")
            chat_box.yview(tk.END)

            for c in clients:
                if c != conn:
                    c.sendall(broadcast.encode())
    except:
        pass
    finally:
        clients.remove(conn)
        conn.close()
        chat_box.insert(tk.END, f"[DISCONNECT] {addr}\n")

def run_server(chat_box):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", PORT))
    server.listen(5)
    chat_box.insert(tk.END, f"🌍 Server listening on port {PORT}...\n")
    while running:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr, chat_box), daemon=True).start()

# ---------------- CLIENT ----------------
def run_client(server_ip, chat_box, entry_field):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server_ip, PORT))
    chat_box.insert(tk.END, f"✅ Connected to {server_ip}:{PORT}\n")

    def listen():
        while running:
            try:
                msg = sock.recv(1024).decode()
                if msg:
                    chat_box.insert(tk.END, msg + "\n")
                    chat_box.yview(tk.END)
            except:
                break
    threading.Thread(target=listen, daemon=True).start()

    def send_msg(event=None):
        text = entry_field.get()
        if text:
            sock.sendall(text.encode())
            entry_field.delete(0, tk.END)

    return send_msg

# ---------------- GUI APP ----------------
def start_app():
    root = tk.Tk()
    root.title("LAN/Internet Chat")

    chat_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20, state="normal")
    chat_box.pack(padx=10, pady=10)

    entry_field = tk.Entry(root, width=40)
    entry_field.pack(side=tk.LEFT, padx=10, pady=5)

    send_btn = tk.Button(root, text="Send")
    send_btn.pack(side=tk.LEFT, padx=5)

    mode = simpledialog.askstring("Mode", "Type 'server' to host or 'client <IP>' to connect:")

    if mode and mode.lower().startswith("server"):
        threading.Thread(target=run_server, args=(chat_box,), daemon=True).start()
        def send_msg(event=None):
            msg = entry_field.get()
            if msg:
                for c in clients:
                    try:
                        c.sendall(f"[SERVER]: {msg}".encode())
                    except:
                        pass
                chat_box.insert(tk.END, f"[SERVER]: {msg}\n")
                chat_box.yview(tk.END)
                entry_field.delete(0, tk.END)

    elif mode and mode.lower().startswith("client"):
        parts = mode.split()
        if len(parts) < 2:
            messagebox.showerror("Error", "You must provide server IP: client <IP>")
            root.destroy()
            return
        server_ip = parts[1]
        send_msg = run_client(server_ip, chat_box, entry_field)
    else:
        messagebox.showerror("Error", "Invalid mode. Restart and type 'server' or 'client <IP>'.")
        root.destroy()
        return

    entry_field.bind("<Return>", lambda e: send_msg())
    send_btn.config(command=send_msg)

    root.mainloop()

if __name__ == "__main__":
    start_app()
