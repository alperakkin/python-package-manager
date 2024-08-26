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


def load_package(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        self = args[0]
        package = read_json(self.PACKAGE_PATH)
        self.__dict__.update(package)
        return func(*args, **kwargs)

    return wrapper


def write_json(filename, package_dict):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(json.dumps(package_dict))


def read_json(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return json.loads(f.read())


def get_package_info(package):
    try:
        package_name, version = package.split("@")
    except ValueError:
        package_name = package
        version = 'latest'
    return (package_name, version)
