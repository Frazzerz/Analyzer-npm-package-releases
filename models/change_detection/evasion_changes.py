from dataclasses import dataclass
from .change_metrics import ChangeMetric

@dataclass
class EvasionChanges:
    obfuscated_code_introduced: bool = False
    minified_code_introduced: bool = False
    hex_obfuscation_patterns: ChangeMetric = ChangeMetric(0.0, 0.0)
    platform_detections: ChangeMetric = ChangeMetric(0.0, 0.0)