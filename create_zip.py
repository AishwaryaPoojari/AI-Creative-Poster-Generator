"""
Zip Packaging Script
--------------------
Bundles the project into a clean, lightweight zip archive for submission.
Excludes virtual environment and temporary cache files.
"""

import os
import zipfile

OUTPUT_ZIP = "AI_Art_Creativity_Assignment.zip"
EXCLUDE_DIRS = {"venv", ".git", "__pycache__", ".idea", ".vscode"}
EXCLUDE_EXTS = {".pyc", ".pyo", ".pyd"}


def package_project():
    print(f"Creating submission package: {OUTPUT_ZIP}...")
    file_count = 0
    with zipfile.ZipFile(OUTPUT_ZIP, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk("."):
            # Exclude unwanted directories
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith(".")]

            for f in files:
                if f == OUTPUT_ZIP:
                    continue
                ext = os.path.splitext(f)[1]
                if ext in EXCLUDE_EXTS:
                    continue

                full_path = os.path.join(root, f)
                rel_path = os.path.relpath(full_path, ".")
                zf.write(full_path, rel_path)
                file_count += 1
                print(f"  + Added: {rel_path}")

    size_mb = os.path.getsize(OUTPUT_ZIP) / (1024 * 1024)
    print(f"\n[SUCCESS] Successfully packaged {file_count} files into '{OUTPUT_ZIP}' ({size_mb:.2f} MB).")


if __name__ == "__main__":
    package_project()
