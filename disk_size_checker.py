'''
Problem 7: Build a command-line disk usage checker
Write a Python script that scans a directory and reports the total size of matching files for each immediate subdirectory.
Example:
logs/
    app/
        server.log       100 bytes
        nested/
            error.log     50 bytes
    worker/
        jobs.log         200 bytes
        notes.txt         80 bytes
    archive/
    root.log             300 bytes

Command:
python disk_report.py logs --extension .log --min-bytes 100
Expected printed output:
worker,200
app,150

Implement two parts:
def directory_usage(root_dir, extension, min_bytes):
    """Return a list of (directory_name, total_bytes) tuples."""
    ...
And a command-line entry point using argparse with:
- root_dir: required positional argument.
- --extension: optional suffix filter, default .log.
- --min-bytes: optional nonnegative integer, default 0.

Rules
- For each immediate subdirectory, recursively sum the sizes of matching files inside it.
- Exclude files directly inside the root, such as root.log.
- Match extensions exactly and case-sensitively.
- Skip symbolic links, including directory links.
- Include directories whose total is at least min_bytes. Empty directories have total 0.
- Sort results by total size descending, then directory name alphabetically.
- Assume the root exists, is a directory, and its contents are accessible and remain unchanged during execution.
- The function returns results; the command-line entry point prints one directory_name,total_bytes line per result.
- Reject a negative --min-bytes with an argument-parsing error.
'''

"""
Approach:
Here, pending is a stack of directories still to visit:
1. Start with the immediate subdirectory.
2. Pop a directory and inspect its contents.
3. Add nested directories to the stack.
4. Add matching file sizes to the total.
5. Skip every symbolic link before deciding whether to traverse it.
You can also use your original folder.rglob("*") approach: by default, it does not recursively expand directory symlinks. The explicit stack makes that behavior clear and gives you control over traversal. The argparse portion stays the same.
"""


from pathlib import Path

def directory_usage(root_dir, extension, min_bytes):
    results = []

    for folder in Path(root_dir).iterdir():
        if folder.is_symlink() or not folder.is_dir():
            continue

        total = 0
        pending = [folder]

        while pending:
            current = pending.pop()

            for entry in current.iterdir():
                if entry.is_symlink():
                    continue

                if entry.is_dir():
                    pending.append(entry)
                elif entry.is_file() and entry.suffix == extension:
                    total += entry.stat().st_size

        if total >= min_bytes:
            results.append((folder.name, total))

    return sorted(results, key=lambda item: (-item[1], item[0]))