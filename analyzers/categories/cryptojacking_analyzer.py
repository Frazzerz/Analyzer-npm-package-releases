import re
from typing import Dict

class CryptojackingAnalyzer:
    """Analyze cryptojacking & wallet theft techniques"""
    
    CRYPTO_PATTERNS = {
        'bitcoin': re.compile(r'\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b'),
        'ethereum': re.compile(r'\b0x[a-fA-F0-9]{40}\b'),
        'tron': re.compile(r'\bT[1-9A-HJ-NP-Za-km-z]{33}\b'),
        'solana': re.compile(r'\b[1-9A-HJ-NP-Za-km-z]{32,44}\b')
    }
    
    WALLET_DETECTION_PATTERNS = [
        re.compile(r'window\.ethereum', re.IGNORECASE),
        re.compile(r'ethereum\.request', re.IGNORECASE),
        re.compile(r'eth_accounts', re.IGNORECASE),
        re.compile(r'window\.web3', re.IGNORECASE),
        re.compile(r'window\.solana', re.IGNORECASE)
    ]

    def analyze(self, content: str) -> Dict:
        
        metrics = {
            'crypto_addresses': 0,
            'wallet_detection': 0,
        }
        
        for pattern in self.CRYPTO_PATTERNS.values():
            metrics['crypto_addresses'] += len(pattern.findall(content))
        
        for pattern in self.WALLET_DETECTION_PATTERNS:
            metrics['wallet_detection'] += len(pattern.findall(content))
        
        return metrics