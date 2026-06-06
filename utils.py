import hashlib
import json
import time
import socket

def sha256_hex(s: str) -> str:
    return hashlib.sha256(s.encode('utf-8')).hexdigest()

def dict_hash(d) -> str:
    return sha256_hex(json.dumps(d, sort_keys=True))

def merkle_root(transactions):
    """
    Simple merkle root: hash pairs recursively. If odd, duplicate last.
    transactions: list of transaction dicts or strings.
    """
    if not transactions:
        return sha256_hex("")
    leaves = [sha256_hex(json.dumps(t, sort_keys=True)) if not isinstance(t, str) else sha256_hex(t) for t in transactions]

    while len(leaves) > 1:
        if len(leaves) % 2 == 1:
            leaves.append(leaves[-1])
        new_leaves = []
        for i in range(0, len(leaves), 2):
            new_leaves.append(sha256_hex(leaves[i] + leaves[i+1]))
        leaves = new_leaves
    return leaves[0]

def now_ts():
    return int(time.time())

def send_line(sock: socket.socket, line: str):
    if not line.endswith("\n"):
        line = line + "\n"
    sock.sendall(line.encode('utf-8'))

def recv_line(sock: socket.socket):
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
