from pathlib import Path
from utils import NPMClient
from .version_analyzer import VersionAnalyzer
from git import Repo
from utils import synchronized_print
from models import VersionEntry
from packaging.version import Version
from analyzers.local_version_analyzer import LocalVersionAnalyzer

class PackageAnalyzer:
    """Coordinator for analyzing Git and local versions of an npm package"""
    def __init__(self, include_local: bool = False, local_versions_dir: str = "./other_versions", workers: int = 1, package_name: str = "", output_dir: Path = Path(".")):
        self.pkg_name = package_name
        self.output_dir = output_dir
        self.npm_client = NPMClient(pkg_name=package_name)
        self.include_local = include_local
        self.local_versions_dir = local_versions_dir
        self.version_analyzer = VersionAnalyzer(
            max_processes=workers,
            include_local=include_local,
            local_versions_dir=local_versions_dir,
            package_name=package_name,
            output_dir=output_dir
        )
        
    def analyze_package(self) -> None:
        """Analyze all releases of a package"""
        repo = self.npm_client.clone_package_repo()
        if repo:
            self.analyze_git_and_local_versions(repo)
        else:
            print(f"Unable to analyze {self.pkg_name} - Git repository not available")

    def analyze_git_and_local_versions(self, repo: Repo) -> None:
        """Analyze versions from Git tags and local versions"""

        tags = sorted(repo.tags, key=lambda t: t.commit.committed_datetime)
        if not tags:
            synchronized_print(f"No tags found for {self.pkg_name}")
            return []
        synchronized_print(f"Found {len(tags)} Git tags")
        
        entries = []
        # Git tags
        for tag in tags:
            entries.append(
                VersionEntry(
                    version=Version(self.normalize_git_tag(tag)),
                    name=tag.name,
                    source="git",
                    ref=tag
                )
            )

        if self.include_local:
            synchronized_print(f"Including local versions in Git analysis for {self.pkg_name}")
            localversionanalyzer = LocalVersionAnalyzer(local_versions_dir=self.local_versions_dir, pkg_name=self.pkg_name)
            localversionanalyzer.setup_local_versions()
            entries = localversionanalyzer.unite_versions(entries)
        
        self.version_analyzer.entries = entries
        self.version_analyzer.repo = repo
        self.version_analyzer.analyze_versions()
    
    def normalize_git_tag(self, tag) -> str:
        """Normalize Git tag by removing leading 'v' if present"""
        return tag.name.lstrip("v")