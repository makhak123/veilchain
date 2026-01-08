"""
UTXO (Unspent Transaction Output) model for VeilChain
Similar to Bitcoin's UTXO model
"""
from dataclasses import dataclass
from typing import List, Dict, Set, Optional
import time
from .crypto import sha256, sign_data, verify_signature

@dataclass
class UTXO:
    """Unspent Transaction Output"""
    tx_id: str
    output_index: int
    address: str
    amount: float
    is_shielded: bool
    
    def get_id(self) -> str:
        """Get unique identifier for this UTXO"""
        return f"{self.tx_id}:{self.output_index}"
    
    def to_dict(self) -> dict:
        return {
            'tx_id': self.tx_id,
            'output_index': self.output_index,
            'address': self.address,
            'amount': self.amount,
            'is_shielded': self.is_shielded
        }

@dataclass
class TransactionInput:
    """Reference to a UTXO being spent"""
    utxo_id: str
    signature: str = ""
    
    def to_dict(self) -> dict:
        return {
            'utxo_id': self.utxo_id,
            'signature': self.signature
        }

@dataclass
class TransactionOutput:
    """New UTXO being created"""
    address: str
    amount: float
    is_shielded: bool = False
    
    def to_dict(self) -> dict:
        return {
            'address': self.address,
            'amount': self.amount,
            'is_shielded': self.is_shielded
        }

class UTXOPool:
    """Manages all unspent transaction outputs"""
    
    def __init__(self):
        self.utxos: Dict[str, UTXO] = {}
        self.spent_utxos: Set[str] = set()
    
    def add_utxo(self, utxo: UTXO):
        """Add a new UTXO to the pool"""
        utxo_id = utxo.get_id()
        if utxo_id not in self.spent_utxos:
            self.utxos[utxo_id] = utxo
    
    def spend_utxo(self, utxo_id: str) -> Optional[UTXO]:
        """Spend a UTXO"""
        if utxo_id in self.utxos:
            utxo = self.utxos.pop(utxo_id)
            self.spent_utxos.add(utxo_id)
            return utxo
        return None
    
    def get_utxo(self, utxo_id: str) -> Optional[UTXO]:
        """Get a UTXO without spending it"""
        return self.utxos.get(utxo_id)
    
    def get_utxos_for_address(self, address: str) -> List[UTXO]:
        """Get all UTXOs for a specific address"""
        return [utxo for utxo in self.utxos.values() if utxo.address == address]
    
    def get_balance(self, address: str) -> float:
        """Calculate balance for an address"""
        return sum(utxo.amount for utxo in self.get_utxos_for_address(address))
    
    def is_utxo_spent(self, utxo_id: str) -> bool:
        """Check if a UTXO has been spent"""
        return utxo_id in self.spent_utxos
    
    def get_total_utxos(self) -> int:
        """Get total number of UTXOs"""
        return len(self.utxos)
