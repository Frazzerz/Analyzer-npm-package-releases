from typing import Dict
from models import VersionMetrics, AggregateVersionMetrics

class CryptojackingComparator:
    """Compare cryptojacking & wallet theft metrics between versions (tags) to identify flags"""
    
    def compare(self, prev_tag_metrics: VersionMetrics, curr_tag_metrics: VersionMetrics, all_prev_tag_metrics: AggregateVersionMetrics) -> Dict:
        
        if prev_tag_metrics.version == "":
            # No comparison for first version - return no flags
            return {
                'crypto_addresses_introduced': False,
                'crypto_addresses_increase': False,
                'change_crypto_addresses': False,
                'cryptocurrency_name_introduced': False,
                'cryptocurrency_name_increase': False,
                'wallet_checks_introduced': False,
                'wallet_checks_increase': False,
                'replaced_crypto_addresses_introduced': False,
                'hook_provider_introduced': False
            }
        else:
            prev_crypto = prev_tag_metrics.crypto_addresses
            curr_crypto = curr_tag_metrics.crypto_addresses

            prev_list_crypto = prev_tag_metrics.list_crypto_addresses
            curr_list_crypto = curr_tag_metrics.list_crypto_addresses

            prev_cryptocurrency = prev_tag_metrics.cryptocurrency_name
            curr_cryptocurrency = curr_tag_metrics.cryptocurrency_name

            prev_wallet = prev_tag_metrics.wallet_detection
            curr_wallet = curr_tag_metrics.wallet_detection

            prev_replaced = prev_tag_metrics.replaced_crypto_addresses
            curr_replaced = curr_tag_metrics.replaced_crypto_addresses

            prev_hook = prev_tag_metrics.hook_provider
            curr_hook = curr_tag_metrics.hook_provider

            return {
                'crypto_addresses_introduced': prev_crypto == 0 and curr_crypto > 0,
                'crypto_addresses_increase': prev_crypto < curr_crypto,
                'change_crypto_addresses': prev_crypto == curr_crypto and prev_list_crypto != curr_list_crypto and prev_crypto > 0,
                'cryptocurrency_name_introduced': prev_cryptocurrency == 0 and curr_cryptocurrency > 0,
                'cryptocurrency_name_increase': prev_cryptocurrency < curr_cryptocurrency,
                'wallet_checks_introduced': prev_wallet == 0 and curr_wallet > 0,
                'wallet_checks_increase': prev_wallet < curr_wallet,
                'replaced_crypto_addresses_introduced': prev_replaced == 0 and curr_replaced > 0,
                'hook_provider_introduced': prev_hook == 0 and curr_hook > 0
            }