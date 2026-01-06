from dataclasses import dataclass
from .change_metrics import ChangeMetric

@dataclass
class GenericChanges:
    total_files: ChangeMetric = ChangeMetric(0.0, 0.0)
    size_bytes: ChangeMetric = ChangeMetric(0.0, 0.0)
    weighted_avg_blank_space_and_character_ratio: ChangeMetric = ChangeMetric(0.0, 0.0)
    weighted_avg_shannon_entropy: ChangeMetric = ChangeMetric(0.0, 0.0)
    longest_line_length: ChangeMetric = ChangeMetric(0.0, 0.0)