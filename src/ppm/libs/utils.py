import sys
import functools
import json
import re
import locale


ENCODING = locale.getencoding()


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
    with open(filename, "w", encoding=ENCODING) as f:
        f.write(json.dumps(package_dict))


def read_json(filename):
    with open(filename, "r", encoding=ENCODING) as f:
        return json.loads(f.read())


def get_package_info(package):
    try:
        package_name, version = package.split("@")
    except ValueError:
        package_name = package
        version = 'latest'
    return (package_name, version)


def create_file(path):
    with open(path, 'a'):
        pass


def get_version_info(stdout):
    stdout = stdout.decode(ENCODING)
    info = {}
    info['name'] = re.findall('Name:(.*)\n', stdout)[0].strip()
    info['version'] = re.findall('Version:(.*)\n', stdout)[0].strip()
    info['summary'] = re.findall('Summary:(.*)\n', stdout)[0].strip()
    info['home_page'] = re.findall('Home-page:(.*)\n', stdout)[0].strip()
    info['author'] = re.findall('Author:(.*)\n', stdout)[0].strip()
    info['author_email'] = re.findall('Author-email:(.*)\n', stdout)[0].strip()
    info['license'] = re.findall('License:(.*)\n', stdout)[0].strip()
    info['location'] = re.findall('Location:(.*)\n', stdout)[0].strip()
    info['author_email'] = re.findall('Author-email:(.*)\n', stdout)[0].strip()
    info['requires'] = re.findall('Requires:(.*)\n', stdout)[0].strip()
    info['required_by'] = re.findall('Required-by:(.*)\n', stdout)[0].strip()
    return info


def append_file(path, line):
    with open(path, 'a') as f:
        f.write('%s\n' % line)


def read_file(path):
    with open(path, 'r') as f:
        return f.read()
