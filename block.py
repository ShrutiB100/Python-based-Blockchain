import time
from utils import sha256_hex, merkle_root

class Block:
    def __init__(self, index, transactions, previous_hash, timestamp=None, nonce=0):
        self.index = index
        self.transactions = transactions  # list of transaction dicts
        self.previous_hash = previous_hash
        self.timestamp = timestamp or int(time.time())
        self.nonce = nonce
        self.merkle_root = merkle_root([t if isinstance(t, str) else t.get('txid', str(t)) for t in self.transactions])
        self.hash = None

    def header_string(self):
        return f"{self.index}{self.previous_hash}{self.timestamp}{self.nonce}{self.merkle_root}"

    def compute_hash(self):
        return sha256_hex(self.header_string())

    def mine(self, difficulty_prefix="0000", max_tries=10**7):
        prefix = difficulty_prefix
        tries = 0
        while tries < max_tries:
            h = self.compute_hash()
            if h.startswith(prefix):
                self.hash = h
                return h
            self.nonce += 1
            tries += 1
        raise RuntimeError("Failed to mine block within max_tries")

    def to_dict(self):
        return {
            "index": self.index,
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "nonce": self.nonce,
            "merkle_root": self.merkle_root,
            "hash": self.hash,
            "transactions": self.transactions
        }

    def __repr__(self):
        return f"Block(idx={self.index} hash={self.hash[:8] if self.hash else None} txs={len(self.transactions)})"
