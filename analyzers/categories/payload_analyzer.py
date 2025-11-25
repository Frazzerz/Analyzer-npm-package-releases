from typing import Dict

class PayloadAnalyzer:
    """Analyze payload delivery and execution techniques"""
    
    '''
    PATTERNS = {
        'eval': ...,
        'shell': ...',
    }
    '''
    
    def analyze(self, content: str) -> Dict:
        metrics = {
            'eval': 0,                                              # TODO
            'shell_commands': 0,                                    # TODO
            'file_or_executable_inside_pkg': 0,                     # TODO
            'file_size_bytes': len(content.encode('utf-8')),
            'suspicious_dependencies_few_downloads': 0,             # TODO
            'suspicious_dependencies_just_created': 0,              # TODO
            'suspicious_dependencies_typesquatted': 0               # TODO
        }
        
        '''
        metrics['eval'] = len(re.findall(self.PATTERNS['eval'], content))
        ...
        '''

        return metrics