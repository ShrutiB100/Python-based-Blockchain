import socket
import threading
import time
import json
from queue import PriorityQueue, Empty
from transaction import Transaction
from block import Block
from blockchain import Blockchain
from bootstrap import send_line, recv_line

class Miner:
    def __init__(self, name, host, port, bootstrap_host="127.0.0.1", bootstrap_port=9000,
                 difficulty_prefix="0000", trans_per_block=2):
        self.name = name
        self.host = host
        self.port = port
        self.bootstrap_host = bootstrap_host
        self.bootstrap_port = bootstrap_port

        self.peers = {}
        self.peers_lock = threading.Lock()

        self.wallets = []                     
        self.wallets_lock = threading.Lock()

        self.mempool = PriorityQueue()
        self.seq = 0
        self.seq_lock = threading.Lock()

        self.blockchain = Blockchain(difficulty_prefix=difficulty_prefix)
        self.trans_per_block = trans_per_block

        self.running = True
        self.server_socket = None

    def start(self):
        try:
            reg_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            reg_sock.connect((self.bootstrap_host, self.bootstrap_port))
            send_line(reg_sock, f"REGISTER {self.name} {self.host} {self.port}")
            resp = recv_line(reg_sock)
            reg_sock.close()
        except Exception as e:
            print(f"[{self.name}] Register failed: {e}")

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.host, self.port))
        s.listen()
        self.server_socket = s
        threading.Thread(target=self.accept_loop, args=(s,), daemon=True).start()

        threading.Thread(target=self._mining_loop, daemon=True).start()

        print(f"[{self.name}] miner started on {self.host}:{self.port}")
        return s

    def stop(self):
        self.running = False
        try:
            if self.server_socket:
                self.server_socket.close()
        except: pass

    def accept_loop(self, s):
        while self.running:
            try:
                conn, _ = s.accept()
                threading.Thread(target=self.handle_incoming, args=(conn,), daemon=True).start()
            except Exception:
                break

    def handle_incoming(self, conn):
        try:
            first = recv_line(conn)
            if not first:
                conn.close()
                return

            fl = first.strip()
            if fl.upper() == "LISTEN":
                print(f"[{self.name}] Wallet listener connected, sending blockchain.")
                try:
                    chain_json = json.dumps(self.blockchain.to_json())
                    send_line(conn, "CHAIN " + chain_json)
                except Exception as e:
                    print(f"[{self.name}] Error sending chain: {e}")
                    conn.close()
                    return
                with self.wallets_lock:
                    self.wallets.append(conn)
                while self.running:
                    time.sleep(1)
                with self.wallets_lock:
                    if conn in self.wallets:
                        self.wallets.remove(conn)
                conn.close()
                return

            if fl.startswith("TX "):
                raw = first[3:]
                try:
                    txd = json.loads(raw)
                    priority = -float(txd.get("fee", 0.0))
                    with self.seq_lock:
                        seq = self.seq
                        self.seq += 1
                    self.mempool.put((priority, seq, txd))
                    send_line(conn, "OK")
                except Exception as e:
                    send_line(conn, "ERR")
                finally:
                    conn.close()
                return

            conn.close()
        except Exception:
            try: conn.close()
            except: pass

    def _gather_txs_for_block(self):
        txs = []
        for _ in range(self.trans_per_block):
            try:
                item = self.mempool.get_nowait()
                _, _, txd = item
                txs.append(txd)
            except Empty:
                break
        return txs

    def broadcast_new_block(self, block_dict):
        with self.wallets_lock:
            for w in list(self.wallets):
                try:
                    send_line(w, "NEW_BLOCK " + json.dumps(block_dict))
                except Exception:
                    try:
                        self.wallets.remove(w)
                    except:
                        pass

    def _mining_loop(self):
        while self.running:
            try:
                if self.mempool.empty():
                    time.sleep(0.5)
                    continue

                prev = self.blockchain.last_hash()
                txs = self._gather_txs_for_block()
                if not txs:
                    time.sleep(0.1)
                    continue

                block = Block(self.blockchain.height(), txs, prev)
                block.mine(self.blockchain.difficulty_prefix)
                ok, reason = self.blockchain.add_block(block)
                if ok:
                    bdict = block.to_dict()
                    print(f"[{self.name}] Mined block {block.index} {block.hash[:8]} (txs={len(txs)}). Height: {self.blockchain.height()}")
                    self.broadcast_new_block(bdict)
                else:
                    print(f"[{self.name}] Block rejected: {reason}")
            except Exception as ex:
                time.sleep(0.2)
