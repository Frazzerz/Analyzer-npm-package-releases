from typing import Dict
from models import FileMetrics

class CryptojackingComparator:
    """Compare cryptojacking & wallet theft metrics to identify red flags"""
    
    def compare(self, prev: FileMetrics, curr: FileMetrics) -> Dict:
        
        # New file
        if prev is None:
            return {
                'initial_presence_of_crypto_addresses': curr.crypto_addresses > 0,
                'crypto_addresses_introduced': False,
                'crypto_addresses_increase': False,
                'change_crypto_addresses': False,
                'initial_presence_of_cryptocurrency_name': curr.cryptocurrency_name > 0,
                'cryptocurrency_name_introduced': False,
                'cryptocurrency_name_increase': False,
                'initial_presence_of_wallet_checks': curr.wallet_detection > 0,
                'wallet_checks_introduced': False,
                'wallet_checks_increase': False,
                'replaced_crypto_addresses_introduced': curr.replaced_crypto_addresses > 0,
                'hook_provider_introduced': curr.hook_provider > 0
            }
        else:
            # Existing file
            return {
                'initial_presence_of_crypto_addresses': False,
                'crypto_addresses_introduced': prev.crypto_addresses == 0 and curr.crypto_addresses > 0,
                'crypto_addresses_increase': prev.crypto_addresses != 0 and prev.crypto_addresses < curr.crypto_addresses,    # increase only if previously is non-zero
                'change_crypto_addresses': (prev.crypto_addresses == curr.crypto_addresses and 
                    set(prev.list_crypto_addresses) != set(curr.list_crypto_addresses)),
                'initial_presence_of_cryptocurrency_name': False,
                'cryptocurrency_name_introduced': prev.cryptocurrency_name == 0 and curr.cryptocurrency_name > 0,
                'cryptocurrency_name_increase': prev.cryptocurrency_name != 0 and prev.cryptocurrency_name < curr.cryptocurrency_name,
                'initial_presence_of_wallet_checks': False,
                'wallet_checks_introduced': prev.wallet_detection == 0 and curr.wallet_detection > 0,
                'wallet_checks_increase': prev.wallet_detection < curr.wallet_detection,
                'replaced_crypto_addresses_introduced': prev.replaced_crypto_addresses == 0 and curr.replaced_crypto_addresses > 0,
                'hook_provider_introduced': prev.hook_provider == 0 and curr.hook_provider > 0
            }