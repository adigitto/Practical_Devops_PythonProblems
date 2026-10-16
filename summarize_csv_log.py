"""
Problem 4: Summarize errors from a CSV log
You’re investigating which services are generating the most server errors. Write a function that reads a CSV file and returns the top k services by failure count.
def top_failing_services(csv_path, k):
    ...
The CSV has these columns:
timestamp,service,status_code
2026-10-13T10:00:00,api,500
2026-10-13T10:00:01,worker,200
2026-10-13T10:00:02,api,502
2026-10-13T10:00:03,worker,503
2026-10-13T10:00:04,frontend,404
2026-10-13T10:00:05,worker,500
2026-10-13T10:00:06,cache,503

For k=2, return:
[("api", 2), ("worker", 2)]
Rules
- Status codes from 500 through 599 count as failures.
- Strip whitespace from service names and status codes.
- Skip rows with an empty service, a missing required value, or a status code that cannot be converted to an integer between 100 and 599.
- Treat the timestamp as text; you don’t need to parse or validate its format.
- Include only services with at least one failure.
- Sort by failure count descending; break ties by service name alphabetically.
- If k <= 0, return [] without opening the file.
- If fewer than k services have failures, return all of them.
- Let file-access errors propagate to the caller.
- Assume the CSV has the required headers and valid CSV structure, though individual row values may be invalid.
- Read the file row by row; don’t load all rows into a list.

"""

"""
Approach:
1. We need data structure to store failure counts
2. We need to return the k highest ones -- either a heap or counter can do it (going with counter and then using mostcommon(n) to get most common elements
3. EDIT -- We shouldnt use mostcommon because we also need tie breaker for sorting api through service names. So using sorted instead
"""

import csv
from collections import Counter

def top_failing_services(csv_path, k):
    if k <=0:
        return []
    
    freq_map = Counter()
    result = []
    with open(csv_path, mode ="r", encoding="utf-8", newline="") as file:
        rows = csv.DictReader(file)
        for row in rows:
            service = (row.get("service") or "").strip()
            status_code = int((row.get("status_code") or "").strip())

            if not service or not status_code:
                continue #skip row
            if status_code <= 100 or status_code >= 600:
                continue
            if 500 <= status_code <= 599:
                freq_map[service] +=1

    sorted_list = sorted(freq_map.items(), key = lambda x:(-x[1],x[0]))
    for i in range(k):
        result.append(sorted_list[i])
    return result

## Earlier Solution not optimal)
# def top_failing_services(csv_path, k):
#     freq_map = Counter()
#     mylist = []
#     if k <=0:
#         return []
#     with open(csv_path, mode="r",encoding="utf-8", newline="") as file:
#         items = csv.DictReader(file,delimiter=",")
#         for item in items:
#             if item["service"] == "":
#                 continue
#             if not item["status_code"].isdigit():
#                 continue
#             if int(item["status_code"]) >= 500:
#                 mylist.append(item["service"])
#                 # freq_map[item["service"]] +=1  #error counts
#     most_common = Counter(mylist).most_common(k)
#     return most_common

csv_path = "Inputs\\summarize_log.csv"
print(top_failing_services(csv_path,2))

