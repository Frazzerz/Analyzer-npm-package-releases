from dataclasses import dataclass
from .change_metrics import ChangeMetric

@dataclass
class ExfiltrationChanges:
    scan_functions: ChangeMetric = ChangeMetric(0.0, 0.0)
    sensitive_elements: ChangeMetric = ChangeMetric(0.0, 0.0)
    data_transmission: ChangeMetric = ChangeMetric(0.0, 0.0)