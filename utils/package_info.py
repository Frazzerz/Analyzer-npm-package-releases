import requests
from typing import Dict, Optional

class PackageInfo:
    """Utility class for retrieving package information from NPM registries"""
    
    def __init__(self):
        self.npm_registry_url = "https://registry.npmjs.org"
    
    def get_npm_package_data(self, package_name: str) -> Optional[Dict]:
        """Retrieves metadata for an NPM package by making an HTTP request to the registry"""
        
        try:
            response = requests.get(f'{self.npm_registry_url}/{package_name}', timeout=3)

            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error fetching NPM data for {package_name}: {response.status_code}")
        
        except Exception as e:
            print(f"Exception fetching NPM data for {package_name}: {e}")
        
        return None