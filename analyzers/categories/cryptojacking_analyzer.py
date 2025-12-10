import re
from typing import Dict, List, Pattern
from utils import UtilsForAnalyzer

class CryptojackingAnalyzer:
    """Analyze cryptojacking & wallet theft techniques"""

    def __init__(self):
        self.REPLACE_CRYPTO_ADDRESS_PATTERN = re.compile(
            # if ( <variable> == 'crypto_symbol' [any optional conditions] ) { [any code] .replace( ...
            r'if\s*\(\s*[^=]+==\s*[\'"](?:' + self.get_all_crypto_symbols() + r')[\'"][^)]*\)\s*\{[^}]*?\.replace\s*\(',
            re.IGNORECASE | re.DOTALL
    )

    CRYPTO_PATTERNS: List[Pattern] = {
        'ethereum': re.compile(r'\b0x[a-fA-F0-9]{40}\b'),
        'bitcoinLegacy': re.compile(r'\b1[a-km-zA-HJ-NP-Z1-9]{25,34}\b'),
        'bitcoinSegwit': re.compile(r'\b(3[a-km-zA-HJ-NP-Z1-9]{25,34}|bc1[qpzry9x8gf2tvdw0s3jn54khce6mua7l]{11,71})\b'),
        #'tron': re.compile(r'((?<!\w)[T][1-9A-HJ-NP-Za-km-z]{33})'),
        'bch': re.compile(r'bitcoincash:[qp][a-zA-Z0-9]{41}'),
        #'ltc': re.compile(r'(?<!\w)ltc1[qpzry9x8gf2tvdw0s3jn54khce6mua7l]{11,71}\b'),
        #'ltc2': re.compile(r'(?<!\w)[mlML][a-km-zA-HJ-NP-Z1-9]{25,34}')
        #'solana': re.compile(r'((?<!\w)[4-9A-HJ-NP-Za-km-z][1-9A-HJ-NP-Za-km-z]{32,44})'),
        #'solana2': re.compile(r'((?<!\w)[3][1-9A-HJ-NP-Za-km-z]{35,44})')
        #'solana3': re.compile(r'((?<!\w)[1][1-9A-HJ-NP-Za-km-z]{35,44})')
        # \b \b word boundaries, find exact word
        # (?<!\w) ensures the preceding character is not a word character
        # [number] specific starting characters (number) for certain crypto addresses
    }

    CRYPTOCURRENCY_NAMES: List[Pattern] = {
        'ethereum': {
            'pattern': re.compile(r'\bethereum\b|\beth\b', re.IGNORECASE),
            'symbols': ['ethereum', 'eth']
        },
        'bitcoin': {
            'pattern': re.compile(r'\bbitcoin\b|\bbtc\b|\bbitcoinLegacy\b|\bbitcoinSegwit\b', re.IGNORECASE),
            'symbols': ['bitcoin', 'btc', 'bitcoinLegacy', 'bitcoinSegwit']
        },
        'tron': {
            'pattern': re.compile(r'\btron\b|\btrx\b', re.IGNORECASE),
            'symbols': ['tron', 'trx']
        },
        'bitcoin-cash': {
            'pattern': re.compile(r'\bbitcoin[-\s]?cash\b|\bbch\b', re.IGNORECASE),
            'symbols': ['bitcoin-cash', 'bch']
        },
        'litecoin': {
            'pattern': re.compile(r'\blitecoin\b|\bltc\b|\bltc2\b', re.IGNORECASE),
            'symbols': ['litecoin', 'ltc', 'ltc2']
        },
        'solana': {
            'pattern': re.compile(r'\bsolana\b|\bsol\b|\bsolana2\b|\bsolana3\b', re.IGNORECASE),
            'symbols': ['solana', 'sol', 'solana2', 'solana3']
        }
    }

    WALLET_DETECTION_PATTERNS: List[Pattern] = {
        'metamask_installed': re.compile(
            r'(typeof\s*window\s*!==?\s*[\'"]undefined[\'"])'
            r'|'
            r'(typeof\s*window\.ethereum\s*!==?\s*[\'"]undefined[\'"])'
            r'|'
            r'(ethereum\.isMetaMask)',
            re.IGNORECASE
        ),
        'wallet_connect_detect': re.compile(
            r'(window\.)?ethereum\.request',
            re.IGNORECASE
        ), 
        # variable spaces: \s+ (at least one space), \s* (zero or more spaces)
        # ['"] can be either single or double quotes
        # !==? -> != and !==
        # ()? is optional group
    }

    # eth_sendTransaction, solana_signTransaction, solana_signAndSendTransaction are functions used to send crypto to someone, sign operations on dApps and authorize smart contracts
    # an attacker can hook these functions to modify the destination address to his own address
    HOOK_PROVIDER_PATTERN: List[Pattern] = re.compile(r'\b(eth_sendTransaction|solana_signTransaction|solana_signAndSendTransaction)\b', re.IGNORECASE)

    def analyze(self, content: str) -> Dict:
        
        metrics = {
            'crypto_addresses': 0,
            'list_crypto_addresses': [],
            'wallet_detection': 0,
            'cryptocurrency_name': 0,
            'replaced_crypto_addresses': 0,
            'hook_provider': 0
        }

        metrics['crypto_addresses'], metrics['list_crypto_addresses'] = UtilsForAnalyzer.detect_patterns(content, list(self.CRYPTO_PATTERNS.values()))
        metrics['cryptocurrency_name'] = UtilsForAnalyzer.detect_count_patterns(content, [data['pattern'] for data in self.CRYPTOCURRENCY_NAMES.values()])
        metrics['wallet_detection'] = UtilsForAnalyzer.detect_count_patterns(content, list(self.WALLET_DETECTION_PATTERNS.values()))

        # Mechanism present in the malware considered :
        #   Intercepts all HTTP responses (fetch/XMLHttpRequest) and replaces the cryptographic addresses found in the content with those controlled by the attacker
        # Check presence of cryptocurrency name and .replace function could indicate address substitution
        metrics['replaced_crypto_addresses'] = UtilsForAnalyzer.detect_count_patterns(content, [self.REPLACE_CRYPTO_ADDRESS_PATTERN])
        metrics['hook_provider'] = UtilsForAnalyzer.detect_count_patterns(content, [self.HOOK_PROVIDER_PATTERN])

        return metrics

    def get_all_crypto_symbols(self):
        """Get all cryptocurrency symbols as a regex pattern"""
        all_symbols = []
        for crypto_data in self.CRYPTOCURRENCY_NAMES.values():
            all_symbols.extend(crypto_data['symbols'])
        # Escape special symbols for regex and join with |
        escaped_symbols = [re.escape(symbol) for symbol in all_symbols]
        return '|'.join(escaped_symbols)