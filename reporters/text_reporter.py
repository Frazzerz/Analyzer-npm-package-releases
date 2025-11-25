from pathlib import Path
from typing import List, Dict
from dataclasses import asdict
from collections import defaultdict

from models import RedFlagChanges

class TextReporter:
    """Generate red flag text report"""

    # fields not considered red flags
    _IGNORE_FIELDS = {"package", "file_path", "version_from", "version_to"}

    @staticmethod
    def _get_active_flags(change: RedFlagChanges) -> List[str]:
        """Return the list of active flags for a change object"""
        data = asdict(change)
        return [field for field, value in data.items()
                if field not in TextReporter._IGNORE_FIELDS and value]

    @staticmethod
    def generate_summary(output_path: Path, changes: List[RedFlagChanges], package: str) -> None:
        with open(output_path, "w", encoding="utf-8") as f:

            f.write("=" * 70 + "\n")
            f.write(f"SUMMARY RED FLAGS - Analyzer NPM package releases - Package: {package}\n")
            f.write("=" * 70 + "\n\n")

            if not changes:
                f.write("No red flags found\n")
                return

            # Grouping by type
            flag_counts = defaultdict(int)
            for change in changes:
                for flag in TextReporter._get_active_flags(change):
                    flag_counts[flag] += 1

            f.write("RED FLAGS GROUPED BY TYPE\n")
            f.write("-" * 70 + "\n")
            for flag, count in sorted(flag_counts.items(), key=lambda x: -x[1]):        # sort by count desc
                f.write(f"  {flag:.<50} {count:>5}\n")                                  # clean alignment space

            f.write("\n" + "=" * 70 + "\n")
            f.write("DETAILS BY VERSION\n")
            f.write("=" * 70 + "\n\n")

            # Grouping by version
            grouped: Dict[str, List] = defaultdict(list)

            # Populate dict grouped
            for change in changes:
                active_flags = TextReporter._get_active_flags(change)
                if not active_flags:
                    continue

                key = f"{change.version_from} → {change.version_to}"
                grouped[key].append((change.file_path, active_flags))

            # Print order by version
            for version_key in sorted(grouped.keys()):
                f.write(f"Version: {version_key}\n")
                f.write("-" * 70 + "\n")

                for file_path, flags in grouped[version_key]:
                    f.write(f"  File: {file_path}\n")
                    for flag in flags:
                        f.write(f"    • {flag}\n")
                f.write("\n")