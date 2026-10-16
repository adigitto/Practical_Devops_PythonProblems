'''
You’re investigating a server running low on disk space. Write a function that recursively searches a directory and returns its k largest log files.
def largest_logs(root_dir, k):
    ...
Return a list of (absolute_path, size_in_bytes) tuples, ordered from largest to smallest.
Example directory
/lab/logs/
    app.log          120 bytes
    debug.txt        900 bytes
    nginx/
        access.log   500 bytes
        error.log    250 bytes
    worker/
        jobs.log     300 bytes
largest_logs("/lab/logs", 2)
Expected:
[
    ("/lab/logs/nginx/access.log", 500),
    ("/lab/logs/worker/jobs.log", 300),
]
Rules
- Include only regular files with the exact, case-sensitive suffix .log.
- Search all nested directories.
- Skip symbolic links, including links to directories.
- Skip files or directories that disappear or cannot be accessed.
- Return [] if k <= 0, or the root is missing or isn’t a directory.
- If fewer than k matching files exist, return all of them.
- Files with equal sizes may appear in any order.
- Assume the directory may contain millions of files; keep only O(k) file candidates in memory. Directory traversal itself may use additional memory.
'''

"""
Approach - 
High Level:
Traverse through each file using Path, check file (using st_size) size and add it to a heap that only stores 2 elements. The final heap will contain 2 largest elements.
Hint/Trick - Python compares tuples from left to right. So whatever element is in left tuple is set for sorting order
"""

#Additional challenge -- Pass the parameters as arguments

from pathlib import Path
import heapq, argparse

class largest_file:

    def largest_file_checker(self, dir_path, k_largest):
        # Set initial heap_list as blank
        min_heap = []

        if dir_path is None or k_largest <=0:
            return []
        
        file_path = Path(dir_path)
        if not file_path.is_dir():  #if its not a directory
            return []

        for file in file_path.rglob("*"):
            if not file.is_file() or file.is_symlink():
                continue

            if file.suffix != ".py":  #lets do it for .py files instead
                continue
            
            size = file.stat().st_size
            # First lets push
            heapq.heappush(min_heap,(size, str(file.absolute())))

            #Now lets pop out if heap becomes greater than k
            if len(min_heap) > k_largest:
                heapq.heappop(min_heap)

        # We want the heap elements in descending order - largest to smallest, so we need to sort it

        sorted_elems = sorted(min_heap, reverse=True) 
        return [sorted_elems[0],sorted_elems[1]]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=str)
    parser.add_argument("--k",type=int)

    args = parser.parse_args()
    file_checker = largest_file()
    result = file_checker.largest_file_checker(args.path,args.k)
    print(result)



