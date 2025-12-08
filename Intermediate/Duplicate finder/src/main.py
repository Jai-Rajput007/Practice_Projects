# src/main.py
import argparse
import os
from collections import defaultdict
from pathlib import Path
from hasher import get_file_hash

# ====================== Argument Parser ======================
parser = argparse.ArgumentParser(description="Fast Duplicate File Finder")
parser.add_argument(
    "folder",
    type=Path,
    nargs='?',
    default=Path("../test_folder"),
    help="Folder to scan for duplicates"
)
parser.add_argument(
    "--delete",
    action="store_true",
    help="Delete duplicates after confirmation (keeps one copy)"
)
args = parser.parse_args()

target_path = args.folder.resolve()

if not target_path.exists():
    print(f"Error: Folder not found → {target_path}")
    exit(1)
if not target_path.is_dir():
    print(f"Error: Not a folder → {target_path}")
    exit(1)

# Global dictionaries (will be filled by phases)
files_by_size = None
files_by_partial = None
files_by_full = None

# ====================== Phase 1 – Group by Size ======================
def phase1_group_by_size(target: Path):
    global files_by_size
    files_by_size = defaultdict(list)

    for root, dirs, files in os.walk(target):
        for file_name in files:
            file_path = Path(root) / file_name

            if file_path.is_symlink():
                continue

            try:
                size = file_path.stat().st_size          # ← Fixed: .stat().st_size
            except (OSError, FileNotFoundError):
                continue

            files_by_size[size].append(file_path)

    # Remove unique sizes
    singletons = [s for s, paths in files_by_size.items() if len(paths) == 1]
    for s in singletons:
        del files_by_size[s]

    print(f"Phase 1: {len(files_by_size)} size groups remain")

# ====================== Phase 2 – Partial Hash (1KB) ======================
def phase2_partial_hash():
    global files_by_partial
    files_by_partial = defaultdict(list)

    for paths in files_by_size.values():
        if len(paths) >= 2:
            for file_path in paths:
                partial = get_file_hash(file_path, first_chunk_only=True)
                files_by_partial[partial].append(file_path)

    # Remove unique partial hashes
    singletons = [h for h, paths in files_by_partial.items() if len(paths) == 1]
    for h in singletons:
        del files_by_partial[h]

    print(f"Phase 2: {len(files_by_partial)} partial-hash groups remain")

# ====================== Phase 3 – Full Hash Confirmation ======================
def phase3_full_hash():
    global files_by_full
    files_by_full = defaultdict(list)

    for paths in files_by_partial.values():
        if len(paths) >= 2:
            for file_path in paths:
                full = get_file_hash(file_path, first_chunk_only=False)
                files_by_full[full].append(file_path)

    # Remove false positives
    singletons = [h for h, paths in files_by_full.items() if len(paths) == 1]
    for h in singletons:
        del files_by_full[h]

    print(f"Phase 3: {len(files_by_full)} confirmed duplicate groups!")

# ====================== Phase 4 – Pretty Output ======================
def phase4_print_results():
    print("\n" + "="*70)
    if not files_by_full:
        print("No duplicates found! Your folder is perfectly clean.")
    else:
        print(f"FOUND {len(files_by_full)} DUPLICATE GROUP(S)!")
        total_wasted_mb = 0
        group_id = 1

        for paths in files_by_full.values():
            paths = sorted(paths, key=lambda p: str(p))
            size_mb = paths[0].stat().st_size / (1024 * 1024)
            wasted_mb = (len(paths) - 1) * size_mb
            total_wasted_mb += wasted_mb

            print(f"\nGroup {group_id} → {len(paths)} copies → {size_mb:.2f} MB each")
            print(f"           Wasting → {wasted_mb:.2f} MB")
            for i, path in enumerate(paths, 1):
                marker = "Original" if i == 1 else "Duplicate"
                print(f"   [{marker.ljust(9)}] {path}")
            group_id += 1

        print("\n" + "─"*70)
        print(f"TOTAL SPACE YOU CAN FREE: {total_wasted_mb:.2f} MB")
    print("="*70)

# ====================== Phase 5 – Safe Delete ======================
def phase5_delete_duplicates():
    if not files_by_full:
        print("Nothing to delete.")
        return

    total_files = sum(len(paths) - 1 for paths in files_by_full.values())
    total_mb = sum((len(paths) - 1) * paths[0].stat().st_size for paths in files_by_full.values()) / (1024*1024)

    print(f"\nDELETE MODE ACTIVE")
    print(f"Will delete {total_files} file(s) → free {total_mb:.2f} MB\n")
    confirm = input("Type exactly 'YES' to proceed: ")

    if confirm != "YES":
        print("Cancelled. No files deleted.")
        return

    deleted = 0
    for paths in files_by_full.values():
        keep = paths[0]
        for dup in paths[1:]:
            try:
                dup.unlink()
                print(f"Deleted → {dup}")
                deleted += 1
            except Exception as e:
                print(f"Failed → {dup} [{e}]")

    print(f"\nSUCCESS! Deleted {deleted} duplicates.")
    print(f"Freed {total_mb:.2f} MB")

# ====================== MAIN – Run everything ======================
if __name__ == "__main__":
    print(f"Scanning: {target_path}\n")
    
    phase1_group_by_size(target_path)
    phase2_partial_hash()
    phase3_full_hash()
    phase4_print_results()

    if args.delete:
        phase5_delete_duplicates()
    else:
        print("\nTip: Add --delete to remove duplicates")