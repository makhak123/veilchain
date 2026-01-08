"""
Transaction types for VeilChain
"""
from dataclasses import dataclass
from typing import Optional
import secrets
import json
from .crypto import sha256, sign_data, create_commitment, generate_nullifier

@dataclass
class TransparentTransaction:
    """Public transaction (like Bitcoin)"""
    sender: str
    recipient: str
    amount: float
    timestamp: float
    signature: str = ""
    
    def to_dict(self) -> dict:
        return {
            'type': 'transparent',
            'sender': self.sender,
            'recipient': self.recipient,
            'amount': self.amount,
            'timestamp': self.timestamp,
            'signature': self.signature
        }
    
    def calculate_hash(self) -> str:
        tx_string = f"{self.sender}{self.recipient}{self.amount}{self.timestamp}"
        return sha256(tx_string)
    
    def sign(self, private_key: str):
        """Sign the transaction"""
        tx_hash = self.calculate_hash()
        self.signature = sign_data(private_key, tx_hash)

@dataclass
class ShieldedTransaction:
    """Private transaction with hidden amounts and addresses"""
    # Public fields
    commitment: str  # Hides the transaction value
    nullifier: str   # Prevents double-spending
    proof: str       # Zero-knowledge proof
    timestamp: float
    
    # Private fields (not broadcasted)
    _sender: Optional[str] = None
    _recipient: Optional[str] = None
    _amount: Optional[float] = None
    _blinding_factor: Optional[str] = None
    
    def to_dict(self) -> dict:
        return {
            'type': 'shielded',
            'commitment': self.commitment,
            'nullifier': self.nullifier,
            'proof': self.proof,
            'timestamp': self.timestamp
        }
    
    def calculate_hash(self) -> str:
        tx_string = f"{self.commitment}{self.nullifier}{self.proof}{self.timestamp}"
        return sha256(tx_string)
    
    @staticmethod
    def create(sender_private_key: str, recipient: str, amount: float, timestamp: float):
        """Create a shielded transaction"""
        blinding_factor = secrets.token_hex(32)
        commitment = create_commitment(int(amount * 1000000), blinding_factor)
        nullifier = generate_nullifier(sender_private_key, commitment)
        
        # Generate simplified zk-proof
        proof_data = f"{commitment}{nullifier}{amount}{timestamp}{blinding_factor}"
        proof = sha256(proof_data)
        
        return ShieldedTransaction(
            commitment=commitment,
            nullifier=nullifier,
            proof=proof,
            timestamp=timestamp,
            _sender=sender_private_key,
            _recipient=recipient,
            _amount=amount,
            _blinding_factor=blinding_factor
        )
    
    def verify_proof(self) -> bool:
        """Verify the zero-knowledge proof (simplified)"""
        # In a real implementation, this would verify the zk-SNARK
        # Here we just check the proof format is valid
        return len(self.proof) == 64 and len(self.commitment) == 64
