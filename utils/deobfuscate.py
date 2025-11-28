import subprocess
import os

class Deobfuscator:

    @staticmethod
    def deobfuscate(content: str, package_name: str, version: str, file_name: str):
        """Deobfuscates a JavaScript file using the obfuscator-io-deobfuscator tool"""

        print(f"Find deobfuscated js file! For package {package_name} version {version}, file {file_name}. Starting try to deobfuscate...")
        base_name = os.path.splitext(file_name)[0]

        # Build directory path: "deobfuscated_files/{package_name}/{version}/"
        dir_path = os.path.join("deobfuscated_files", package_name.replace('/', '_'), version)
        output_file = os.path.join(dir_path, f"{base_name}-deobfuscated.js")

        if os.path.exists(output_file):
            print(f"Deobfuscated file already exists: {output_file}. Skipping deobfuscation...")
            return        
        os.makedirs(dir_path, exist_ok=True)
        
        with open(os.path.join(dir_path, f"{file_name}"), mode='w') as f:
            f.write(content)
            temp_file = f.name

        command = ['obfuscator-io-deobfuscator', temp_file, '-o', output_file]      # Build the command to run
        
        try:
            result = subprocess.run(command, check=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"Success! Deobfuscated file saved to: {output_file}")
            else:
                print("An error occurred during deobfuscation: ", result.stderr)
                
        except subprocess.CalledProcessError as e:
            print(f"Failed to run the deobfuscator. Error: {e}")
        except FileNotFoundError:
            print("Error: The 'obfuscator-io-deobfuscator' command was not found. Please ensure it is installed globally using npm")