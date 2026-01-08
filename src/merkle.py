"""
Merkle Tree implementation for efficient transaction verification
"""
from typing import List, Optional
from .crypto import sha256

class MerkleNode:
    """Node in a Merkle tree"""
    
    def __init__(self, left=None, right=None, data: str = ""):
        self.left = left
        self.right = right
        self.data = data
        self.hash = self.calculate_hash()
    
    def calculate_hash(self) -> str:
        """Calculate hash of the node"""
        if self.left and self.right:
            return sha256(self.left.hash + self.right.hash)
        else:
            return sha256(self.data)

class MerkleTree:
    """Merkle Tree for transaction hashing"""
    
    def __init__(self, transactions: List[str]):
        self.transactions = transactions
        self.root = self.build_tree(transactions)
    
    def build_tree(self, transactions: List[str]) -> Optional[MerkleNode]:
        """Build Merkle tree from transactions"""
        if not transactions:
            return None
        
        nodes = [MerkleNode(data=tx) for tx in transactions]
        
        while len(nodes) > 1:
            new_level = []
            
            for i in range(0, len(nodes), 2):
                left = nodes[i]
                right = nodes[i + 1] if i + 1 < len(nodes) else nodes[i]
                new_level.append(MerkleNode(left=left, right=right))
            
            nodes = new_level
        
        return nodes[0] if nodes else None
    
    def get_root_hash(self) -> str:
        """Get the root hash of the Merkle tree"""
        return self.root.hash if self.root else ""
    
    def get_proof(self, transaction: str) -> List[dict]:
        """Get Merkle proof for a transaction"""
        if transaction not in self.transactions:
            return []
        
        index = self.transactions.index(transaction)
        proof = []
        
        nodes = [MerkleNode(data=tx) for tx in self.transactions]
        
        while len(nodes) > 1:
            new_level = []
            
            for i in range(0, len(nodes), 2):
                left = nodes[i]
                right = nodes[i + 1] if i + 1 < len(nodes) else nodes[i]
                
                if i == index or i + 1 == index:
                    sibling = right if i == index else left
                    proof.append({
                        'hash': sibling.hash,
                        'position': 'right' if i == index else 'left'
                    })
                    index = i // 2
                
                new_level.append(MerkleNode(left=left, right=right))
            
            nodes = new_level
        
        return proof
    
    @staticmethod
    def verify_proof(transaction_hash: str, proof: List[dict], root_hash: str) -> bool:
        """Verify a Merkle proof"""
        current_hash = transaction_hash
        
        for proof_element in proof:
            if proof_element['position'] == 'right':
                current_hash = sha256(current_hash + proof_element['hash'])
            else:
                current_hash = sha256(proof_element['hash'] + current_hash)
        
        return current_hash == root_hash
