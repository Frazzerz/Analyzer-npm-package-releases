from dataclasses import dataclass
from .change_metrics import ChangeMetric

@dataclass
class CryptoChanges:
    crypto_addresses: ChangeMetric = ChangeMetric(0.0, 0.0)
    change_crypto_addresses: bool = False
    cryptocurrency_name: ChangeMetric = ChangeMetric(0.0, 0.0)
    wallet_checks: ChangeMetric = ChangeMetric(0.0, 0.0)
    replaced_crypto_addresses: ChangeMetric = ChangeMetric(0.0, 0.0)
    hook_provider: ChangeMetric = ChangeMetric(0.0, 0.0)