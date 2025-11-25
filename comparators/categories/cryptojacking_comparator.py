from typing import Dict
from models import FileMetrics

class CryptojackingComparator:
    """Compare cryptojacking & wallet theft metrics to identify red flags"""
    
    def compare(self, prev: FileMetrics, curr: FileMetrics) -> Dict:
        
        # New file
        if prev is None:
            return {
                'crypto_addresses_introduced': curr.crypto_addresses > 0,
                'wallet_checks_introduced': curr.wallet_detection > 0,
            }
        else:
            # Existing file
            return {
                'crypto_addresses_introduced': (prev.crypto_addresses < curr.crypto_addresses),
                'wallet_checks_introduced': (prev.wallet_detection < curr.wallet_detection),
            }