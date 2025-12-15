from pathlib import Path
from typing import List
from dataclasses import asdict, fields
from collections import defaultdict
from models import RedFlagChanges

class TextReporter:
    """Generate red flag text report considering all red flag fields"""

    @staticmethod
    def _get_active_flags(change: RedFlagChanges) -> List[str]:
        """Return the list of active flags for a change object"""
        data = asdict(change)
        # Get all fields from the dataclass
        all_fields = [field.name for field in fields(change)]
        # Return only boolean fields that are True (excluding non-flag fields)
        return [field for field in all_fields 
                if field not in {"package", "version_from", "version_to"} 
                and data.get(field, False)]

    @staticmethod
    def generate_compact_report(output_path: Path, changes: List[RedFlagChanges], package: str) -> None:
        """Alternative compact format showing flags per version without file details"""
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"RED FLAGS REPORT - Package: {package}\n")
            f.write("=" * 60 + "\n\n")

            version_groups = defaultdict(list)
            
            for change in changes:
                active_flags = TextReporter._get_active_flags(change)
                if active_flags:
                    version_key = f"{change.version_from} → {change.version_to}"
                    version_groups[version_key].extend(active_flags)

            if version_groups:
                for version_key in sorted(version_groups.keys()):
                    f.write(f"{version_key}:\n")
                    flags = sorted(set(version_groups[version_key]))
                    for flag in flags:
                        f.write(f"  • {flag}\n")
                    f.write("\n")
            else:
                f.write("No red flags detected in any version\n")