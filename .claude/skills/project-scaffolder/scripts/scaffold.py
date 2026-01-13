#!/usr/bin/env python3
"""
Project Scaffolder Script

Usage:
    python scaffold.py --template node-express-ts --name my-project
    python scaffold.py --template react-vite-ts --name my-app
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Dict, Any


class ProjectScaffolder:
    """Main scaffolding class."""

    def __init__(self, template_name: str, project_name: str, install_deps: bool = False):
        self.template_name = template_name
        self.project_name = project_name
        self.install_deps = install_deps
        self.template_dir = Path(__file__).parent.parent / "assets" / "templates"
        self.template_data = None

    def load_template(self) -> bool:
        """Load template configuration."""
        template_file = self.template_dir / f"{self.template_name}.json"

        if not template_file.exists():
            print(f"Error: Template '{self.template_name}' not found")
            print(f"Available templates:")
            for t in self.template_dir.glob("*.json"):
                print(f"  - {t.stem}")
            return False

        with open(template_file, 'r') as f:
            self.template_data = json.load(f)

        return True

    def validate_project_name(self) -> bool:
        """Validate project name."""
        # Check for invalid characters
        if not self.project_name.replace('-', '').replace('_', '').isalnum():
            print(f"Error: Invalid project name '{self.project_name}'")
            print("Use only lowercase letters, numbers, hyphens, and underscores")
            return False

        # Check if directory already exists
        if os.path.exists(self.project_name):
            response = input(f"Directory '{self.project_name}' already exists. Overwrite? (y/N): ")
            if response.lower() != 'y':
                print("Scaffolding cancelled")
                return False

        return True

    def replace_placeholders(self, content: str) -> str:
        """Replace placeholders in content."""
        replacements = {
            "{{PROJECT_NAME}}": self.project_name,
            "{{PROJECT_NAME_UPPER}}": self.project_name.upper(),
            "{{PROJECT_NAME_TITLE}}": self.project_name.replace('-', ' ').title()
        }

        for placeholder, value in replacements.items():
            content = content.replace(placeholder, value)

        return content

    def create_structure(self, structure: Dict, current_path: Path):
        """Recursively create folder structure."""
        for name, content in structure.items():
            item_path = current_path / name

            if isinstance(content, dict):
                # It's a directory
                item_path.mkdir(parents=True, exist_ok=True)
                self.create_structure(content, item_path)
            elif isinstance(content, str):
                # It's a file with content
                if content.startswith("{{") and content.endswith("}}"):
                    # It's a placeholder for file content
                    file_key = content.strip("{}")
                    if file_key in self.template_data.get("files", {}):
                        file_content = self.template_data["files"][file_key]
                        file_content = self.replace_placeholders(file_content)

                        with open(item_path, 'w') as f:
                            f.write(file_content)
                        print(f"  Created: {item_path.relative_to(self.project_name)}")
                else:
                    # Direct content
                    content = self.replace_placeholders(content)
                    with open(item_path, 'w') as f:
                        f.write(content)
                    print(f"  Created: {item_path.relative_to(self.project_name)}")
            else:
                # Empty file
                item_path.touch()
                print(f"  Created: {item_path.relative_to(self.project_name)}")

    def initialize_git(self):
        """Initialize git repository."""
        try:
            os.chdir(self.project_name)
            os.system("git init")
            os.system("git add .")
            os.system('git commit -m "Initial commit: Project scaffolding"')
            os.chdir("..")
            print("\n  Git repository initialized")
        except Exception as e:
            print(f"\n  Warning: Could not initialize git: {e}")

    def install_dependencies(self):
        """Install project dependencies."""
        if not self.install_deps:
            return

        try:
            install_cmd = self.template_data.get("dependencies", {}).get("install_command", "npm install")
            print(f"\n  Installing dependencies with: {install_cmd}")
            os.chdir(self.project_name)
            os.system(install_cmd)
            os.chdir("..")
            print("  Dependencies installed successfully")
        except Exception as e:
            print(f"  Warning: Could not install dependencies: {e}")

    def scaffold(self) -> bool:
        """Main scaffolding process."""
        print("=" * 60)
        print("PROJECT SCAFFOLDER")
        print("=" * 60)

        # Load template
        if not self.load_template():
            return False

        # Validate project name
        if not self.validate_project_name():
            return False

        # Create project structure
        print(f"\nScaffolding project: {self.project_name}")
        print(f"Template: {self.template_data['description']}")
        print("\nCreating files...")

        project_path = Path(self.project_name)
        project_path.mkdir(parents=True, exist_ok=True)

        structure = self.template_data.get("structure", {})
        self.create_structure(structure, project_path)

        # Initialize git
        self.initialize_git()

        # Install dependencies
        if self.install_deps:
            self.install_dependencies()

        # Print success message
        self.print_success_message()

        return True

    def print_success_message(self):
        """Print success message with next steps."""
        print("\n" + "=" * 60)
        print(f"SUCCESS! Project '{self.project_name}' created")
        print("=" * 60)

        install_cmd = self.template_data.get("dependencies", {}).get("install_command", "npm install")

        print("\nNext steps:")
        print(f"  1. cd {self.project_name}")

        if not self.install_deps:
            print(f"  2. {install_cmd}")
            print("  3. cp .env.example .env")
            print("  4. npm run dev  (or python run.py)")
        else:
            print("  2. cp .env.example .env")
            print("  3. npm run dev  (or python run.py)")

        print("\nFor more information, see README.md")
        print("=" * 60)


def main():
    parser = argparse.ArgumentParser(description="Project Scaffolder")

    parser.add_argument("--template", "-t", required=True, help="Template name (e.g., node-express-ts, react-vite-ts)")
    parser.add_argument("--name", "-n", required=True, help="Project name")
    parser.add_argument("--install", "-i", action="store_true", help="Install dependencies after scaffolding")

    args = parser.parse_args()

    scaffolder = ProjectScaffolder(
        template_name=args.template,
        project_name=args.name,
        install_deps=args.install
    )

    success = scaffolder.scaffold()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
