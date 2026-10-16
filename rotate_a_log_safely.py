"""
Your mission
If an existing file is larger than max_bytes, move it to path + ".1" (replace an existing backup), create an empty original, and return True. Otherwise return False, including a missing file. Fixtures reset before every test.

Start your 45-minute attempt, then implement the named function. Return the specified result; printing alone does not pass. Imports belong in your editor. Each test uses fresh fixtures.

Example & fixture
Fixture setup:
from pathlib import Path
Path('/lab').mkdir(exist_ok=True)
Path('/lab/app.log').write_text('abcdef')
Path('/lab/app.log.1').write_text('old')

Arguments: ["/lab/app.log",4]
Expected: true
"""
from pathlib import Path

def rotate_log(path, max_bytes):
    file_path = Path(path)

    if not file_path.exists():
        return False

    if file_path.stat().st_size <= max_bytes:
        return False

    backup_path = Path(str(file_path) + ".1")
    file_path.replace(backup_path)
    file_path.touch()

    return True

path = "/lab/app.log"

rotate_log(path,4)



