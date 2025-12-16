import re
from typing import Dict, List, Pattern
from utils import Deobfuscator
from utils import UtilsForAnalyzer
class EvasionAnalyzer:
    """Analyze evasion techniques"""

    OBFUSCATION_PATTERNS: List[Pattern] = [
        re.compile(r'_?0x[0-9a-fA-F]{6,}'),                                                   # Hexadecimal values and variables (at least 6 hex values), ex. 0x58e7a2 or _0x5f3b1c
        re.compile(r'parseInt\(_?0x[0-9a-fA-F]{6,}', re.IGNORECASE),                          # ParseInt with hexadecimals, ex. parseInt(0x58e7a2
        re.compile(r'try\{.*?\}catch\(_?0x[0-9a-fA-F]{6,}\)', re.IGNORECASE),                 # Try-catch blocks with obfuscated vars, ex. try{...}catch(_0x5f3b1c)
        re.compile(r'const\s+_?0x[0-9a-fA-F]{6,}\s*=\s*_?0x[0-9a-fA-F]{6,}', re.IGNORECASE),  # Constant assignments with obfuscated names, ex. const _0x5f3b1c = _0x5f3b1d 
        re.compile(r'_?0x[0-9a-fA-F]{6,}\(_?0x[0-9a-fA-F]{6,}'),                              # Function calls with hex parameters, ex. _0x5f3b1c(0x58e7a2
        # 3281-12-8-38-17
        # \s for spaces
        # + at least one
        # * zero or more
        # ? facoltative
        # . matches any character except newline
        # re.IGNORECASE for case insensitive, re.DOTALL to match newlines  
    ]

    PLATFORM_PATTERNS: List[Pattern] = [
        # process.platform() == 'win32'  platform === "linux"
        # .arch() returns the CPU architecture of the operating system on which Node.js is running
        re.compile(
            r'(?:'
            r'(\w+\.)?platform\(?\)?\s*[!=]==?\s*[\'"](?:win(?:32|64|dows)?|linux|darwin|mac(?:os)?)[\'"]|'
            r'\w*\.arch\s*\(\s*\)'
            r')',
            re.IGNORECASE
        ),
        # [!=]==? -> ==, ===, !=, !==
        # \' for escape
        # darwin  macOS
        # (?:...) non-capturing group, best performance, do not allocate memory to capture the group
    ]

    def analyze(self, content: str, package_info: Dict) -> Dict:
        metrics = {
            'code_type': 'None',
            'suspicious_patterns_count': 0,
            'list_suspicious_patterns': [],
            'longest_line_length': 0,
            'blank_space_and_character_ratio': 0.0,
            'platform_detections_count': 0,
            'list_platform_detections': []
        }

        if not content:
            return metrics
        
        metrics['suspicious_patterns_count'], metrics['list_suspicious_patterns'] = UtilsForAnalyzer.detect_patterns(content, self.OBFUSCATION_PATTERNS)
        metrics['platform_detections_count'], metrics['list_platform_detections'] = UtilsForAnalyzer.detect_patterns(content, self.PLATFORM_PATTERNS)
        metrics['longest_line_length'] = max(len(r) for r in content.splitlines()) if content.splitlines() else 0
        metrics['blank_space_and_character_ratio'] = content.count(' ') / len(content) if content else 0.0
        no_empty_lines = len([r for r in content.splitlines() if r.strip()])

        if (package_info['info'] == 'deobfuscated'):
            code_type = 'Deobfuscated'
        elif (self._detect_obfuscated_code(metrics['suspicious_patterns_count'], metrics['longest_line_length'])):
            code_type = 'Obfuscated'
        elif (self._detect_minified_code(no_empty_lines, metrics['blank_space_and_character_ratio'], metrics['longest_line_length'])):
            code_type = 'Minified'
        else:
            code_type = 'Clear'
        metrics['code_type'] = code_type        

        if code_type == 'Obfuscated' and package_info['file_name'].endswith('.js'):                              # Only deobfuscate JS files
            self.deobfuscate_code(content, package_info['name'], package_info['version'], package_info['file_name'])
        return metrics
    
    @staticmethod
    def _detect_obfuscated_code(suspicious_patterns_count: int, longest_line_length: int) -> bool:
        """Detect if code is obfuscated"""
        #Simple heuristic checks for obfuscation
        return suspicious_patterns_count > 15 and longest_line_length > 30000           # Thresholds for obfuscation detection
    
    @staticmethod
    def _detect_minified_code(no_empty_lines: int, blank_space_and_character_ratio: float, longest_line_length: int) -> bool:
        """Detect if code is minified"""
        # Simple heuristic checks for minification
        return blank_space_and_character_ratio < 0.03 and no_empty_lines < 3 and longest_line_length > 100        # Thresholds for minification detection

    def deobfuscate_code(self, content: str, package_name: str, version: str, file_name: str):
        """Attempt to deobfuscate code"""
        Deobfuscator.deobfuscate(content, package_name, version, file_name)

    def deminify_code(self, content: str, package_name: str, version: str, file_name: str):
        """Attempt to deminify code"""
        # TODO ?