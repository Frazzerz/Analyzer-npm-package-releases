import subprocess
import os
from utils import synchronized_print

class Deobfuscator:

    @staticmethod
    def deobfuscate(content: str, package_name: str, version: str, file_name: str) -> None:
        """Deobfuscates a JavaScript file using the obfuscator-io-deobfuscator tool"""

        synchronized_print(f"Find deobfuscated js file! For package {package_name} version {version}, file {file_name}. Starting try to deobfuscate...")
        base_name = os.path.splitext(file_name)[0]

        # Build directory path: "deobfuscated_files/{package_name}/{version}/"
        dir_path = os.path.join("deobfuscated_files", package_name.replace('/', '_'), version)
        output_file = os.path.join(dir_path, f"{base_name}-deobfuscated.js")

        if os.path.exists(output_file):
            synchronized_print(f"Deobfuscated file already exists: {output_file}. Skipping deobfuscation...")
            return        
        os.makedirs(dir_path, exist_ok=True)
        
        with open(os.path.join(dir_path, f"{file_name}"), mode='w') as f:
            f.write(content)
            temp_file = f.name

        command = ['obfuscator-io-deobfuscator', temp_file, '-o', output_file]      # Build the command to run
        try:
            result = subprocess.run(command, check=True, capture_output=True, text=True, timeout=120)    
            if result.returncode == 0:
                synchronized_print(f"Success! Deobfuscated file saved to: {output_file}")
                
        except Exception as e:
            error_msg = str(e).lower()
            if 'timed out' in error_msg:
                synchronized_print(f"Deobfuscation process timed out for file: {file_name}")
            else:
                synchronized_print(f"An error occurred during deobfuscation of file {file_name}: {e}")