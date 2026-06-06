Project Description

The project demonstrates core blockchain concepts through a simplified Python-based blockchain system which shows decentralized transaction management, proof-of-work, and block validation processes. The system enables multiple clients with wallets to create transactions and send them while miners perform black validation and mining operations. A bootstrap node handles network connection management. The project delivers practical learning about blockchain systems through Python thread-based concurrent programming exercises.

System Components
1. Clients (Wallets)
- 5 clients (client1, client2, client3, client4, client5)
- Each wallet stores received transactions and can send funds to other wallets.
- Wallets connect to a miner to sync the blockchain and receive updates.
- Wallets simulate delays using sleep of 5 seconds to represent network or user wait times.
- Menu-driven interface:
    1. Send Transaction
    2. Show Balance
    3. Show Sent Transactions
    4. Show Received Transactions
    5. Quit Wallet


2. Miners
- 3 Miners (miner1, miner2, miner3) running in parallel threads.
- Register with the bootstrap node and maintain peer connections.
- Maintain a mempool of pending transactions.
- Produce blocks with proof-of-work, each containing multiple transactions.
- Broadcast mined blocks to all connected peers.

3. Bootstrap Node
- Manages network registration for miners.
- Provides miner connectivity details to wallets.

4. Blockchain
- Hash-linked blocks stored in memory.
- Each block includes: transactions, timestamp, previous hash, nonce, and proof-ofwork.
- Transaction processing uses a simplified Merkle tree.
- Mining difficulty requires hash to start with “0000”.


Running the Project
1. Ensure Python 3.10+ is installed.
2. Required standard libraries: hashlib, time, threading, random, bootstrap, socket, json.
3. Start the simulation: python main.py
4. Interact with wallets via menu.
5. When sending a transaction, choose receiver, amount and fee.

Concurrency Model
The project uses Python’s threading module to simulate a decentralized blockchain network in
which miners and wallets operate concurrently. The system runs each major component
bootstrap node, miners, and wallets in separate threads which operate independently. The
mining process runs through simultaneous threads that perform proof-of-work while receiving
transactions from wallets, updating their peer list with the bootstrap node, and broadcasting
mined blocks to other miners. Miner threads operate independently from the wallet interface as
background processes. Each wallet runs in its own thread, controlling user input for balances,
menu selections, and building transactions sent to the chosen miner. Wallet threads track their
own transaction history while staying connected to a miner for instant updates. The bootstrap
node thread receives miner connections and answers wallet queries while keeping the system
operational.

Overall concurrency enables:
- Independent proof-of-work mining by multiple users.
- Parallel wallet actions across multiple clients.
- Continuous background coordination between miners and the bootstrap nodes.

Known Limitations
- The wallet input system operates in a blocking mode which restricts user interaction to one
wallet menu at any given time.
- Blockchain operates as an in-memory system which lacks any form of permanent storage
capabilities.
- Miner selection and transaction routing are simplified and random.
- The network simulation operates on a local setup, which does not include actual socket
operations or latency simulation.

Future Improvements
- Blockchain storage requires permanent solution through database systems or file storage
mechanisms.
- The system needs to establish a network simulation which duplicates actual sockets and
network latency conditions.
- The system needs to develop more advanced methods for choosing miners, and directing
transactions.
- The system provides users with a GUI option to visualize their wallets, and mining
operations, together with the blockchain data.
