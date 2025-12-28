import re
from typing import Dict, List, Pattern
from utils import UtilsForAnalyzer

class DataExfiltrationAnalyzer:
    """Analyze data exfiltration & command and control techniques"""
    
    SCAN_FUNCTIONS_PATTERNS: List[Pattern] = [
        re.compile(r'(\w+)\.(get)?homedir\s*\(?\s*\)?\s*', re.IGNORECASE),
        re.compile(r'(\w+)\.((?:read(?:dir|file)|scanfilesystem)(?:sync)?)\s*\(([^;]*);', re.IGNORECASE)
        # os.homedir() Gets the home directory and is base, gethomedir() is custom wrapper function
        # readdirsync reads the content of a directory
        # scanFileSystem is custom function
        # readFileSync reads the content of a file
        # statSync reads the metadata of a file or folder and returns a fs.Stats object. It can be used later to do e.g. stats.isFile()
    ]

    SCANNED_ELEMENTS_PATTERNS: List[Pattern] = [
        #re.compile(r'\w*[_-]?\.?host[-_]?name\.?[_-]?\w*', re.IGNORECASE),                                                 # Hostname
        #re.compile(r'\w*[_-]?\.?userinfo\.?[_-]?\w*', re.IGNORECASE),                                                      # Userinfo
        #re.compile(r'\w*[-_]?\.?(ssh|aws|secret|access|token)s?\.?[-_]?\w*', re.IGNORECASE),                               # Ssh Aws Secret Access Token
        #re.compile(r'\w*[_-]?\.?database\.?[_-]?\w*', re.IGNORECASE),                                                      # Database
        #re.compile(r'\w*[_-]?\.?google\.?[_-]?\w*', re.IGNORECASE),                                                        # Google
        #re.compile(r'\w*[_-]?api[_-]?key[s]?\w*', re.IGNORECASE),                                                          # API Key
        #re.compile(r'(\w*)?\.env((\.)?\w*)?', re.IGNORECASE),                                                              # Env
        #re.compile(r'(\w*)?(\.)?username[s]?((\.)?\w*)?', re.IGNORECASE),                                                  # Username
        #re.compile(r'(\w*)?(\.)?[e]?[-]?mail[s]?((\.)?\w*)?', re.IGNORECASE),                                              # Email
        #re.compile(r'(\w*)?(\.)?(password|passphrase)s?((\.)?\w*)?', re.IGNORECASE),                                       # Password or Passphrase
        
        # Hostname, Userinfo, Ssh, Aws, Secret, Access, Token, Database, Google, API Key, Env, Username, Email, Password, Passphrase
        # No more Client Auth Private env
        # 10033 e 15969
        #re.compile(r'\w*[._-]?(?:host[-_]?name|userinfo|(?:ssh|aws|secret|access|token)s?|database|google|api[-_]?keys?usernames?|[e]?[-]?mails?|(?:pass(word|phrase))s?)[._-]?\w*', re.IGNORECASE),
        
        # [] indicate character set
        # () capturing group
        # \w alphanumeric character or underscore. This allows for characters attached to “access”
        # password, passphrase, secret, token, apikey, awssecret, sshkey, privatekeys, database/google/aws+password/secret/key
        re.compile(
            r'(?<![A-Za-z0-9-])(?:'
            r'passwords?|passphrases?|'
            r'secrets?|access[-_]?tokens?|'
            r'api[-_]?keys?|aws[-_]?secrets?|'
            r'ssh[-_]?keys?|private[-_]?keys?|'
            r'(?:database|google|aws)[-_]?(?:password|secret|key)'
            r')(?![A-Za-z0-9])',
            re.IGNORECASE
        ),
    ]

    DATA_TRANSMISSION_PATTERNS: List[Pattern] = [
        re.compile(r'(\w+)\.(post|get|put|delete|request)\s*\(\s*[\'"]?(https?:\/\/[^\s\'"]+)[\'"]?', re.IGNORECASE),   # http methods
        re.compile(r'new\s+WebSocket\s*\(\s*[\'"]?(wss?:\/\/[^\s\'"]+)[\'"]?', re.IGNORECASE),                          # WebSocket connections
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

        if not content:
            return metrics

        metrics['scan_functions_count'],  metrics['list_scan_functions'] = UtilsForAnalyzer.detect_patterns(content, self.SCAN_FUNCTIONS_PATTERNS)
        metrics['sensitive_elements_count'], metrics['list_sensitive_elements'] = UtilsForAnalyzer.detect_patterns(content, self.SCANNED_ELEMENTS_PATTERNS)
        metrics['data_transmission_count'], metrics['list_data_transmission'] = UtilsForAnalyzer.detect_patterns(content, self.DATA_TRANSMISSION_PATTERNS)
        return metrics