import difflib
from typing import Optional, Tuple
import hashlib

class CalculateDiffs:
    """Calculates the differences (additions and removals) between versions of a file"""
    
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
        
        # Use SequenceMatcher for a more efficient calculation
        matcher = difflib.SequenceMatcher(None, old_lines, new_lines)
        
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == 'insert':
                additions.extend([line.strip() for line in new_lines[j1:j2]])
            elif tag == 'delete':
                deletions.extend([line.strip() for line in old_lines[i1:i2]])
            elif tag == 'replace':
                # When there is a replacement, the old lines are removed, the new ones are added
                deletions.extend([line.strip() for line in old_lines[i1:i2]])
                additions.extend([line.strip() for line in new_lines[j1:j2]])
        
        return additions, deletions
