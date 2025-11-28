import re
from typing import Dict
from utils import Deobfuscator
class EvasionAnalyzer:
    """Analyze evasion techniques"""

    OBFUSCATION_PATTERNS = {
        r'0x[0-9a-fA-F]+',          # Hexadecimal values, ex. 0x58e7a2
        r'_0x[0-9a-fA-F]+',         # Hexadecimal variables, ex. _0x5f3b1c
        r'\[[\'"]\w+[\'"]\]',       # Property access with array, ex. [push]
        r'\b[a-zA-Z0-9]{1,2}_0x',   # Common prefixes, ex. a0_0x
        r'parseInt\(.*?\)',         # ParseInt with hexadecimals, ex. parseInt(_0x
    }

    def analyze(self, content: str, package_info: Dict) -> Dict:
        
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
        
        is_transformed, transformed_type, suspicious_patterns_count = self._detect_obfuscation(content, package_info['info'])
        if transformed_type == 'Obfuscated' and package_info['file_name'].endswith('.js'):                              # Only deobfuscate JS files
            self.deobfuscate_code(content, package_info['name'], package_info['version'], package_info['file_name'])
        metrics['is_transformed'] = is_transformed
        metrics['transformed_type'] = transformed_type
        metrics['suspicious_patterns_count'] = suspicious_patterns_count
        
        return metrics
    
    def _detect_obfuscation(self, content: str, info: str) -> tuple[bool, str, int]:
        """Detect if code is obfuscated and what type.
            trasformed_type: None, Obfuscated or Deobfuscated (For now)"""

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

        if info == 'deobfuscated':
            return True, "Deobfuscated", len(all_matches)

        if len(all_matches) > 15 and long_lines_count > 0:           # Threshold for obfuscation detection
            return True, "Obfuscated", len(all_matches)

        return False, "none", len(all_matches)
    
    def deobfuscate_code(self, content: str, package_name: str, version: str, file_name: str):
        """Attempt to deobfuscate code"""
        Deobfuscator.deobfuscate(content, package_name, version, file_name)