from block import Block
import threading

class Blockchain:
    def __init__(self, difficulty_prefix="0000"):
        self.chain = []
        self.difficulty_prefix = difficulty_prefix
        self.lock = threading.Lock()
        self.create_genesis()

    def create_genesis(self):
        genesis = Block(0, [], "0"*64)
        genesis.hash = genesis.compute_hash()
        self.chain.append(genesis)

    def last_block(self):
        return self.chain[-1]

    def last_hash(self):
        return self.last_block().hash

    def add_block(self, block: Block):
        with self.lock:
            if block.previous_hash != self.last_block().hash:
                return False, "bad previous hash"
            if not block.hash:
                return False, "block not mined"
            if not block.hash.startswith(self.difficulty_prefix):
                return False, "invalid difficulty"
            self.chain.append(block)
            return True, "ok"

    def height(self):
        with self.lock:
            return len(self.chain)

    def to_json(self):
        with self.lock:
            return [b.to_dict() for b in self.chain]
