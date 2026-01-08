"""
VeilChain demonstration script
"""
import sys
import time
sys.path.append('.')

from src.blockchain import VeilChain
from src.wallet import Wallet
from src.transaction import TransparentTransaction, ShieldedTransaction

def print_separator():
    print("\n" + "="*80 + "\n")

def main():
    print_separator()
    print("🔒 VEILCHAIN - Privacy-Focused Blockchain Demo")
    print_separator()
    
    # Create blockchain
    print("Creating VeilChain blockchain...")
    blockchain = VeilChain(difficulty=2)
    print(f"✓ Blockchain initialized with difficulty {blockchain.difficulty}")
    
    print_separator()
    
    # Create wallets
    print("Creating wallets...")
    alice = Wallet.create()
    bob = Wallet.create()
    charlie = Wallet.create()
    
    print(f"✓ Alice's wallet created")
    print(f"  Transparent: {alice.transparent_address}")
    print(f"  Shielded:    {alice.shielded_address}")
    print(f"\n✓ Bob's wallet created")
    print(f"  Transparent: {bob.transparent_address}")
    print(f"  Shielded:    {bob.shielded_address}")
    print(f"\n✓ Charlie's wallet created")
    print(f"  Transparent: {charlie.transparent_address}")
    print(f"  Shielded:    {charlie.shielded_address}")
    
    print_separator()
    
    # Mine initial block to get coins
    print("Mining initial block to distribute VEIL coins...")
    blockchain.mine_pending_transactions(alice.transparent_address)
    alice.balance = blockchain.get_balance(alice.transparent_address)
    print(f"✓ Alice received mining reward: {alice.balance} VEIL")
    
    print_separator()
    
    # Transparent transaction
    print("Creating TRANSPARENT transaction (public)...")
    transparent_tx = TransparentTransaction(
        sender=alice.transparent_address,
        recipient=bob.transparent_address,
        amount=3.0,
        timestamp=time.time()
    )
    transparent_tx.sign(alice.private_key)
    blockchain.add_transaction(transparent_tx)
    print(f"✓ Transparent TX: {alice.transparent_address[:20]}... → {bob.transparent_address[:20]}...")
    print(f"  Amount: 3.0 VEIL (visible on blockchain)")
    
    print_separator()
    
    # Shielded transaction
    print("Creating SHIELDED transaction (private)...")
    shielded_tx = ShieldedTransaction.create(
        sender_private_key=alice.private_key,
        recipient=charlie.shielded_address,
        amount=2.5,
        timestamp=time.time()
    )
    blockchain.add_transaction(shielded_tx)
    print(f"✓ Shielded TX created")
    print(f"  Commitment: {shielded_tx.commitment}")
    print(f"  Nullifier:  {shielded_tx.nullifier}")
    print(f"  Amount: HIDDEN (private)")
    print(f"  Sender: HIDDEN (private)")
    print(f"  Recipient: HIDDEN (private)")
    
    print_separator()
    
    # Mine block with transactions
    print("Mining block with both transaction types...")
    blockchain.mine_pending_transactions(bob.transparent_address)
    
    print_separator()
    
    # Show balances
    print("Checking transparent balances...")
    alice.balance = blockchain.get_balance(alice.transparent_address)
    bob.balance = blockchain.get_balance(bob.transparent_address)
    print(f"Alice: {alice.balance} VEIL")
    print(f"Bob:   {bob.balance} VEIL")
    print(f"Charlie: HIDDEN (shielded address)")
    
    print_separator()
    
    # Validate blockchain
    print("Validating blockchain integrity...")
    is_valid = blockchain.is_chain_valid()
    print(f"✓ Blockchain is {'VALID' if is_valid else 'INVALID'}")
    
    print_separator()
    
    # Show statistics
    print("Blockchain Statistics:")
    stats = blockchain.get_chain_stats()
    for key, value in stats.items():
        print(f"  {key.replace('_', ' ').title()}: {value}")
    
    print_separator()
    
    # Show chain
    print("Blockchain Contents:")
    for block in blockchain.chain:
        print(f"\nBlock #{block.index}")
        print(f"  Hash: {block.hash}")
        print(f"  Previous: {block.previous_hash}")
        print(f"  Transactions: {len(block.transactions)}")
        for i, tx in enumerate(block.transactions):
            tx_type = "SHIELDED" if isinstance(tx, ShieldedTransaction) else "TRANSPARENT"
            print(f"    TX {i+1}: {tx_type}")
    
    print_separator()
    print("Demo completed! VeilChain successfully demonstrated privacy features.")
    print_separator()

if __name__ == "__main__":
    main()
