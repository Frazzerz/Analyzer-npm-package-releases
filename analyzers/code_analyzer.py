from typing import Dict
from .categories import EvasionAnalyzer, PayloadAnalyzer, DataExfiltrationAnalyzer, CryptojackingAnalyzer

class CodeAnalyzer:
    """Coordinates analysis across all categories"""
    
    def __init__(self):
        self.evasion_analyzer = EvasionAnalyzer()
        self.payload_analyzer = PayloadAnalyzer()
        self.data_exfiltration_analyzer = DataExfiltrationAnalyzer()
        self.cryptojacking_analyzer = CryptojackingAnalyzer()

    def analyze_file(self, content: str, package_info: Dict) -> Dict:
        """Analyze a single file and return all metrics"""
        metrics = {}
        
        metrics.update(self.evasion_analyzer.analyze(content, package_info))
        metrics.update(self.payload_analyzer.analyze(content, package_info))
        metrics.update(self.data_exfiltration_analyzer.analyze(content))
        metrics.update(self.cryptojacking_analyzer.analyze(content))
        
        return metrics