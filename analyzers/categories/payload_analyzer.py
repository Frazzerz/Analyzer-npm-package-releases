import re
from typing import Dict
class PayloadAnalyzer:
    """Analyze payload delivery and execution techniques"""
    
    TIMING_DELAYS_PATTERNS = [
        # await new Promise( (resolve) => { setTimeout( resolve, 1000); } );
        re.compile(r'await\s+new\s+Promise\s*\(\s*(\w+)\s*=>\s*\{?\s*[\s\S]*?setTimeout\w*\s*\(\s*\1[\s\S]*?\}?\s*\)', re.IGNORECASE),
        # (\w+) capture the variable name (resolve)
        # \w* zero or more alphanumeric characters (or underscore)
        # [\s\S] any character (space or non-space). Used to match newlines as well
        # *? Non-greedy quantifier (takes the minimum necessary), stop as soon as you find setTimeout, do not take the following ones
        # \1 Backreference to the captured variable (resolve)
        # ?: Indicates a non-capturing group (returns the entire match, not just the group)
    ]
    
    EVAL_PATTERNS = [
        re.compile(r'eval\s*\([\s\S]*?\)'),
    ]
    
    SHELL_COMMANDS_PATTERNS = [
        # obj.exec(command, args)
        re.compile(r'(\w+)?.?exec\s*\(\s*(\w+)\s*,\s*(\w+)\s*\)', re.IGNORECASE),
        # Bun is a JavaScript runtime similar to Node.js, and it has a function to execute system commands
        # await Bun.$`command`
        re.compile(r'(\w+)?\s*Bun\.\$\s*\`[\s\S]*?\`', re.IGNORECASE),
        # Not to be confused with RegExp.exec(), which is a method for searching for patterns in a string
    ]

    PREINSTALL_PATTERNS = [
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
        
        timing_delays_count, list_timing_delays = self.detect_timing_delays(content)
        metrics['timing_delays_count'] = timing_delays_count
        metrics['list_timing_delays'] = list_timing_delays

        eval_count, eval_list = self.detect_eval(content)
        metrics['eval_count'] = eval_count
        metrics['eval_list'] = eval_list

        shell_commands_count, list_shell_commands = self.detect_shell_commands(content)
        metrics['shell_commands_count'] = shell_commands_count
        metrics['list_shell_commands'] = list_shell_commands
        
        if len(file_diff_additions) > 0:
            preinstall_scripts_count, list_preinstall_scripts = self.detect_preinstall_scripts('\n'.join(file_diff_additions))
            metrics['preinstall_scripts_count'] = preinstall_scripts_count
            metrics['list_preinstall_scripts'] = list_preinstall_scripts
        
        return metrics
    
    def detect_timing_delays(self, content: str) -> tuple[int, list[str]]:
        matches = []
        for pattern in PayloadAnalyzer.TIMING_DELAYS_PATTERNS:
            for match in pattern.finditer(content):
                matches.append(match.group(0))
        return len(matches), matches
    
    def detect_eval(self, content: str) -> tuple[int, list[str]]:
        matches = []
        for pattern in PayloadAnalyzer.EVAL_PATTERNS:
            for match in pattern.finditer(content):
                matches.append(match.group(0))
        return len(matches), matches
    
    def detect_shell_commands(self, content: str) -> tuple[int, list[str]]:
        matches = []
        for pattern in PayloadAnalyzer.SHELL_COMMANDS_PATTERNS:
            for match in pattern.finditer(content):
                matches.append(match.group(0))
        return len(matches), matches
    
    def detect_preinstall_scripts(self, content: str) -> tuple[int, list[str]]:
        matches = []
        for pattern in PayloadAnalyzer.PREINSTALL_PATTERNS:
            for match in pattern.finditer(content):
                matches.append(match.group(0))
        return len(matches), matches