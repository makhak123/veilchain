"""
Block structure for VeilChain
"""
from dataclasses import dataclass, field
from typing import List, Union, Optional
import time
from .transaction import TransparentTransaction, ShieldedTransaction
from .crypto import sha256

@dataclass
class Block:
    """A block in the blockchain"""
    index: int
    timestamp: float
    transactions: List[Union[TransparentTransaction, ShieldedTransaction]]
    previous_hash: str
    nonce: int = 0
    hash: str = ""
    difficulty: int = 2
    merkle_root: str = ""
    version: int = 1
    
    def calculate_hash(self) -> str:
        """Calculate the block hash"""
        transactions_string = ''.join([tx.calculate_hash() for tx in self.transactions])
        block_string = f"{self.index}{self.timestamp}{transactions_string}{self.previous_hash}{self.nonce}{self.difficulty}{self.version}"
        return sha256(block_string)
    
    def calculate_merkle_root(self) -> str:
        """Calculate Merkle root of transactions"""
        if not self.transactions:
            return sha256("empty")
        
        from .merkle import MerkleTree
        tx_hashes = [tx.calculate_hash() for tx in self.transactions]
        merkle_tree = MerkleTree(tx_hashes)
        return merkle_tree.get_root_hash()
    
    def mine_block(self, difficulty: int):
        """Mine the block with proof of work"""
        self.difficulty = difficulty
        self.merkle_root = self.calculate_merkle_root()
        
        target = '0' * difficulty
        start_time = time.time()
        
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
            
            # Print progress every 100000 hashes
            if self.nonce % 100000 == 0:
                elapsed = time.time() - start_time
                hashrate = self.nonce / elapsed if elapsed > 0 else 0
                print(f"Mining... Nonce: {self.nonce}, Hashrate: {hashrate:.2f} H/s")
        
        elapsed = time.time() - start_time
        print(f"Block mined: {self.hash} (Time: {elapsed:.2f}s, Nonce: {self.nonce})")
    
    def verify_merkle_root(self) -> bool:
        """Verify the Merkle root is correct"""
        calculated_root = self.calculate_merkle_root()
        return calculated_root == self.merkle_root
    
    def to_dict(self) -> dict:
        return {
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': [tx.to_dict() for tx in self.transactions],
            'previous_hash': self.previous_hash,
            'nonce': self.nonce,
            'hash': self.hash,
            'difficulty': self.difficulty,
            'merkle_root': self.merkle_root,
            'version': self.version
        }
