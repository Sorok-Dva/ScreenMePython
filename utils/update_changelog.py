import sys
import os
from datetime import datetime

CHANGELOG_FILE = "CHANGELOG.md"

def update_changelog(version, changes):
    if not os.path.exists(CHANGELOG_FILE):
        print(f"{CHANGELOG_FILE} does not exist.")
        return

    with open(CHANGELOG_FILE, "r") as file:
        lines = file.readlines()

    with open(CHANGELOG_FILE, "w") as file:
        found_unreleased = False
        for line in lines:
            if line.strip() == "## [Unreleased]":
                found_unreleased = True
                file.write(line)
                file.write("\n")
                file.write(f"## [{version}] - {datetime.now().strftime('%Y-%m-%d')}\n")
                file.write("### Added\n")
                for change in changes:
                    file.write(f"- {change}\n")
                file.write("\n")
            else:
                file.write(line)

        if not found_unreleased:
            file.write("\n## [Unreleased]\n")
            file.write("\n")
            file.write(f"## [{version}] - {datetime.now().strftime('%Y-%m-%d')}\n")
            file.write("### Added\n")
            for change in changes:
                file.write(f"- {change}\n")
            file.write("\n")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python update_changelog.py <version> <change1> [<change2> ... <changeN>]")
        sys.exit(1)

    version = sys.argv[1]
    changes = sys.argv[2:]
    update_changelog(version, changes)
