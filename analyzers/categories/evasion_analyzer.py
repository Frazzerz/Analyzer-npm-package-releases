import re
from typing import Dict

class EvasionAnalyzer:
    """Analyze evasion techniques"""

    OBFUSCATION_PATTERNS = {
        r'0x[0-9a-fA-F]+',          # Hexadecimal values, ex. 0x58e7a2
        r'_0x[0-9a-fA-F]+',         # Hexadecimal variables, ex. _0x5f3b1c
        r'\[[\'"]\w+[\'"]\]',       # Property access with array, ex. [push]
        r'\b[a-zA-Z0-9]{1,2}_0x',   # Common prefixes, ex. a0_0x
        r'parseInt\(.*?\)',         # ParseInt with hexadecimals, ex. parseInt(_0x
    }

    def analyze(self, content: str) -> Dict:
        
        metrics = {
            'is_transformed': False,
            'transformed_type': 'none',
            'suspicious_patterns_count': 0,
            'new_code_obfuscated_differently': False,
            'timing_delays': 0,
            'dynamic_imports': 0,
            'env_node_env': 0,
            'env_platform': 0,
            'execution_time': 0,
        }
        
        is_transformed, transformed_type, suspicious_patterns_count = self._detect_obfuscation(content)
        metrics['is_transformed'] = is_transformed
        metrics['transformed_type'] = transformed_type
        metrics['suspicious_patterns_count'] = suspicious_patterns_count
        
        return metrics
    
    def _detect_obfuscation(self, content: str) -> tuple[bool, str, int]:
        """Detect if code is obfuscated and what type.
            trasformed_type: None or Obfuscated (For now)"""
        
        if not content.strip():
            return False, "none", 0

        #Simple heuristic checks for obfuscation
        all_matches = []
        for pattern in EvasionAnalyzer.OBFUSCATION_PATTERNS:
            all_matches.extend(re.findall(pattern, content))
        
        # Check long lines
        long_lines_count = 0
        for line in content.split('\n'):
            if len(line.strip()) > 3000:                            # Threshold for long lines
                long_lines_count += 1

        if len(all_matches) > 15 and long_lines_count > 0:           # Threshold for obfuscation detection
            return True, "obfuscated", len(all_matches)

        return False, "none", len(all_matches)