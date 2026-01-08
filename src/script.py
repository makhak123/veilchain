"""
Scripting system for VeilChain - Similar to Bitcoin Script
"""
from typing import List, Dict, Any
from enum import Enum
from .crypto import sha256, verify_signature

class OpCode(Enum):
    """Script operation codes"""
    # Stack operations
    OP_DUP = "OP_DUP"
    OP_DROP = "OP_DROP"
    OP_SWAP = "OP_SWAP"
    
    # Crypto operations
    OP_HASH256 = "OP_HASH256"
    OP_CHECKSIG = "OP_CHECKSIG"
    OP_CHECKMULTISIG = "OP_CHECKMULTISIG"
    
    # Arithmetic
    OP_ADD = "OP_ADD"
    OP_SUB = "OP_SUB"
    OP_EQUAL = "OP_EQUAL"
    OP_VERIFY = "OP_VERIFY"
    
    # Time locks
    OP_CHECKLOCKTIMEVERIFY = "OP_CHECKLOCKTIMEVERIFY"
    OP_CHECKSEQUENCEVERIFY = "OP_CHECKSEQUENCEVERIFY"
    
    # Control flow
    OP_IF = "OP_IF"
    OP_ELSE = "OP_ELSE"
    OP_ENDIF = "OP_ENDIF"
    OP_RETURN = "OP_RETURN"

class Script:
    """Script execution engine"""
    
    def __init__(self, script: List[Any]):
        self.script = script
        self.stack: List[Any] = []
    
    def execute(self, context: Dict[str, Any] = None) -> bool:
        """Execute the script"""
        context = context or {}
        
        for item in self.script:
            if isinstance(item, OpCode):
                if not self._execute_opcode(item, context):
                    return False
            else:
                # Push data onto stack
                self.stack.append(item)
        
        # Script succeeds if stack has true value
        return len(self.stack) > 0 and self.stack[-1] == True
    
    def _execute_opcode(self, opcode: OpCode, context: Dict[str, Any]) -> bool:
        """Execute a single opcode"""
        try:
            if opcode == OpCode.OP_DUP:
                if len(self.stack) < 1:
                    return False
                self.stack.append(self.stack[-1])
            
            elif opcode == OpCode.OP_DROP:
                if len(self.stack) < 1:
                    return False
                self.stack.pop()
            
            elif opcode == OpCode.OP_SWAP:
                if len(self.stack) < 2:
                    return False
                self.stack[-1], self.stack[-2] = self.stack[-2], self.stack[-1]
            
            elif opcode == OpCode.OP_HASH256:
                if len(self.stack) < 1:
                    return False
                data = str(self.stack.pop())
                self.stack.append(sha256(sha256(data)))
            
            elif opcode == OpCode.OP_CHECKSIG:
                if len(self.stack) < 2:
                    return False
                public_key = self.stack.pop()
                signature = self.stack.pop()
                message = context.get('message', '')
                result = verify_signature(public_key, message, signature)
                self.stack.append(result)
            
            elif opcode == OpCode.OP_CHECKMULTISIG:
                # Simplified multisig verification
                if len(self.stack) < 3:
                    return False
                n_required = self.stack.pop()
                n_total = self.stack.pop()
                
                if len(self.stack) < n_total + n_required:
                    return False
                
                # Get public keys and signatures
                public_keys = [self.stack.pop() for _ in range(n_total)]
                signatures = [self.stack.pop() for _ in range(n_required)]
                
                # Verify signatures
                message = context.get('message', '')
                valid_sigs = sum(1 for sig, pk in zip(signatures, public_keys) 
                               if verify_signature(pk, message, sig))
                
                self.stack.append(valid_sigs >= n_required)
            
            elif opcode == OpCode.OP_ADD:
                if len(self.stack) < 2:
                    return False
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a + b)
            
            elif opcode == OpCode.OP_SUB:
                if len(self.stack) < 2:
                    return False
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a - b)
            
            elif opcode == OpCode.OP_EQUAL:
                if len(self.stack) < 2:
                    return False
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a == b)
            
            elif opcode == OpCode.OP_VERIFY:
                if len(self.stack) < 1:
                    return False
                if not self.stack.pop():
                    return False
            
            elif opcode == OpCode.OP_CHECKLOCKTIMEVERIFY:
                if len(self.stack) < 1:
                    return False
                locktime = self.stack[-1]  # Don't pop
                current_time = context.get('block_time', 0)
                if current_time < locktime:
                    return False
            
            elif opcode == OpCode.OP_RETURN:
                return False  # OP_RETURN always fails execution
            
            return True
            
        except Exception as e:
            print(f"Script execution error: {e}")
            return False
    
    @staticmethod
    def create_p2pkh_script(public_key_hash: str) -> 'Script':
        """Create Pay-to-Public-Key-Hash script"""
        return Script([
            OpCode.OP_DUP,
            OpCode.OP_HASH256,
            public_key_hash,
            OpCode.OP_EQUAL,
            OpCode.OP_VERIFY,
            OpCode.OP_CHECKSIG
        ])
    
    @staticmethod
    def create_multisig_script(n_required: int, public_keys: List[str]) -> 'Script':
        """Create multisig script (n-of-m)"""
        return Script([
            len(public_keys),
            n_required,
            OpCode.OP_CHECKMULTISIG
        ])
    
    @staticmethod
    def create_timelock_script(locktime: int, public_key_hash: str) -> 'Script':
        """Create time-locked script"""
        return Script([
            locktime,
            OpCode.OP_CHECKLOCKTIMEVERIFY,
            OpCode.OP_DROP,
            OpCode.OP_DUP,
            OpCode.OP_HASH256,
            public_key_hash,
            OpCode.OP_EQUAL,
            OpCode.OP_VERIFY,
            OpCode.OP_CHECKSIG
        ])
