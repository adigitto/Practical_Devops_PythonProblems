'''
Problem 6: Merge maintenance windows
Your monitoring system receives maintenance windows from multiple teams. Overlapping windows should be merged so alerts can be suppressed during the combined periods.
Implement:
def merge_maintenance_windows(windows):
    ...
Each window is a tuple (start, end) using integer minutes.
Example
windows = [
    (60, 120),
    (90, 150),
    (200, 240),
    (150, 180),
    (300, 330),
]
Expected:
[(60, 180), (200, 240), (300, 330)]
The first two windows overlap. The window (150, 180) touches the combined window at 150, so it merges too.
Rules
- Input windows may be in any order.
- Merge overlapping or touching windows.
- Return the merged windows sorted by start time.
- Return [] for empty input.
- Assume valid integer values with start < end.
- Do not modify the input list.
- Duplicate windows should merge into one.
- Aim for O(n log n) time.
Another example:
merge_maintenance_windows([(10, 50), (20, 30), (50, 60)])
# [(10, 60)]
'''

"""
My Approach -- 1. First sort the tuples wrt to the first element in ascending order.
Use 2 pointers(i,j) - compare last element of tuple1 (t1) with first element of tuple2(t2), if its greater, then compare last of t1 with last of t2 - whichever is greater is the last elemt of merged tuple.
Then move the pointer j to next tuple and keep i at same pointer and compare them, if no merge needed, move both pointers ... continue till j < len(tuple_list)
"""

#Pythonic way (optimized) of solving this:
def merge_intervals_optimized(windows):
    merged = []

    for start, end in sorted(windows):      #this is called tuple unpacking. Eg. start = 60, end =120 for first tuple
        if not merged or start > merged[-1][1]:
            merged.append((start, end))  #add the whole element (no merge)
        else:
            # Overlapping or touching: extend the last interval.
            previous_start, previous_end = merged[-1]
            merged[-1] = (previous_start, max(previous_end, end))

    return merged

#Below code I have written works correctly, but is not optimized due to element deletion!
def merge_intervals(windows):
    i,j = 0,1 #2 pointers
    
    #sort the list first
    windows.sort(key=lambda x:x[0])
    # temp_list = []
    print(windows)
    # merged = []
    while j < len(windows):
        if windows[i][1] >= windows[j][0]:
            if windows[i][1] >= windows[j][1]:
                windows[i] = (windows[i][0], windows[i][1])
                windows.remove(windows[j])
                # interval = (windows[i][0], windows[i][1])
            else:
                windows[i] = (windows[i][0], windows[j][1]) 
                windows.remove(windows[j])
                # interval = (windows[i][0], windows[j][1])
        else:
            i+=1
            j+=1
    return windows



windows = [
    (60, 120),
    (90, 150),
    (200, 240),
    (150, 180),
    (300, 330),
]

print(merge_intervals(windows))
