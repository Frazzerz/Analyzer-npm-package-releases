import re
from typing import Dict

class DataExfiltrationAnalyzer:
    """Analyze data exfiltration & command and control techniques"""
    
    SCAN_FUNCTIONS_PATTERNS = [
        re.compile(r'(\w+)\.(get)?homedir\s*\(?\s*\)?\s*', re.IGNORECASE),
        re.compile(r'(\w+)\.(readdirsync|scanfilesystem|scanfs)\s*\(([^;]*);', re.IGNORECASE),
        re.compile(r'(\w+)\.(readfile(sync)?)\s*\(([^;]*);', re.IGNORECASE),
        re.compile(r'\w*\.arch\s*\(\s*\)', re.IGNORECASE),
        # .arch() returns the CPU architecture of the operating system on which Node.js is running
        # os.homedir() Gets the home directory and is base, gethomedir() is custom wrapper function
        # readdirsync reads the content of a directory
        # scanFileSystem is custom function
        # readFileSync reads the content of a file
        # statSync reads the metadata of a file or folder and returns a fs.Stats object. It can be used later to do e.g. stats.isFile()
    ]

    SCANNED_ELEMENTS_PATTERNS = [
        re.compile(r'\w*[_-]?\.?host[-_]?name\.?[_-]?\w*', re.IGNORECASE),                                                 # Hostname
        re.compile(r'\w*[_-]?\.?userinfo\.?[_-]?\w*', re.IGNORECASE),                                                      # Userinfo
        # Ssh Aws Secret Client Access Token Auth Private
        re.compile(r'\w*[-_]?\.?(ssh|aws|secret|client|access|token|auth|private)s?\.?[-_]?\w*', re.IGNORECASE),
        re.compile(r'\w*[_-]?\.?database\.?[_-]?\w*', re.IGNORECASE),                                                      # Database
        re.compile(r'\w*[_-]?\.?google\.?[_-]?\w*', re.IGNORECASE),                                                        # Google
        re.compile(r'\w*[_-]?api[_-]?key[s]?\w*', re.IGNORECASE),                                                          # API Key
        re.compile(r'(\w*)?\.env((\.)?\w*)?', re.IGNORECASE),                                                              # Env
        re.compile(r'(\w*)?(\.)?username[s]?((\.)?\w*)?', re.IGNORECASE),                                                  # Username
        re.compile(r'(\w*)?(\.)?[e]?[-]?mail[s]?((\.)?\w*)?', re.IGNORECASE),                                              # Email
        re.compile(r'(\w*)?(\.)?(password|passphrase)s?((\.)?\w*)?', re.IGNORECASE),                                     # Password or Passphrase
        # [] indicate character set
        # () capturing group
        # \w alphanumeric character or underscore. This allows for characters attached to “access”
    ]

    def analyze(self, content: str) -> Dict:
        metrics = {
            'scan_functions_count': 0,
            'list_scan_functions': [],
            'sensitive_elements_count': 0,
            'list_sensitive_elements': [],
            'data_transmission_count': 0,
            'list_data_transmission': [],
        }

        scan_functions_count, list_scan_functions = self.detect_scan_functions(content)
        metrics['scan_functions_count'] = scan_functions_count
        metrics['list_scan_functions'] = list_scan_functions
        
        sensitive_elements_count, list_sensitive_elements = self.detect_scanned_elements(content)
        metrics['sensitive_elements_count'] = sensitive_elements_count
        metrics['list_sensitive_elements'] = list_sensitive_elements
        
        return metrics
    
    def detect_scan_functions(self, content: str) -> tuple[int, list[str]]:
        matches = []
        for pattern in DataExfiltrationAnalyzer.SCAN_FUNCTIONS_PATTERNS:
            for match in pattern.finditer(content):
                matches.append(match.group(0))
        return len(matches), matches
    
    def detect_scanned_elements(self, content: str) -> tuple[int, list[str]]:
        matches = []
        for pattern in DataExfiltrationAnalyzer.SCANNED_ELEMENTS_PATTERNS:
           for match in pattern.finditer(content):
            matches.append(match.group(0))
        return len(matches), matches