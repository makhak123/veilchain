"""
Create a new VeilChain wallet
"""
import sys
sys.path.append('.')

from src.wallet import Wallet
import json

def main():
    print("Creating new VeilChain wallet...\n")
    
    wallet = Wallet.create()
    
    print(wallet)
    
    # Save to file
    with open('wallet.json', 'w') as f:
        json.dump(wallet.to_dict(), f, indent=2)
    
    print("\n⚠️  WARNING: Keep your private key secure!")
    print("Wallet saved to wallet.json")

if __name__ == "__main__":
    main()
