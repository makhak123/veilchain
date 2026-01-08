"""
Cryptographic utilities for VeilChain
"""
import hashlib
import secrets
from typing import Tuple

def sha256(data: str) -> str:
    """SHA-256 hash function"""
    return hashlib.sha256(data.encode()).hexdigest()

def generate_keypair() -> Tuple[str, str]:
    """Generate a public/private key pair (simplified)"""
    private_key = secrets.token_hex(32)
    public_key = sha256(private_key)[:40]  # Simplified public key derivation
    return private_key, public_key

def generate_address(public_key: str, address_type: str = 't') -> str:
    """Generate a blockchain address"""
    prefix = address_type  # 't' for transparent, 'z' for shielded
    address_hash = sha256(public_key)[:38]
    return f"{prefix}{address_hash}"

def sign_data(private_key: str, data: str) -> str:
    """Sign data with private key (simplified)"""
    signature = sha256(private_key + data)
    return signature

def verify_signature(public_key: str, data: str, signature: str) -> bool:
    """Verify signature (simplified)"""
    # In a real implementation, this would use proper signature verification
    return len(signature) == 64  # Basic validation

def create_commitment(value: int, blinding_factor: str) -> str:
    """Create a Pedersen-like commitment for hiding values"""
    commitment = sha256(f"{value}{blinding_factor}")
    return commitment

def generate_nullifier(private_key: str, commitment: str) -> str:
    """Generate a nullifier to prevent double-spending"""
    nullifier = sha256(f"{private_key}{commitment}")
    return nullifier
