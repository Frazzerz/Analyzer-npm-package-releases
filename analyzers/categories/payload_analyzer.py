import re
from typing import Dict, List, Pattern
from utils import UtilsForAnalyzer
class PayloadAnalyzer:
    """Analyze payload delivery and execution techniques"""
    
    TIMING_DELAYS_PATTERNS: List[Pattern] = [
        # await new Promise( (resolve) => { setTimeout( resolve, 1000); } );
        re.compile(r'await\s+new\s+Promise\s*\(\s*(\w+)\s*=>\s*\{?\s*[\s\S]*?setTimeout\w*\s*\(\s*\1[\s\S]*?\}?\s*\)', re.IGNORECASE),
        # (\w+) capture the variable name (resolve)
        # \w* zero or more alphanumeric characters (or underscore)
        # [\s\S] any character (space or non-space). Used to match newlines as well
        # *? Non-greedy quantifier (takes the minimum necessary), stop as soon as you find setTimeout, do not take the following ones
        # \1 Backreference to the captured variable (resolve)
        # ?: Indicates a non-capturing group (returns the entire match, not just the group)
    ]
    
    EVAL_PATTERNS: List[Pattern] = [
        re.compile(r'eval\s*\([\s\S]*?\)'),
    ]
    
    SHELL_COMMANDS_PATTERNS: List[Pattern] = [
        # obj.exec(command, args)
        re.compile(r'(\w+)?.?exec\s*\(\s*(\w+)\s*,\s*(\w+)\s*\)', re.IGNORECASE),
        # Bun is a JavaScript runtime similar to Node.js, and it has a function to execute system commands
        # await Bun.$`command`
        re.compile(r'(\w+)?\s*Bun\.\$\s*\`[\s\S]*?\`', re.IGNORECASE),
        # Not to be confused with RegExp.exec(), which is a method for searching for patterns in a string
    ]

    PREINSTALL_PATTERNS: List[Pattern] = [
        re.compile(r'"preinstall"\s*:\s*"[^"]*"\s*,?', re.IGNORECASE),
        # [^"]*  Any text between quotes
    ]

    def analyze(self, content: str, file_diff_additions: list[str]) -> Dict:
        metrics = {
            'timing_delays_count': 0,
            'list_timing_delays': [],
            'eval_count': 0,
            'eval_list': [],
            'shell_commands_count': 0,
            'list_shell_commands': [],
            'file_size_bytes': len(content.encode('utf-8')),
            'preinstall_scripts_count': 0,
            'list_preinstall_scripts': [],
            'presence_of_suspicious_dependency': 0,
        }
        
        metrics['timing_delays_count'], metrics['list_timing_delays'] = UtilsForAnalyzer.detect_patterns(content, self.TIMING_DELAYS_PATTERNS)
        metrics['eval_count'], metrics['eval_list'] = UtilsForAnalyzer.detect_patterns(content, self.EVAL_PATTERNS)
        metrics['shell_commands_count'], metrics['list_shell_commands'] = UtilsForAnalyzer.detect_patterns(content, self.SHELL_COMMANDS_PATTERNS)
        if len(file_diff_additions) > 0:
            metrics['preinstall_scripts_count'], metrics['list_preinstall_scripts'] = UtilsForAnalyzer.detect_patterns('\n'.join(file_diff_additions), self.PREINSTALL_PATTERNS)

        return metrics