"""
Advanced demonstration of VeilChain features
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.blockchain import VeilChain
from src.wallet import Wallet
from src.transaction import TransparentTransaction, ShieldedTransaction
from src.network import Peer
from src.script import Script, OpCode
from src.mixing import StealthAddress
import time

def demo_multisig():
    """Demonstrate multi-signature transactions"""
    print("\n" + "="*60)
    print("MULTISIG TRANSACTION DEMO")
    print("="*60)
    
    # Create wallets
    wallet1 = Wallet.create()
    wallet2 = Wallet.create()
    wallet3 = Wallet.create()
    
    print(f"\nCreated 3 wallets for 2-of-3 multisig")
    print(f"Wallet 1: {wallet1.transparent_address[:20]}...")
    print(f"Wallet 2: {wallet2.transparent_address[:20]}...")
    print(f"Wallet 3: {wallet3.transparent_address[:20]}...")
    
    # Create multisig script (2-of-3)
    public_keys = [wallet1.public_key, wallet2.public_key, wallet3.public_key]
    multisig_script = Script.create_multisig_script(2, public_keys)
    
    print(f"\nCreated 2-of-3 multisig script")
    print("This requires 2 out of 3 signatures to spend funds")

def demo_timelock():
    """Demonstrate time-locked transactions"""
    print("\n" + "="*60)
    print("TIME-LOCKED TRANSACTION DEMO")
    print("="*60)
    
    wallet = Wallet.create()
    current_time = int(time.time())
    locktime = current_time + 3600  # Lock for 1 hour
    
    print(f"\nWallet: {wallet.transparent_address[:20]}...")
    print(f"Current time: {current_time}")
    print(f"Locktime: {locktime} (1 hour from now)")
    
    # Create time-locked script
    timelock_script = Script.create_timelock_script(locktime, wallet.public_key)
    
    print("\nTime-locked script created")
    print("Funds cannot be spent until locktime expires")

def demo_stealth_addresses():
    """Demonstrate stealth address generation"""
    print("\n" + "="*60)
    print("STEALTH ADDRESS DEMO")
    print("="*60)
    
    sender = Wallet.create()
    recipient = Wallet.create()
    
    print(f"\nRecipient public address: {recipient.transparent_address}")
    
    # Generate stealth address
    stealth_addr, ephemeral_pub = StealthAddress.generate_stealth_address(recipient.public_key)
    
    print(f"Stealth address: z{stealth_addr[:38]}")
    print(f"Ephemeral public key: {ephemeral_pub[:20]}...")
    
    print("\nStealth addresses provide receiver privacy")
    print("Each transaction uses a unique one-time address")

def demo_mixing():
    """Demonstrate transaction mixing"""
    print("\n" + "="*60)
    print("TRANSACTION MIXING DEMO")
    print("="*60)
    
    blockchain = VeilChain(difficulty=1)
    
    # Create multiple wallets
    wallets = [Wallet.create() for _ in range(5)]
    
    print(f"\nCreated {len(wallets)} wallets")
    
    # Add transactions to mixing pool
    for i, wallet in enumerate(wallets):
        tx = ShieldedTransaction.create(
            wallet.private_key,
            f"recipient_{i}",
            10.0,
            time.time()
        )
        blockchain.mixing_pool.add_to_pool(10.0, tx.commitment, time.time())
        print(f"Wallet {i+1} added 10.0 VEIL to mixing pool")
    
    # Mix transactions
    mixed = blockchain.mixing_pool.mix_transactions(10.0)
    
    print(f"\nMixed {len(mixed)} transactions")
    print(f"Anonymity set size: {len(mixed)}")
    print("Transaction origins are now hidden among the mixing set")

def demo_network():
    """Demonstrate P2P network"""
    print("\n" + "="*60)
    print("P2P NETWORK DEMO")
    print("="*60)
    
    # Create multiple nodes
    blockchain1 = VeilChain(difficulty=1, node_id="node_1")
    blockchain2 = VeilChain(difficulty=1, node_id="node_2")
    blockchain3 = VeilChain(difficulty=1, node_id="node_3")
    
    print("\nCreated 3 network nodes")
    
    # Connect peers
    peer2 = Peer("node_2", "localhost", 8002)
    peer3 = Peer("node_3", "localhost", 8003)
    
    blockchain1.network.add_peer(peer2)
    blockchain1.network.add_peer(peer3)
    
    print(f"Node 1 connected to {blockchain1.network.get_peer_count()} peers")
    
    # Mine a block on node 1
    wallet = Wallet.create()
    blockchain1.mine_pending_transactions(wallet.transparent_address)
    
    print(f"\nNode 1 mined block {blockchain1.get_latest_block().index}")
    print("Broadcasting block to peers...")
    
    # Simulate broadcast
    blockchain1.network.broadcast_block(blockchain1.get_latest_block())

def demo_chain_stats():
    """Show comprehensive blockchain statistics"""
    print("\n" + "="*60)
    print("BLOCKCHAIN STATISTICS")
    print("="*60)
    
    blockchain = VeilChain(difficulty=2)
    
    # Create some activity
    wallet1 = Wallet.create()
    wallet2 = Wallet.create()
    
    # Mine a few blocks
    for i in range(3):
        blockchain.mine_pending_transactions(wallet1.transparent_address)
    
    # Get stats
    stats = blockchain.get_chain_stats()
    
    print(f"\nTotal Blocks: {stats['total_blocks']}")
    print(f"Total Supply: {stats['total_supply']} VEIL")
    print(f"Transparent Transactions: {stats['total_transparent_transactions']}")
    print(f"Shielded Transactions: {stats['total_shielded_transactions']}")
    print(f"Current Difficulty: {stats['difficulty']}")
    print(f"Mempool Size: {stats['mempool_size']}")
    print(f"UTXO Count: {stats['utxo_count']}")
    print(f"Connected Peers: {stats['connected_peers']}")
    print(f"Anonymity Set Size: {stats['anonymity_set_size']}")

def main():
    print("\n" + "="*60)
    print("VEILCHAIN - ADVANCED FEATURES DEMONSTRATION")
    print("="*60)
    
    try:
        demo_multisig()
        demo_timelock()
        demo_stealth_addresses()
        demo_mixing()
        demo_network()
        demo_chain_stats()
        
        print("\n" + "="*60)
        print("DEMO COMPLETED SUCCESSFULLY")
        print("="*60)
        
    except Exception as e:
        print(f"\nError during demo: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
