"""
Memory pool for pending transactions
"""
from typing import List, Dict, Union, Optional
import time
from .transaction import TransparentTransaction, ShieldedTransaction
from .utxo import TransactionInput, TransactionOutput, UTXOPool

class TransactionPriority:
    """Calculate transaction priority for mining"""
    
    @staticmethod
    def calculate_priority(transaction: Union[TransparentTransaction, ShieldedTransaction], 
                         fee: float, age: float) -> float:
        """Calculate transaction priority based on fee and age"""
        # Priority = fee * age
        # Older transactions with higher fees get priority
        return fee * age

class Mempool:
    """Memory pool for pending transactions"""
    
    def __init__(self):
        self.transactions: List[Dict] = []
        self.transaction_fees: Dict[str, float] = {}
        self.max_size = 1000  # Maximum transactions in mempool
    
    def add_transaction(self, transaction: Union[TransparentTransaction, ShieldedTransaction], 
                       fee: float = 0.001) -> bool:
        """Add transaction to mempool"""
        if len(self.transactions) >= self.max_size:
            # Remove lowest priority transaction
            self.evict_lowest_priority()
        
        tx_hash = transaction.calculate_hash()
        
        # Check if transaction already exists
        if any(tx['hash'] == tx_hash for tx in self.transactions):
            return False
        
        self.transactions.append({
            'transaction': transaction,
            'hash': tx_hash,
            'timestamp': time.time(),
            'fee': fee
        })
        
        self.transaction_fees[tx_hash] = fee
        return True
    
    def remove_transaction(self, tx_hash: str):
        """Remove transaction from mempool"""
        self.transactions = [tx for tx in self.transactions if tx['hash'] != tx_hash]
        self.transaction_fees.pop(tx_hash, None)
    
    def get_transactions_for_mining(self, max_transactions: int = 100) -> List:
        """Get highest priority transactions for mining"""
        # Sort by priority (fee * age)
        current_time = time.time()
        sorted_transactions = sorted(
            self.transactions,
            key=lambda tx: TransactionPriority.calculate_priority(
                tx['transaction'],
                tx['fee'],
                current_time - tx['timestamp']
            ),
            reverse=True
        )
        
        return [tx['transaction'] for tx in sorted_transactions[:max_transactions]]
    
    def evict_lowest_priority(self):
        """Remove lowest priority transaction"""
        if not self.transactions:
            return
        
        current_time = time.time()
        lowest_priority_tx = min(
            self.transactions,
            key=lambda tx: TransactionPriority.calculate_priority(
                tx['transaction'],
                tx['fee'],
                current_time - tx['timestamp']
            )
        )
        
        self.remove_transaction(lowest_priority_tx['hash'])
    
    def get_size(self) -> int:
        """Get current mempool size"""
        return len(self.transactions)
    
    def clear(self):
        """Clear all transactions"""
        self.transactions = []
        self.transaction_fees = {}
