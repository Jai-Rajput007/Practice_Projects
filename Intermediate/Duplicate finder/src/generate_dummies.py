import os
import shutil
from pathlib import Path

TEST_ROOT = Path(__file__).resolve().parent.parent / "test_folder"

# ──────────────────────────────────────────────────────────────
# 2. Clean previous run – Windows-friendly version
# ──────────────────────────────────────────────────────────────
def safe_rmtree(path: Path):
    if not path.exists():
        return
    # Try normal delete first
    try:
        shutil.rmtree(path)
    except PermissionError:
        print(f"Warning: Could not delete {path} (locked by another process)")
        print("   → Continuing anyway – files will be overwritten")
    except Exception as e:
        print(f"Warning: Unexpected error while cleaning: {e}")

safe_rmtree(TEST_ROOT)

# Now always recreate the folder fresh
TEST_ROOT.mkdir(exist_ok=True)

def write_text_file(path:Path,lines:list[str]):
    path.write_text("\n".join(lines),encoding="utf-8")

def write_binary_file(path:Path,size_mb:int=1):
    chunk = os.urandom(1024*1024)
    with path.open("wb") as f:
        for _ in range(size_mb):
            f.write(chunk)
        f.write(os.urandom(size_mb*1024*1024%1024))

folders = [
    "Move 3",
    "Move 3/Move 1",
    "Move 3/Move 1/Move 5",
    "Move 4",
]
for f in folders:
    (TEST_ROOT / f).mkdir(parents=True, exist_ok=True)
write_text_file(TEST_ROOT/"test1.txt",["This is the original test1.txt","Unique content A"])
write_text_file(TEST_ROOT/"test2.csv",["name,age,city","Alice,30,Paris", "Bob,25,Tokyo"])
write_text_file(TEST_ROOT/"Move 3/Move 1/Moved1.txt",["Original Moved1.txt content", "Deep inside Move 1"])

write_binary_file(TEST_ROOT/"test3.jpg",size_mb=3)
write_binary_file(TEST_ROOT/"test4.docx",size_mb=2)
write_binary_file(TEST_ROOT/"test5.pdf",size_mb=4)
write_binary_file(TEST_ROOT/"Move 3/Move 1/Move 5/Moved5.pdf",size_mb=8)

duplicates = [
    # test1.txt appears twice more
    (TEST_ROOT / "test1.txt", TEST_ROOT / "Move 4/Moved4.docx"),   # same bytes, different extension!
    (TEST_ROOT / "test1.txt", TEST_ROOT / "Move 3/Moved3.jpg"),    # another copy disguised as jpg

    # Deep Moved1.txt has a duplicate in root
    (TEST_ROOT / "Move 3/Move 1/Moved1.txt",      TEST_ROOT / "test2.csv"),            # same content as test2.csv

    # The big 8 MB PDF has an exact twin at root
    (TEST_ROOT / "Move 3/Move 1/Move 5/Moved5.pdf", TEST_ROOT / "test5.pdf"),
]

for src,dst in duplicates:
    if dst.exists():
        dst.unlink()
    shutil.copy2(src,dst)

huge1 = TEST_ROOT / "large_video.iso"
huge2 = TEST_ROOT / "Move 3" / "large_video_backup.iso"

write_binary_file(huge1, size_mb=12)
shutil.copy2(huge1, huge2)

print("Test folder created successfully!")
print(f"Location: {TEST_ROOT.resolve()}")
print("\nYou now have:")
print("   • 3 groups of text duplicates (some with different extensions)")
print("   • 1 pair of identical 8 MB PDFs")
print("   • 1 pair of identical 12 MB huge files")
print("   • Plenty of unique files of different types and sizes")