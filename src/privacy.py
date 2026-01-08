"""
Privacy layer for VeilChain - Zero-knowledge proof simulation
"""
from typing import List, Set
from .transaction import ShieldedTransaction

class PrivacyLayer:
    """Manages privacy features and zero-knowledge proofs"""
    
    def __init__(self):
        self.nullifier_set: Set[str] = set()
        self.commitment_set: Set[str] = set()
    
    def verify_shielded_transaction(self, transaction: ShieldedTransaction) -> bool:
        """Verify a shielded transaction"""
        # Check if nullifier has been used (prevent double-spending)
        if transaction.nullifier in self.nullifier_set:
            print(f"Transaction rejected: Nullifier already used (double-spend attempt)")
            return False
        
        # Verify the zero-knowledge proof
        if not transaction.verify_proof():
            print(f"Transaction rejected: Invalid zero-knowledge proof")
            return False
        
        # Add nullifier to the set
        self.nullifier_set.add(transaction.nullifier)
        self.commitment_set.add(transaction.commitment)
        
        return True
    
    def get_anonymity_set_size(self) -> int:
        """Get the size of the anonymity set"""
        return len(self.commitment_set)
