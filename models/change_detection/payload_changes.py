from dataclasses import dataclass
from .change_metrics import ChangeMetric

@dataclass
class PayloadChanges:
    timing_delays: ChangeMetric = ChangeMetric(0.0, 0.0)
    eval_function: ChangeMetric = ChangeMetric(0.0, 0.0)
    shell_commands: ChangeMetric = ChangeMetric(0.0, 0.0)
    preinstall_scripts_introduced: bool = False
    preinstall_scripts_change: bool = False