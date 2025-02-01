import hashlib
import time
import json

class Block:
    def __init__(self, index, transactions, previous_hash, difficulty=2):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.mine_block(difficulty)
    
    def compute_hash(self):
        block_data = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True).encode()
        return hashlib.sha256(block_data).hexdigest()
    
    def mine_block(self, difficulty):
        prefix = '0' * difficulty
        while True:
            self.hash = self.compute_hash()
            if self.hash.startswith(prefix):
                break
            self.nonce += 1
        return self.hash

class Blockchain:
    def __init__(self, difficulty=2):
        self.chain = []
        self.difficulty = difficulty
        self.create_genesis_block()
    
    def create_genesis_block(self):
        genesis_block = Block(0, "Genesis Block", "0", self.difficulty)
        self.chain.append(genesis_block)
    
    def add_block(self, transactions):
        previous_block = self.chain[-1]
        new_block = Block(len(self.chain), transactions, previous_block.hash, self.difficulty)
        self.chain.append(new_block)
    
    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if current_block.hash != current_block.compute_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True
    
    def print_chain(self):
        for block in self.chain:
            print(f"Index: {block.index}\nTimestamp: {block.timestamp}\nTransactions: {block.transactions}\nPrev Hash: {block.previous_hash}\nHash: {block.hash}\nNonce: {block.nonce}\n{'-'*40}")

# Example Usage
if __name__ == "__main__":
    blockchain = Blockchain(difficulty=3)
    blockchain.add_block(["Alice pays Bob 5 BTC", "Charlie pays Dave 2 BTC"])
    blockchain.add_block(["Eve pays Frank 3 BTC"])
    blockchain.print_chain()
    
    print("Blockchain valid?", blockchain.is_chain_valid())
    
    # Tampering with the chain
    blockchain.chain[1].transactions = ["Alice pays Bob 100 BTC"]
    print("Blockchain valid after tampering?", blockchain.is_chain_valid())
