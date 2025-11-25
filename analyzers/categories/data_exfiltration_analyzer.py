import re
from typing import Dict

class DataExfiltrationAnalyzer:
    """Analyze data exfiltration & command and control techniques"""
    
    '''
    PATTERNS = {
        'tcp_socket': ...,
        'http': ...
    }
    
    SUSPICIOUS_DOMAINS = [
        r'\b(bit\.ly|tinyurl|short\.io|goo\.gl)\b',
        r'\b([0-9]{1,3}\.){3}[0-9]{1,3}\b',  # IP addresses
        r'\b(malicious|suspicious|evil|hack|steal)\.',
    ]
    '''
    def analyze(self, content: str) -> Dict:
        metrics = {                                 # TODO ALL
            'tcp_udp_sockets': 0,
            'http_requests': 0,
            'suspicious_domains': 0,
            'sensitive_file_reads': 0,
            'directory_traversal': 0,
        }
        
        '''
        metrics['tcp_udp_sockets'] = len(re.findall(self.PATTERNS['tcp_socket'], content))
        metrics['http_requests'] = len(re.findall(self.PATTERNS['http'], content))
        ...
        
        for domain_pattern in self.SUSPICIOUS_DOMAINS:
            metrics['suspicious_domains'] += len(re.findall(domain_pattern, content))
        '''

        return metrics