import re
from typing import Dict
from utils import Deobfuscator
class EvasionAnalyzer:
    """Analyze evasion techniques"""

    OBFUSCATION_PATTERNS = [
        re.compile(r'_?0x[0-9a-fA-F]{6,}'),                                                   # Hexadecimal values and variables (at least 6 hex values), ex. 0x58e7a2 or _0x5f3b1c
        re.compile(r'parseInt\(_?0x[0-9a-fA-F]{6,}', re.IGNORECASE),                          # ParseInt with hexadecimals, ex. parseInt(0x58e7a2
        re.compile(r'try\{.*?\}catch\(_?0x[0-9a-fA-F]{6,}\)', re.IGNORECASE),                 # Try-catch blocks with obfuscated vars, ex. try{...}catch(_0x5f3b1c)
        re.compile(r'const\s+_?0x[0-9a-fA-F]{6,}\s*=\s*_?0x[0-9a-fA-F]{6,}', re.IGNORECASE),  # Constant assignments with obfuscated names, ex. const _0x5f3b1c = _0x5f3b1d 
        re.compile(r'_?0x[0-9a-fA-F]{6,}\(_?0x[0-9a-fA-F]{6,}'),                              # Function calls with hex parameters, ex. _0x5f3b1c(0x58e7a2
        # \s for spaces
        # + at least one
        # * zero or more
        # ? facoltative
        # . matches any character except newline
        # re.IGNORECASE for case insensitive, re.DOTALL to match newlines  
    ]

    PLATFORM_PATTERNS = [
        # process.platform() == 'win32'  platform === "linux"
        re.compile(
            r'(\w+\.)?platform\(?\)?\s*[!=]==?\s*[\'"](win(32|64|dows)?|linux|darwin|mac(os)?)[\'"]',
            re.IGNORECASE
            ),
        # [!=]==? -> ==, ===, !=, !==
        # \' for escape
        # darwin  macOS
    ]

    def analyze(self, content: str, package_info: Dict, file_diff_additions: list[str]) -> Dict:
        metrics = {
            'is_transformed': False,
            'transformed_type': 'none',
            'suspicious_patterns_count': 0,
            'list_suspicious_patterns': [],
            'longest_line_length': 0,
            'new_code_transformed_type': 'none',
            'platform_detections_count': 0,
            'list_platform_detections': [],
            'concatenated_elements_count': 0,
            'list_concatenated_elements': [],
        }
        
        is_transformed, transformed_type, suspicious_patterns_count, list_suspicious_patterns, longest_line_length = self._detect_obfuscation(content, package_info['info'])
        if transformed_type == 'Obfuscated' and package_info['file_name'].endswith('.js'):              # Only deobfuscate JS files
            self.deobfuscate_code(content, package_info['name'], package_info['version'], package_info['file_name'])
        metrics['is_transformed'] = is_transformed
        metrics['transformed_type'] = transformed_type
        metrics['suspicious_patterns_count'] = suspicious_patterns_count
        metrics['list_suspicious_patterns'] = list_suspicious_patterns
        metrics['longest_line_length'] = longest_line_length

        new_code_transformed_type = self._detect_obfuscation_diff('\n'.join(file_diff_additions))       # "line1\nline2\nline3"
        metrics['new_code_transformed_type'] = new_code_transformed_type    

        metrics['platform_detections_count'], metrics['list_platform_detections'] = self.platform_detection(content)

        return metrics
    
    def _detect_obfuscation(self, content: str, info: str) -> tuple[bool, str, int, list, int]:
        """Detect if code is obfuscated and what type.
            trasformed_type: Clear, Obfuscated, Deobfuscated or none (For now)
            return if is_transformed, transformed_type, suspicious_patterns_count, list_suspicious_patterns, longest_line_length"""

        if not content.strip():
            return False, "none", 0, [], 0  # Empty content

        #Simple heuristic checks for obfuscation
        all_matches = []
        for pattern in EvasionAnalyzer.OBFUSCATION_PATTERNS:
            all_matches.extend(pattern.findall(content))
        
        # Check number of lines longer than 30000 characters, remove spaces
        long_lines_count = [r for r in content.splitlines() if len(r.replace(' ', '')) > 30000]         # Threshold for long lines
        longest_line_length = max(len(r.replace(' ', '')) for r in content.splitlines()) if content.splitlines() else 0

        if info == 'deobfuscated':
            return True, "Deobfuscated", len(all_matches), all_matches, longest_line_length

        if len(all_matches) > 15 and len(long_lines_count) > 0:                                         # Threshold for obfuscation detection
            return True, "Obfuscated", len(all_matches), all_matches, longest_line_length

        return False, "Clear", len(all_matches), all_matches, longest_line_length
    
    def _detect_obfuscation_diff(self, diff_content: str) -> str:
        _, transformed_type, _, _, _ = self._detect_obfuscation(diff_content, 'Diff')                   # Diff is not used for now
        return transformed_type

    def deobfuscate_code(self, content: str, package_name: str, version: str, file_name: str):
        """Attempt to deobfuscate code"""
        Deobfuscator.deobfuscate(content, package_name, version, file_name)

    def platform_detection(self, content: str) -> tuple[int, list[str]]:
        matches = []
        for pattern in EvasionAnalyzer.PLATFORM_PATTERNS:
            for match in pattern.finditer(content):
                matches.append(match.group(0))
        return len(matches), matches