import threading
import time
from bootstrap import run_bootstrap
from miner import Miner
from wallet import Wallet, CLIENTS, INITIAL_BALANCE 

def start_bootstrap():
    run_bootstrap()

def start_miners():
    miners = []
    regs = []
    ports = [9101, 9102, 9103]
    for i, port in enumerate(ports):
        name = f"miner{i+1}"
        m = Miner(name, "127.0.0.1", port, difficulty_prefix="0000", trans_per_block=2)
        reg = m.start()
        miners.append(m)
        regs.append(reg)
    return miners, regs

def main():
    print("Starting Bootstrap + Miners...")
    start_bootstrap()
    time.sleep(0.2)
    miners, regs = start_miners()
    print("Creating Task 9 initial transactions (system-funded)...")
    for cname, bal in INITIAL_BALANCE.items():
        tx = {"sender": "system", "receiver": cname, "amount": float(bal), "fee": 0.0, "timestamp": int(time.time()), "txid": f"sys-{cname}-{int(time.time())}"}
        for m in miners:
            with m.seq_lock:
                seq = m.seq
                m.seq += 1
            m.mempool.put((0, seq, tx))

    print("Waiting 2 seconds for miners to mine initial blocks...")
    time.sleep(2)

    print("Simulation started with manual wallets.")
    print("Simulation runs for 60 seconds.\n")

    wallets = {}
    stop_time = time.time() + 10000

    try:
        while time.time() < stop_time:
            print("\n=== Select Wallet ===")
            for idx, cname in enumerate(CLIENTS, 1):
                print(f"{idx}) {cname}")
            print(f"{len(CLIENTS)+1}) Quit Simulation")
            ch = input("Enter choice: ").strip()
            if ch == str(len(CLIENTS)+1):
                break
            try:
                idx = int(ch)-1
                if 0 <= idx < len(CLIENTS):
                    name = CLIENTS[idx]
                    print(f"\nOpening {name} wallet...\n")
                    w = Wallet(name, interactive=True)
                    w.start()
                    while w.running and time.time() < stop_time:
                        time.sleep(0.2)
                    if w.running:
                        w.stop()
                    print(f"\nClosed {name} wallet.\n")
                else:
                    print("Invalid choice.")
            except ValueError:
                print("Invalid input.")
    except KeyboardInterrupt:
        pass
    finally:
        print("Shutting down miners and bootstrap...")
        for m in miners:
            m.stop()
        print("Simulation ended.")

if __name__ == "__main__":
    main()
