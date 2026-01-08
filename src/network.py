"""
Peer-to-peer network simulation for VeilChain
"""
from typing import List, Dict, Set
import json
import time
from .blockchain import VeilChain
from .block import Block

class Peer:
    """Represents a network peer"""
    
    def __init__(self, peer_id: str, host: str, port: int):
        self.peer_id = peer_id
        self.host = host
        self.port = port
        self.last_seen = time.time()
        self.reputation = 100  # Reputation score
    
    def to_dict(self) -> dict:
        return {
            'peer_id': self.peer_id,
            'host': self.host,
            'port': self.port,
            'last_seen': self.last_seen,
            'reputation': self.reputation
        }

class NetworkMessage:
    """Network message structure"""
    
    def __init__(self, message_type: str, data: dict, sender: str):
        self.type = message_type
        self.data = data
        self.sender = sender
        self.timestamp = time.time()
    
    def to_dict(self) -> dict:
        return {
            'type': self.type,
            'data': self.data,
            'sender': self.sender,
            'timestamp': self.timestamp
        }

class P2PNetwork:
    """Peer-to-peer network manager"""
    
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.peers: Dict[str, Peer] = {}
        self.blockchain: VeilChain = None
        self.message_history: Set[str] = set()
        self.max_peers = 8
    
    def add_peer(self, peer: Peer) -> bool:
        """Add a peer to the network"""
        if len(self.peers) >= self.max_peers:
            # Remove lowest reputation peer
            lowest_rep_peer = min(self.peers.values(), key=lambda p: p.reputation)
            self.remove_peer(lowest_rep_peer.peer_id)
        
        self.peers[peer.peer_id] = peer
        print(f"[Network] Added peer {peer.peer_id}")
        return True
    
    def remove_peer(self, peer_id: str):
        """Remove a peer from the network"""
        if peer_id in self.peers:
            del self.peers[peer_id]
            print(f"[Network] Removed peer {peer_id}")
    
    def broadcast_block(self, block: Block):
        """Broadcast a new block to all peers"""
        message = NetworkMessage(
            message_type="new_block",
            data=block.to_dict(),
            sender=self.node_id
        )
        
        print(f"[Network] Broadcasting block {block.index} to {len(self.peers)} peers")
        
        for peer in self.peers.values():
            self.send_message(peer, message)
    
    def broadcast_transaction(self, transaction):
        """Broadcast a new transaction to all peers"""
        message = NetworkMessage(
            message_type="new_transaction",
            data=transaction.to_dict(),
            sender=self.node_id
        )
        
        print(f"[Network] Broadcasting transaction to {len(self.peers)} peers")
        
        for peer in self.peers.values():
            self.send_message(peer, message)
    
    def send_message(self, peer: Peer, message: NetworkMessage):
        """Send message to a specific peer (simulated)"""
        message_id = f"{message.sender}:{message.timestamp}"
        if message_id not in self.message_history:
            self.message_history.add(message_id)
            # In a real implementation, this would send over network
            print(f"[Network] Sent {message.type} to {peer.peer_id}")
    
    def request_blockchain(self, peer: Peer):
        """Request blockchain from a peer"""
        message = NetworkMessage(
            message_type="get_blockchain",
            data={},
            sender=self.node_id
        )
        self.send_message(peer, message)
    
    def sync_blockchain(self, other_chain: List[Block]) -> bool:
        """Sync blockchain with received chain"""
        if len(other_chain) > len(self.blockchain.chain):
            # Validate the received chain
            temp_blockchain = VeilChain()
            temp_blockchain.chain = other_chain
            
            if temp_blockchain.is_chain_valid():
                self.blockchain.chain = other_chain
                print(f"[Network] Synced blockchain ({len(other_chain)} blocks)")
                return True
        
        return False
    
    def get_peer_count(self) -> int:
        """Get number of connected peers"""
        return len(self.peers)
    
    def update_peer_reputation(self, peer_id: str, change: int):
        """Update peer reputation score"""
        if peer_id in self.peers:
            self.peers[peer_id].reputation = max(0, min(100, self.peers[peer_id].reputation + change))
