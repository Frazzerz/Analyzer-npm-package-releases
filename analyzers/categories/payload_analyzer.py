import re
from typing import Dict
class PayloadAnalyzer:
    """Analyze payload delivery and execution techniques"""
    
    TIMING_DELAYS_PATTERNS = {
        # await new Promise( (resolve) => { setTimeout( resolve, 1000); } );
        r'await\s+new\s+Promise\s*\(\s*(\w+)\s*=>\s*\{?\s*[\s\S]*?setTimeout\w*\s*\(\s*\1[\s\S]*?\}?\s*\)',
        # (\w+) capture the variable name (resolve)
        # \w* zero or more alphanumeric characters (or underscore)
        # [\s\S] any character (space or non-space). Used to match newlines as well
        # *? Non-greedy quantifier (takes the minimum necessary), stop as soon as you find setTimeout, do not take the following ones
        # \1 Backreference to the captured variable (resolve)
        # ?: Indicates a non-capturing group (returns the entire match, not just the group)
    }
    
    EVAL_PATTERNS = {
        r'eval\s*\([\s\S]*?\)',
    }
    
    SHELL_COMMANDS_PATTERNS = {
        # obj.exec(command, args)
        r'(\w+)?.?exec\s*\(\s*(\w+)\s*,\s*(\w+)\s*\)',
        # Bun is a JavaScript runtime similar to Node.js, and it has a function to execute system commands
        # await Bun.$`command`
        r'(\w+)?\s*Bun\.\$\s*\`[\s\S]*?\`',
        # Not to be confused with RegExp.exec(), which is a method for searching for patterns in a string
    }

    PREINSTALL_PATTERNS = {
        r'"preinstall"\s*:\s*"[^"]*"\s*,?',
        # [^"]*  Any text between quotes
    }

    def analyze(self, content: str, file_diff_additions: list[str]) -> Dict:
        metrics = {
            'timing_delays_count': 0,
            'list_timing_delays': [],
            'eval_count': 0,
            'eval_list': [],
            'shell_commands_count': 0,
            'file_size_bytes': len(content.encode('utf-8')),
            'preinstall_scripts_count': 0,
            'list_preinstall_scripts': [],
            'presence_of_suspicious_dependency': 0,
        }
        
        for pattern in PayloadAnalyzer.TIMING_DELAYS_PATTERNS:
            for match in re.finditer(pattern, content, re.IGNORECASE):
                metrics['timing_delays_count'] += 1
                metrics['list_timing_delays'].append(match.group(0))

        for pattern in PayloadAnalyzer.EVAL_PATTERNS:
            for match in re.finditer(pattern, content, re.IGNORECASE):
                metrics['eval_count'] += 1
                metrics['eval_list'].append(match.group(0))
        
        for pattern in PayloadAnalyzer.SHELL_COMMANDS_PATTERNS:
            for match in re.finditer(pattern, content, re.IGNORECASE):
                metrics['shell_commands_count'] += 1
                metrics['list_shell_commands'].append(match.group(0))
        
        if len(file_diff_additions) > 0:
            for pattern in PayloadAnalyzer.PREINSTALL_PATTERNS:
                for match in re.finditer(pattern, '\n'.join(file_diff_additions), re.IGNORECASE):
                    metrics['preinstall_scripts_count'] += 1
                    metrics['list_preinstall_scripts'].append(match.group(0))
        
        return metrics