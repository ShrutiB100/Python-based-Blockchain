from dataclasses import dataclass
from utils import dict_hash, now_ts

@dataclass
class Transaction:
    sender: str
    receiver: str
    amount: float
    fee: float = 0.0
    timestamp: int = None
    txid: str = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = now_ts()
        if self.txid is None:
            self.txid = self.compute_txid()

    def to_dict(self):
        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": float(self.amount),
            "fee": float(self.fee),
            "timestamp": int(self.timestamp),
            "txid": self.txid
        }

    def to_json_dict(self):
        return self.to_dict()

    def compute_txid(self):
        base = {
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": float(self.amount),
            "fee": float(self.fee),
            "timestamp": int(self.timestamp)
        }
        return dict_hash(base)

    @classmethod
    def from_dict(cls, d):
        return cls(
            sender=d.get("sender"),
            receiver=d.get("receiver"),
            amount=float(d.get("amount")),
            fee=float(d.get("fee", 0.0)),
            timestamp=int(d.get("timestamp")),
            txid=d.get("txid")
        )

    def __repr__(self):
        return f"TX({self.sender}->{self.receiver} {self.amount} fee={self.fee})"
