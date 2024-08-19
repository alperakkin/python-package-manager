import json


def write_json(filename, package_dict):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(json.dumps(package_dict))


def read_json(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return json.loads(f.read())
