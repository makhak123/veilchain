"""
Consensus rules and difficulty adjustment for VeilChain
"""
import time
from typing import List
from .block import Block

class ConsensusRules:
    """Consensus rules for VeilChain"""
    
    # Block timing
    TARGET_BLOCK_TIME = 150  # 2.5 minutes (like Zcash)
    DIFFICULTY_ADJUSTMENT_INTERVAL = 20  # Adjust every 20 blocks
    
    # Block limits
    MAX_BLOCK_SIZE = 2000000  # 2MB
    MAX_TRANSACTIONS_PER_BLOCK = 1000
    
    # Reward
    INITIAL_BLOCK_REWARD = 12.5
    HALVING_INTERVAL = 840000  # Halve reward every 840,000 blocks
    
    @staticmethod
    def calculate_difficulty(chain: List[Block]) -> int:
        """Calculate new difficulty based on block times"""
        if len(chain) < ConsensusRules.DIFFICULTY_ADJUSTMENT_INTERVAL:
            return 2  # Initial difficulty
        
        # Get last adjustment interval blocks
        recent_blocks = chain[-ConsensusRules.DIFFICULTY_ADJUSTMENT_INTERVAL:]
        
        # Calculate time taken
        time_taken = recent_blocks[-1].timestamp - recent_blocks[0].timestamp
        expected_time = ConsensusRules.TARGET_BLOCK_TIME * ConsensusRules.DIFFICULTY_ADJUSTMENT_INTERVAL
        
        # Adjust difficulty
        if time_taken < expected_time / 2:
            return recent_blocks[-1].difficulty + 1
        elif time_taken > expected_time * 2:
            return max(1, recent_blocks[-1].difficulty - 1)
        
        return recent_blocks[-1].difficulty
    
    @staticmethod
    def get_block_reward(block_height: int) -> float:
        """Calculate block reward based on height"""
        halvings = block_height // ConsensusRules.HALVING_INTERVAL
        reward = ConsensusRules.INITIAL_BLOCK_REWARD / (2 ** halvings)
        return max(0.00000001, reward)  # Minimum reward
    
    @staticmethod
    def validate_block_size(block: Block) -> bool:
        """Validate block size"""
        import sys
        block_size = sys.getsizeof(block)
        return block_size <= ConsensusRules.MAX_BLOCK_SIZE
    
    @staticmethod
    def validate_transaction_count(block: Block) -> bool:
        """Validate transaction count"""
        return len(block.transactions) <= ConsensusRules.MAX_TRANSACTIONS_PER_BLOCK
    
    @staticmethod
    def validate_block_time(block: Block, previous_block: Block) -> bool:
        """Validate block timestamp"""
        # Block time should be after previous block
        if block.timestamp <= previous_block.timestamp:
            return False
        
        # Block time should not be too far in the future (2 hours)
        if block.timestamp > time.time() + 7200:
            return False
        
        return True
