import difflib
from typing import Optional, Tuple
import hashlib

class CalculateDiffs:
    """Calculates the differences (additions and removals) between versions of a file"""
    '''No more needed'''
    
    @staticmethod
    def calculate_file_diffs(old_content: Optional[str], new_content: Optional[str]) -> Tuple[list[str], list[str]]:

        if old_content is None or new_content is None:
            return [], []
        
        # Use hash to quickly check if contents are the same
        old_hash = hashlib.md5(old_content.encode()).hexdigest()
        new_hash = hashlib.md5(new_content.encode()).hexdigest()
        
        if old_hash == new_hash:
            return [], [] 

        old_lines = old_content.splitlines(keepends=True)
        new_lines = new_content.splitlines(keepends=True)
        
        additions = []
        deletions = []
        
        diff = difflib.unified_diff(old_lines, new_lines, lineterm='')
        
        for line in diff:
            if line.startswith('+') and not line.startswith('+++'):
                additions.append(line[1:].strip())
            elif line.startswith('-') and not line.startswith('---'):
                deletions.append(line[1:].strip())
        
        return additions, deletions
