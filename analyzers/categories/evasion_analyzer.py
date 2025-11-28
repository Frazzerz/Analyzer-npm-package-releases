import re
from typing import Dict
from utils import Deobfuscator
from pathlib import Path
class EvasionAnalyzer:
    """Analyze evasion techniques"""

    OBFUSCATION_PATTERNS = {
        r'_?0x[0-9a-fA-F]{6,}',                                         # Hexadecimal values and variables (at least 6 hex values), ex. 0x58e7a2 or _0x5f3b1c
        r'parseInt\(_?0x[0-9a-fA-F]{6,}',                               # ParseInt with hexadecimals, ex. parseInt(0x58e7a2
        r'try\{.*?\}catch\(_?0x[0-9a-fA-F]{6,}\)',                      # Try-catch blocks with obfuscated vars, ex. try{...}catch(_0x5f3b1c)
        r'const\s+_?0x[0-9a-fA-F]{6,}\s*=\s*_?0x[0-9a-fA-F]{6,}',       # Constant assignments with obfuscated names, ex. const _0x5f3b1c = _0x5f3b1d 
        r'_?0x[0-9a-fA-F]{6,}\(_?0x[0-9a-fA-F]{6,}',                    # Function calls with hex parameters, ex. _0x5f3b1c(0x58e7a2
        # \s for spaces
        # + at least one
        # * zero or more
        # ? facoltative
    }

    def analyze(self, content: str, package_info: Dict) -> Dict:
        
        metrics = {
            'is_transformed': False,
            'transformed_type': 'none',
            'suspicious_patterns_count': 0,
            'list_suspicious_patterns': [],
            'longest_line_length': 0,
            'new_code_obfuscated_differently': False,
            'timing_delays': 0,
            'dynamic_imports': 0,
            'env_node_env': 0,
            'env_platform': 0,
            'execution_time': 0,
        }
        
        is_transformed, transformed_type, suspicious_patterns_count, list_suspicious_patterns, longest_line_length = self._detect_obfuscation(content, package_info['info'])
        if transformed_type == 'Obfuscated' and package_info['file_name'].endswith('.js'):                              # Only deobfuscate JS files
            self.deobfuscate_code(content, package_info['name'], package_info['version'], package_info['file_name'])
        metrics['is_transformed'] = is_transformed
        metrics['transformed_type'] = transformed_type
        metrics['suspicious_patterns_count'] = suspicious_patterns_count
        metrics['list_suspicious_patterns'] = list_suspicious_patterns
        metrics['longest_line_length'] = longest_line_length
        
        return metrics
    
    def _detect_obfuscation(self, content: str, info: str) -> tuple[bool, str, int, list, int]:
        """Detect if code is obfuscated and what type.
            trasformed_type: None, Obfuscated or Deobfuscated (For now)"""

        if not content.strip():
            return False, "none", 0, [], 0

        #Simple heuristic checks for obfuscation
        all_matches = []
        for pattern in EvasionAnalyzer.OBFUSCATION_PATTERNS:
            all_matches.extend(re.findall(pattern, content))
        
        # Check number of lines longer than 30000 characters, remove spaces
        long_lines_count = [r for r in content.splitlines() if len(r.replace(' ', '')) > 30000]         # Threshold for long lines
        longest_line_length = max(len(r.replace(' ', '')) for r in content.splitlines()) if content.splitlines() else 0

        if info == 'deobfuscated':
            return True, "Deobfuscated", len(all_matches), all_matches, longest_line_length

        if len(all_matches) > 15 and len(long_lines_count) > 0:                                         # Threshold for obfuscation detection
            return True, "Obfuscated", len(all_matches), all_matches, longest_line_length

        return False, "none", len(all_matches), all_matches, longest_line_length
    
    def deobfuscate_code(self, content: str, package_name: str, version: str, file_name: str):
        """Attempt to deobfuscate code"""
        Deobfuscator.deobfuscate(content, package_name, version, file_name)