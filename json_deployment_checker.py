'''
Problem 5: Validate a JSON service configuration
You're writing a pre-deployment checker. It reads a JSON configuration and reports invalid service settings before deployment.
Implement:
def validate_config(config_path):
    ...
Example file:
{
  "services": [
    {"name": "api", "port": 8080, "replicas": 3},
    {"name": "worker", "port": 9000, "replicas": 2},
    {"name": "api", "port": 70000, "replicas": 0}
  ]
}
Expected result:
[
    "services[2]: duplicate name 'api'",
    "services[2]: port must be an integer between 1 and 65535",
    "services[2]: replicas must be an integer between 1 and 100"
]
Rules
- Read the file using Python’s json module.
- The top-level value must be a dictionary containing "services" as a list. Otherwise, return:["config: services must be a list"]
- Each list entry must be a dictionary. For other values, report:"services[i]: must be an object"
  Then continue to the next entry.
- Validate each service in this order:
  1. Name: Must be a nonempty string after stripping whitespace. Otherwise report "services[i]: name must be a nonempty string".
  2. Uniqueness: Valid names must be unique after stripping whitespace. Names are case-sensitive. Report duplicates using the format shown above. Track valid names even when other fields are invalid.
  3. Port: Must be an integer from 1 through 65535.
  4. Replicas: Must be an integer from 1 through 100.
- Missing fields are invalid. Booleans must not count as integers.
- Collect all validation errors in list order; don’t stop at the first invalid field.
- Return [] for a valid configuration, including an empty services list.
- Let file-access errors and invalid JSON errors propagate to the caller.

'''
import json


def pre_deployment_checker(json_file):
    with open(json_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, dict):
        return ["config: services must be a list"]

    services = data.get("services")
    if not isinstance(services, list):
        return ["config: services must be a list"]

    result_list = []
    service_set = set()

    for ind, val in enumerate(services):
        prefix = f"services[{ind}]"

        if not isinstance(val, dict):
            result_list.append(f"{prefix}: must be an object")
            continue

        name = val.get("name")

        if not isinstance(name, str) or not name.strip():
            result_list.append(
                f"{prefix}: name must be a nonempty string"
            )
        else:
            service = name.strip()

            if service in service_set:
                result_list.append(
                    f"{prefix}: duplicate name '{service}'"
                )
            else:
                service_set.add(service)

        port = val.get("port")
        if type(port) is not int or not 1 <= port <= 65535:
            result_list.append(
                f"{prefix}: port must be an integer between 1 and 65535"
            )

        replicas = val.get("replicas")
        if type(replicas) is not int or not 1 <= replicas <= 100:
            result_list.append(
                f"{prefix}: replicas must be an integer between 1 and 100"
            )

    return result_list

input_file = "Inputs\\services_checker.json"
result = pre_deployment_checker(input_file)
for i in result:
    print(i)