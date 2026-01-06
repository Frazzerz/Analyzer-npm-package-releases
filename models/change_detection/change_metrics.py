from dataclasses import dataclass
from typing import Optional

@dataclass
class ChangeMetric:
    absolute: Optional[float]
    percentage: Optional[float]

'''
@dataclass
class ChangeMetric:
    """Rappresenta un cambiamento in una metrica tra versioni"""
    current: float
    previous: float
    absolute_change: float
    percentage_change: Optional[float] = None  # None se previous == 0
    is_new: bool = False  # True se introdotto in questa versione
    is_significant: bool = False  # True se supera soglie definite
    
    @classmethod
    def create(cls, current: float, previous: float, 
               significance_threshold: Optional[float] = None) -> 'ChangeMetric':
        """Factory method per creare ChangeMetric con calcoli automatici"""
        absolute_change = current - previous
        percentage_change = (absolute_change / previous * 100) if previous > 0 else None
        is_new = previous == 0 and current > 0
        
        # Calcola is_significant
        is_significant = False
        if significance_threshold is not None:
            if percentage_change is not None:
                is_significant = abs(percentage_change) >= significance_threshold
            else:
                is_significant = absolute_change >= significance_threshold
        
        return cls(
            current=current,
            previous=previous,
            absolute_change=absolute_change,
            percentage_change=percentage_change,
            is_new=is_new,
            is_significant=is_significant
        )
'''