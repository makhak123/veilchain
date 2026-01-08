# VeilChain

CA: H7bRCULbPip3GcTsbg9iKNYZZXnm159FWkSnMs8Spump

A privacy-focused blockchain implementation inspired by Zcash, featuring zero-knowledge proof concepts, advanced scripting, transaction mixing, and sophisticated privacy protocols for anonymous transactions.

## Features

### Privacy & Anonymity
- **Shielded Transactions**: Hide transaction amounts and addresses using cryptographic commitments
- **Transaction Mixing**: CoinJoin-style mixing pools for enhanced anonymity
- **Ring Signatures**: Unlinkable transactions with plausible deniability
- **Stealth Addresses**: One-time addresses for receiver privacy
- **Zero-Knowledge Proofs**: Simplified zk-SNARK-like verification system

### Transaction Types
- **Transparent Transactions**: Public transactions (like Bitcoin) for auditability
- **UTXO Model**: Unspent Transaction Output system for better security
- **Multisig Support**: N-of-M multi-signature transactions
- **Time-Locked Transactions**: Lock funds until specific time/block height

### Blockchain Features
- **Proof of Work**: Adjustable difficulty mining with hashrate monitoring
- **Merkle Trees**: Efficient transaction verification with SPV support
- **Dynamic Difficulty**: Automatic difficulty adjustment every 20 blocks
- **Block Reward Halving**: Controlled supply with halvings every 840,000 blocks
- **Chain Reorganization**: Fork resolution with configurable reorg depth
- **Mempool**: Priority-based transaction pool with fee market

### Network & Consensus
- **P2P Network**: Peer-to-peer networking with reputation scoring
- **Consensus Rules**: Comprehensive validation (block size, timestamps, PoW)
- **Block Broadcasting**: Efficient block and transaction propagation
- **Network Sync**: Blockchain synchronization across nodes

### Smart Contracts
- **Script System**: Bitcoin-like scripting language with opcodes
- **Script Operations**: Stack manipulation, crypto ops, control flow
- **Custom Scripts**: Pay-to-PubKey-Hash (P2PKH), multisig, timelocks

## Architecture

VeilChain implements a sophisticated multi-layer architecture:

1. **Transaction Layer**: Transparent and shielded transaction types with UTXO model
2. **Privacy Layer**: Zero-knowledge proofs, mixing, ring signatures, stealth addresses
3. **Consensus Layer**: Dynamic PoW difficulty, validation rules, block rewards
4. **Network Layer**: P2P networking with peer discovery and sync
5. **Script Layer**: Programmable transaction conditions and smart contracts

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/veilchain.git
cd veilchain

# No dependencies required - uses only Python standard library
```

## Usage

### Running the Full Demo

```bash
python scripts/demo.py
```

### Running Advanced Features Demo

```bash
python scripts/advanced_demo.py
```

This demonstrates:
- Multi-signature transactions (2-of-3)
- Time-locked transactions
- Stealth address generation
- Transaction mixing pools
- P2P network simulation
- Comprehensive blockchain statistics

### Creating a Wallet

```bash
python scripts/create_wallet.py
```

### Mining Blocks

```bash
python scripts/mine_block.py
```

## Project Structure

```
veilchain/
├── src/
│   ├── blockchain.py       # Core blockchain with advanced features
│   ├── block.py           # Block structure with Merkle trees
│   ├── transaction.py     # Transaction types (transparent/shielded)
│   ├── wallet.py          # Wallet management
│   ├── privacy.py         # Privacy layer (zk-proof simulation)
│   ├── crypto.py          # Cryptographic utilities
│   ├── utxo.py           # UTXO model implementation
│   ├── merkle.py         # Merkle tree for transactions
│   ├── mempool.py        # Transaction memory pool
│   ├── consensus.py      # Consensus rules & difficulty
│   ├── network.py        # P2P networking layer
│   ├── script.py         # Scripting system (opcodes)
│   └── mixing.py         # Transaction mixing & ring sigs
├── scripts/
│   ├── demo.py           # Basic demonstration
│   ├── advanced_demo.py  # Advanced features demo
│   ├── create_wallet.py  # Wallet creation tool
│   └── mine_block.py     # Mining tool
├── tests/
│   └── test_blockchain.py # Unit tests
└── README.md
```

## How It Works

### Shielded Transactions

VeilChain uses a simplified version of zero-knowledge proofs to enable private transactions:

1. **Commitment Scheme**: Transaction values are hidden using Pedersen-like commitments
2. **Nullifiers**: Prevent double-spending without revealing which output is spent
3. **zk-SNARK Simulation**: Proves transaction validity without revealing details
4. **Blinding Factors**: Random values ensure commitments are cryptographically secure

### Transaction Mixing

Mixing pools enhance privacy by grouping similar-valued transactions:

1. **Pool Formation**: Transactions of similar amounts are grouped together
2. **Minimum Anonymity Set**: At least 3 transactions required for mixing
3. **Unlinkability**: Output transactions cannot be linked to input transactions
4. **Ring Signatures**: Additional layer providing plausible deniability

### Ring Signatures

Unlinkable transaction signatures using ring signature scheme:

1. **Ring Creation**: Transaction signed by one member of a group
2. **Key Image**: Prevents double-spending without revealing signer
3. **Anonymity**: Impossible to determine which ring member signed
4. **Verification**: Anyone can verify signature is from ring member

### Stealth Addresses

One-time addresses for receiver privacy:

1. **Ephemeral Keys**: Sender generates one-time keypair per transaction
2. **Shared Secret**: Derived from sender ephemeral + recipient public key
3. **Stealth Address**: Unique address only recipient can spend from
4. **Recovery**: Recipient scans blockchain to find their transactions

### UTXO Model

Unspent Transaction Output system similar to Bitcoin:

1. **Transaction Inputs**: References to previous outputs being spent
2. **Transaction Outputs**: New UTXOs created by transaction
3. **UTXO Pool**: Tracks all spendable outputs
4. **Double-Spend Prevention**: Spent UTXOs removed from pool

### Script System

Programmable transaction conditions:

```python
# Pay-to-PubKey-Hash Script
OP_DUP → OP_HASH256 → <pubKeyHash> → OP_EQUAL → OP_VERIFY → OP_CHECKSIG

# 2-of-3 Multisig Script
3 → 2 → OP_CHECKMULTISIG

# Time-Locked Script
<locktime> → OP_CHECKLOCKTIMEVERIFY → OP_DROP → [P2PKH Script]
```

### Consensus Rules

- **Target Block Time**: 150 seconds (2.5 minutes like Zcash)
- **Difficulty Adjustment**: Every 20 blocks
- **Initial Block Reward**: 12.5 VEIL
- **Halving Interval**: Every 840,000 blocks
- **Max Block Size**: 2MB
- **Max Transactions**: 1,000 per block

### Transaction Flow

```
Sender Wallet → Create TX → Sign → Add to Mempool
                                         ↓
                              Priority Sorting (fee × age)
                                         ↓
Miner Selects TXs ← Verify Proofs ← Validate ← Check Nullifiers
         ↓
Create Block → Mine (PoW) → Broadcast → Peers Validate → Add to Chain
```

## Technical Details

### Cryptography
- **Hashing**: SHA-256 for all hash operations
- **Signatures**: Simplified signature scheme (educational)
- **Commitments**: Pedersen-like commitments for hiding values
- **Merkle Trees**: Binary tree structure for transaction verification

### Mining
- **Algorithm**: SHA-256 proof-of-work
- **Difficulty**: Dynamic adjustment based on block times
- **Target**: Adjusts to maintain ~150 second block time
- **Hashrate Monitoring**: Real-time mining statistics

### Network
- **Max Peers**: 8 simultaneous connections
- **Peer Reputation**: 0-100 score based on behavior
- **Message Types**: new_block, new_transaction, get_blockchain
- **Sync Protocol**: Longest valid chain wins

## Security Notes

⚠️ **This is an educational implementation**. It demonstrates privacy and blockchain concepts but is NOT suitable for production use. Real implementations like Zcash use:
- Battle-tested cryptographic libraries (libsodium, bellman)
- Formal security proofs and audits
- Optimized zk-SNARK circuits
- Production-grade networking protocols

## Comparison with Zcash

| Feature | VeilChain | Zcash |
|---------|-----------|-------|
| Privacy | Simplified zk-proofs, mixing, ring sigs | Full zk-SNARKs (Sapling/Orchard) |
| Address Types | t-addr, z-addr | t-addr, z-addr (unified) |
| UTXO Model | ✅ | ✅ |
| Scripting | Bitcoin-like opcodes | Bitcoin Script |
| Consensus | SHA-256 PoW | Equihash PoW |
| Block Time | 150s (adjustable) | 75s |
| Merkle Trees | ✅ | ✅ |
| Network | Simulated P2P | Full P2P (libp2p) |
| Mixing | Built-in pools | Optional (via Orchard) |
| Ring Signatures | ✅ | ❌ (uses zk-SNARKs instead) |
| Stealth Addresses | ✅ | ✅ (diversified addresses) |
| Language | Python | C++/Rust |
| Purpose | Educational | Production |
| Security | Demo-level | Production-grade |

## Advanced Features

### Multisig Transactions

Create N-of-M signature requirements:

```python
# 2-of-3 multisig
public_keys = [wallet1.pub_key, wallet2.pub_key, wallet3.pub_key]
script = Script.create_multisig_script(2, public_keys)
```

### Time-Locked Transactions

Lock funds until specific time:

```python
locktime = int(time.time()) + 3600  # 1 hour
script = Script.create_timelock_script(locktime, public_key_hash)
```

### Transaction Mixing

Enhance privacy through mixing:

```python
# Add to mixing pool
mixing_pool.add_to_pool(amount, commitment, timestamp)

# Mix when pool has enough similar amounts
mixed_commitments = mixing_pool.mix_transactions(amount)
```

### Stealth Addresses

Generate one-time addresses:

```python
stealth_addr, ephemeral_pub = StealthAddress.generate_stealth_address(
    recipient_public_key
)
```

## Performance

- **Block Mining**: ~1-10 seconds (difficulty 2)
- **Transaction Verification**: < 1ms per transaction
- **Merkle Proof**: O(log n) verification complexity
- **Blockchain Sync**: Linear with chain length
- **Mempool**: Priority queue with O(log n) insertion

## Future Enhancements

- [ ] GUI wallet application
- [ ] Full network implementation (sockets)
- [ ] Real cryptographic libraries (libsodium)
- [ ] SPV (Simplified Payment Verification) clients
- [ ] Shielded coinbase transactions
- [ ] Cross-chain atomic swaps
- [ ] Smart contract VM
- [ ] WebAssembly compilation
- [ ] Mobile wallet support

## Contributing

Contributions are welcome! Areas of interest:
- Performance optimizations
- Additional privacy features
- Network protocol improvements
- Test coverage expansion
- Documentation improvements

Please feel free to submit pull requests or open issues.

## License

MIT License - See LICENSE file for details

## Acknowledgments

Inspired by:
- **Zcash**: Pioneering blockchain privacy with zk-SNARKs
- **Bitcoin**: UTXO model and proof-of-work consensus
- **Monero**: Ring signatures and stealth addresses
- **CoinJoin**: Transaction mixing concepts

## Resources

- [Zcash Protocol Specification](https://zips.z.cash/)
- [Bitcoin Script](https://en.bitcoin.it/wiki/Script)
- [Zero-Knowledge Proofs](https://z.cash/technology/zksnarks/)
- [Ring Signatures](https://en.wikipedia.org/wiki/Ring_signature)
- [Merkle Trees](https://en.wikipedia.org/wiki/Merkle_tree)
