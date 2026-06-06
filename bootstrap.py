import socket
import threading

REGISTRY = {} 
LOCK = threading.Lock()

def run_bootstrap(host="127.0.0.1", port=9000):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen()
    threading.Thread(target=accept_loop, args=(s,), daemon=True).start()
    print("[BOOT] Listening on 127.0.0.1:9000")

def accept_loop(s):
    while True:
        conn, _ = s.accept()
        threading.Thread(target=handle_conn, args=(conn,), daemon=True).start()

def handle_conn(conn):
    try:
        data = recv_line(conn)
        if not data:
            conn.close()
            return
        parts = data.strip().split()
        if parts[0].upper() == "REGISTER" and len(parts) == 4:
            name, host, port = parts[1], parts[2], int(parts[3])
            with LOCK:
                REGISTRY[name] = (host, port)
            send_line(conn, "OK")
        elif parts[0].upper() == "LIST":
            with LOCK:
                for name, (h, p) in REGISTRY.items():
                    send_line(conn, f"{name} {h} {p}")
            send_line(conn, "END")
        else:
            send_line(conn, "ERR")
    except Exception:
        pass
    finally:
        try: conn.close()
        except: pass

import socket as _socket
def send_line(sock: _socket.socket, line: str):
    if not line.endswith("\n"):
        line = line + "\n"
    sock.sendall(line.encode('utf-8'))

def recv_line(sock: _socket.socket):
    data = bytearray()
    while True:
        ch = sock.recv(1)
        if not ch:
            if not data:
                return None
            break
        if ch == b'\n':
            break
        data.extend(ch)
    try:
        return data.decode('utf-8')
    except:
        return None
