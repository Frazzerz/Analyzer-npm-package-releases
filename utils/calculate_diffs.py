import difflib
from typing import Optional, Tuple
import hashlib

class CalculateDiffs:
    """Calcola le differenze tra file di versioni diverse in modo ottimizzato"""
    
    @staticmethod
    def calculate_file_diffs(old_content: Optional[str], new_content: Optional[str]) -> Tuple[list[str], list[str]]:
        """
        Calcola il diff tra due versioni di un file, restituendo sia aggiunte che rimozioni.
        Più efficiente di calcolarli separatamente.
        """
        if old_content is None or new_content is None:
            return [], []
        
        # Usa hash per verificare se i contenuti sono uguali rapidamente
        old_hash = hashlib.md5(old_content.encode()).hexdigest()
        new_hash = hashlib.md5(new_content.encode()).hexdigest()
        
        if old_hash == new_hash:
            return [], [] 

        old_lines = old_content.splitlines(keepends=True)
        new_lines = new_content.splitlines(keepends=True)
        
        additions = []
        deletions = []
        
        # Usa SequenceMatcher per un calcolo più efficiente
        matcher = difflib.SequenceMatcher(None, old_lines, new_lines)
        
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == 'insert':
                # Linee aggiunte
                additions.extend([line.strip() for line in new_lines[j1:j2]])
            elif tag == 'delete':
                # Linee rimosse
                deletions.extend([line.strip() for line in old_lines[i1:i2]])
            elif tag == 'replace':
                # Quando c'è sostituzione, le vecchie linee sono rimosse, le nuove sono aggiunte
                deletions.extend([line.strip() for line in old_lines[i1:i2]])
                additions.extend([line.strip() for line in new_lines[j1:j2]])
            # 'equal' non ci interessa per le differenze
        
        return additions, deletions
