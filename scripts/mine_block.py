"""
Mine a block on VeilChain
"""
import sys
import time
sys.path.append('.')

from src.blockchain import VeilChain
from src.transaction import TransparentTransaction

def main():
    print("VeilChain Mining Tool\n")
    
    # Create blockchain
    blockchain = VeilChain(difficulty=3)
    
    # Add some sample transactions
    tx1 = TransparentTransaction(
        sender="tSampleSender123",
        recipient="tSampleRecipient456",
        amount=5.0,
        timestamp=time.time()
    )
    
    blockchain.add_transaction(tx1)
    
    # Mine block
    miner_address = "tMinerAddress789"
    print(f"Mining block for address: {miner_address}\n")
    
    blockchain.mine_pending_transactions(miner_address)
    
    print(f"\n✓ Block mined successfully!")
    print(f"Miner balance: {blockchain.get_balance(miner_address)} VEIL")

if __name__ == "__main__":
    main()
