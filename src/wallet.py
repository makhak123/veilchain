"""
Wallet management for VeilChain
"""
from dataclasses import dataclass
from typing import Tuple
from .crypto import generate_keypair, generate_address

@dataclass
class Wallet:
    """VeilChain wallet with both transparent and shielded addresses"""
    private_key: str
    public_key: str
    transparent_address: str
    shielded_address: str
    balance: float = 0.0
    
    @staticmethod
    def create() -> 'Wallet':
        """Create a new wallet"""
        private_key, public_key = generate_keypair()
        transparent_address = generate_address(public_key, 't')
        shielded_address = generate_address(public_key, 'z')
        
        return Wallet(
            private_key=private_key,
            public_key=public_key,
            transparent_address=transparent_address,
            shielded_address=shielded_address
        )
    
    def to_dict(self) -> dict:
        return {
            'private_key': self.private_key,
            'public_key': self.public_key,
            'transparent_address': self.transparent_address,
            'shielded_address': self.shielded_address,
            'balance': self.balance
        }
    
    def __repr__(self) -> str:
        return f"""
VeilChain Wallet
================
Transparent Address: {self.transparent_address}
Shielded Address:    {self.shielded_address}
Balance:            {self.balance} VEIL
        """
