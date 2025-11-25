from typing import Dict
from models import FileMetrics

class DataExfiltrationComparator:
    """Compare data exfiltration & command and control metrics to identify red flags"""
    
    def compare(self, prev: FileMetrics, curr: FileMetrics) -> Dict:
        
        # New file
        if prev is None:
            return {
                'tcp_udp_introduced': curr.tcp_udp_sockets > 0,                                                              #TODO ALL, placeholder
                'http_requests_introduced': curr.http_requests > 0,
                'suspicious_domains_introduced': curr.suspicious_domains > 0,
                'sensitive_reads_introduced': curr.sensitive_file_reads > 0,
                'directory_traversal_introduced': curr.directory_traversal > 0,
            }
        else:
            # Existing file
            return {
                'tcp_udp_introduced': (prev.tcp_udp_sockets == 0 and curr.tcp_udp_sockets > 0),                              #TODO ALL, placeholder
                'http_requests_introduced': (prev.http_requests == 0 and curr.http_requests > 0),
                'suspicious_domains_introduced': (prev.suspicious_domains == 0 and curr.suspicious_domains > 0),
                'sensitive_reads_introduced': (prev.sensitive_file_reads == 0 and curr.sensitive_file_reads > 0),
                'directory_traversal_introduced': (prev.directory_traversal == 0 and curr.directory_traversal > 0),
            }