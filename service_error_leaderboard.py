"""
Your mission
Parse a JSON array of log objects. Count only records whose level is ERROR and service is a nonempty string. Ignore other records. Return [[service, count], ...], sorted by descending count then service name. Invalid JSON must return [].

Start your 45-minute attempt, then implement the named function. Return the specified result; printing alone does not pass. Imports belong in your editor. Each test uses fresh fixtures.

Example & fixture
Arguments: ["[{\"service\":\"api\",\"level\":\"ERROR\"},{\"service\":\"db\",\"level\":\"ERROR\"},{\"service\":\"api\",\"level\":\"ERROR\"}]"]
Expected: [["api",2],["db",1]]
"""
import json
from collections import Counter

def error_counts(input):
    try:
        data = json.loads(input)
    except Exception as e:
        print(f"Invalid json encountered with exception as {e}")
        return []
    
    freq_map = Counter()  #Initiates default int counts to 0
    
    for item in data:
        if item is not None and item!="":
            service = item.get("service","")
            level = item.get("level","")

            if service != "" and level == "ERROR":
                freq_map[service] +=1

    sorted_dict = sorted(freq_map.items(), key = lambda x: (-x[1],x[0]))
    return sorted_dict


input =  "[{\"service\":\"api\",\"level\":\"ERROR\"},{\"service\":\"db\",\"level\":\"ERROR\"},{\"service\":\"api\",\"level\":\"ERROR\"},{\"service\":\"api\",\"level\":\"ERROR\"},{\"service\":\"ui\",\"level\":\"ERROR\"},{\"service\":\"da\",\"level\":\"ERROR\"}]"


print(error_counts(input))