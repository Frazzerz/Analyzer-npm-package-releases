import subprocess
import os
from utils import synchronized_print, OutputTarget

class Deobfuscator:

    @staticmethod
    def deobfuscate(content: str, package_name: str, version: str, file_name: str) -> bool:
        """Deobfuscates a JavaScript file using the obfuscator-io-deobfuscator tool, saves the output to a structured directory, and returns True if successful."""

        synchronized_print(f"    Try to deobfuscate file: {file_name}, version {version}", target=OutputTarget.FILE_ONLY)
        base_name = os.path.splitext(file_name)[0]

        # Build directory path: "deobfuscated_files/{package_name}/{version}/"
        dir_path = os.path.join("deobfuscated_files", package_name.replace('/', '_'), version)
        output_file = os.path.join(dir_path, f"{base_name}-deobfuscated.js")

        if os.path.exists(output_file):
            synchronized_print(f"    Deobfuscated file already exists: {output_file}. Skipping deobfuscation.", target=OutputTarget.FILE_ONLY)
            return True
        os.makedirs(dir_path, exist_ok=True)
        
        # Write original content to a file
        with open(os.path.join(dir_path, f"{file_name}"), mode='w') as f:
            f.write(content)
            original_file = f.name

        command = ['obfuscator-io-deobfuscator', original_file, '-o', output_file]      # Build the command to run
        try:
            result = subprocess.run(command, check=True, capture_output=True, text=True, timeout=120)    
            if result.returncode == 0:
                synchronized_print(f"    Success! Deobfuscated file saved to: {output_file}", target=OutputTarget.FILE_ONLY)
                return True
                
        except Exception as e:
            error_msg = str(e).lower()
            if 'timed out' in error_msg:
                synchronized_print(f"    Deobfuscation process timed out for file: {file_name}", target=OutputTarget.FILE_ONLY)
            else:
                synchronized_print(f"    An error occurred during deobfuscation of file {file_name}: {e}", target=OutputTarget.FILE_ONLY)
        return False