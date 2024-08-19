import sys
import functools
import json


def handle_errors(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"\033[91mError: {e}\033[0m")
            sys.exit(1)
    return wrapper


def write_json(filename, package_dict):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(json.dumps(package_dict))


def read_json(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return json.loads(f.read())
