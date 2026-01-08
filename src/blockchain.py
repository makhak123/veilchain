"""
Core blockchain implementation for VeilChain
"""
from typing import List, Union, Optional
import time
from .block import Block
from .transaction import TransparentTransaction, ShieldedTransaction
from .privacy import PrivacyLayer
from .utxo import UTXOPool, UTXO
from .mempool import Mempool
from .consensus import ConsensusRules
from .mixing import MixingPool, RingSignature
from .network import P2PNetwork

class VeilChain:
    """VeilChain blockchain implementation with advanced features"""
    
    def __init__(self, difficulty: int = 2, node_id: str = "node_0"):
        self.chain: List[Block] = []
        self.difficulty = difficulty
        self.pending_transactions: List[Union[TransparentTransaction, ShieldedTransaction]] = []
        self.mining_reward = ConsensusRules.INITIAL_BLOCK_REWARD
        
        self.privacy_layer = PrivacyLayer()
        self.utxo_pool = UTXOPool()
        self.mempool = Mempool()
        self.mixing_pool = MixingPool()
        self.ring_signature = RingSignature()
        self.network = P2PNetwork(node_id)
        self.network.blockchain = self
        
        self.orphaned_blocks: List[Block] = []
        self.max_reorg_depth = 6
        
        # Create genesis block
        self.create_genesis_block()
    
    def create_genesis_block(self):
        """Create the first block in the chain"""
        genesis_block = Block(
            index=0,
            timestamp=time.time(),
            transactions=[],
            previous_hash="0",
            difficulty=self.difficulty,
            version=1
        )
        genesis_block.merkle_root = genesis_block.calculate_merkle_root()
        genesis_block.hash = genesis_block.calculate_hash()
        self.chain.append(genesis_block)
        print("Genesis block created")
    
    def get_latest_block(self) -> Block:
        """Get the most recent block"""
        return self.chain[-1]
    
    def add_transaction(self, transaction: Union[TransparentTransaction, ShieldedTransaction], 
                       fee: float = 0.001) -> bool:
        """Add a transaction to the mempool"""
        # Verify transaction based on type
        if isinstance(transaction, ShieldedTransaction):
            if not self.privacy_layer.verify_shielded_transaction(transaction):
                return False
        
        # Add to mempool instead of pending transactions
        return self.mempool.add_transaction(transaction, fee)
    
    def mine_pending_transactions(self, mining_reward_address: str):
        """Mine a new block with pending transactions from mempool"""
        transactions = self.mempool.get_transactions_for_mining(max_transactions=100)
        
        block_height = len(self.chain)
        block_reward = ConsensusRules.get_block_reward(block_height)
        
        # Create reward transaction
        reward_tx = TransparentTransaction(
            sender="COINBASE",
            recipient=mining_reward_address,
            amount=block_reward,
            timestamp=time.time()
        )
        
        # Add reward to transactions
        transactions = transactions + [reward_tx]
        
        if block_height > 0 and block_height % ConsensusRules.DIFFICULTY_ADJUSTMENT_INTERVAL == 0:
            self.difficulty = ConsensusRules.calculate_difficulty(self.chain)
            print(f"Difficulty adjusted to: {self.difficulty}")
        
        # Create new block
        new_block = Block(
            index=block_height,
            timestamp=time.time(),
            transactions=transactions,
            previous_hash=self.get_latest_block().hash,
            difficulty=self.difficulty,
            version=1
        )
        
        # Mine the block
        print(f"Mining block {new_block.index}...")
        new_block.mine_block(self.difficulty)
        
        # Validate block before adding
        if self.validate_new_block(new_block):
            # Add to chain
            self.chain.append(new_block)
            
            for tx in transactions:
                self.mempool.remove_transaction(tx.calculate_hash())
            
            self.network.broadcast_block(new_block)
            
            print(f"Block {new_block.index} added to chain")
        else:
            print(f"Block {new_block.index} validation failed")
    
    def validate_new_block(self, block: Block) -> bool:
        """Validate a new block before adding to chain"""
        # Verify hash
        if block.hash != block.calculate_hash():
            print("Invalid block hash")
            return False
        
        # Verify previous hash
        if block.previous_hash != self.get_latest_block().hash:
            print("Invalid previous hash")
            return False
        
        # Verify proof of work
        if not block.hash.startswith('0' * block.difficulty):
            print("Invalid proof of work")
            return False
        
        if not block.verify_merkle_root():
            print("Invalid merkle root")
            return False
        
        if not ConsensusRules.validate_block_size(block):
            print("Block size exceeds limit")
            return False
        
        if not ConsensusRules.validate_transaction_count(block):
            print("Too many transactions in block")
            return False
        
        if len(self.chain) > 0:
            if not ConsensusRules.validate_block_time(block, self.get_latest_block()):
                print("Invalid block timestamp")
                return False
        
        return True
    
    def handle_chain_reorganization(self, competing_chain: List[Block]) -> bool:
        """Handle blockchain reorganization"""
        # Only reorg if competing chain is longer and valid
        if len(competing_chain) <= len(self.chain):
            return False
        
        # Validate competing chain
        temp_blockchain = VeilChain(node_id=self.network.node_id)
        temp_blockchain.chain = competing_chain
        
        if not temp_blockchain.is_chain_valid():
            return False
        
        # Store orphaned blocks
        reorg_depth = len(self.chain) - len(competing_chain)
        if abs(reorg_depth) > self.max_reorg_depth:
            print(f"Reorganization depth {abs(reorg_depth)} exceeds maximum {self.max_reorg_depth}")
            return False
        
        self.orphaned_blocks.extend(self.chain[len(competing_chain):])
        self.chain = competing_chain
        
        print(f"Chain reorganized: {len(self.orphaned_blocks)} blocks orphaned")
        return True
    
    def is_chain_valid(self) -> bool:
        """Validate the entire blockchain"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Check if hash is correct
            if current_block.hash != current_block.calculate_hash():
                print(f"Invalid hash at block {i}")
                return False
            
            # Check if previous hash matches
            if current_block.previous_hash != previous_block.hash:
                print(f"Invalid previous hash at block {i}")
                return False
            
            if not current_block.verify_merkle_root():
                print(f"Invalid merkle root at block {i}")
                return False
            
            # Check proof of work
            if not current_block.hash.startswith('0' * current_block.difficulty):
                print(f"Invalid proof of work at block {i}")
                return False
        
        return True
    
    def get_balance(self, address: str) -> float:
        """Get balance for a transparent address using UTXO model"""
        return self.utxo_pool.get_balance(address)
    
    def get_chain_stats(self) -> dict:
        """Get blockchain statistics"""
        total_transparent = 0
        total_shielded = 0
        total_supply = 0.0
        
        for block in self.chain:
            for tx in block.transactions:
                if isinstance(tx, TransparentTransaction):
                    total_transparent += 1
                    if tx.sender == "COINBASE":
                        total_supply += tx.amount
                elif isinstance(tx, ShieldedTransaction):
                    total_shielded += 1
        
        return {
            'total_blocks': len(self.chain),
            'total_transparent_transactions': total_transparent,
            'total_shielded_transactions': total_shielded,
            'anonymity_set_size': self.privacy_layer.get_anonymity_set_size(),
            'difficulty': self.difficulty,
            'total_supply': total_supply,
            'mempool_size': self.mempool.get_size(),
            'utxo_count': self.utxo_pool.get_total_utxos(),
            'connected_peers': self.network.get_peer_count(),
            'orphaned_blocks': len(self.orphaned_blocks)
        }
