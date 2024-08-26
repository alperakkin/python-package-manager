from pathlib import Path

from ppm.libs.utils import (write_json, read_json,
                            handle_errors, load_package, get_package_info)
from ppm.libs.process import Shell


class PackageManager:
    PACKAGE_PATH = "pyconfig.json"

    def __init__(self):
        self.project = ""
        self.author = ""
        self.author_url = ""
        self.version = "1.0.0"
        self.virtual_env = ""
        self.env_file = ".env"
        self.scripts = {
            "start": "",
            "build": "",
            "test": ""
        }
        self.shell = "sh"
        self.module = "python3.8"
        self.packages = {}
        self.__shell_manager = Shell()

    @property
    def shell_manager(self):
        return self.__shell_manager

    @property
    def to_dict(self):
        dict_view = self.__dict__.copy()
        for k in self.__dict__:
            if k.startswith("_"):
                dict_view.pop(k)
        return dict_view

    @property
    def env_path(self):
        return Path(self.project) / self.virtual_env

    def get_func_name(self, func):
        return func.split("cmd_")[1]

    def validate(self, key):
        if key == 'project' and self.project == "":
            raise ValueError("A project name should be defined!")
        if key == 'shell' and self.shell == "":
            raise ValueError("Working shell should be defined!")

    def eval_package(self):
        project_path = Path(self.project)
        project_path.mkdir(parents=True, exist_ok=True)
        self.shell_manager.execute(f"python -m venv {self.env_path}")
        # TODO: Activate the virtual environment here
        # TODO: Set project file as active dir

    def execute_package_scripts(self, script_name):
        package = read_json(self.PACKAGE_PATH)
        script = package["scripts"].get(script_name)
        if not script:
            raise ValueError(
                f"Please provide a {script_name} "
                f"script in to {self.PACKAGE_PATH}"
            )

        self.shell_manager.execute(script)

    @ handle_errors
    def cmd_start(self):
        """Executes the predefined start script"""
        self.execute_package_scripts('start')

    @ handle_errors
    def cmd_build(self):
        """Executes the predefined build script"""
        self.execute_package_scripts('build')

    @ handle_errors
    def cmd_test(self):
        """Executes the predefined test script"""
        self.execute_package_scripts('test')

    @ handle_errors
    def cmd_init(self):
        """Initializes a new project"""

        for key, val in self.to_dict.items():
            if isinstance(val, str):
                out = input(f"{key}: {val} -> ")
                setattr(self, key, out or val)
                self.validate(key)

        package_path = Path(self.project) / Path(self.PACKAGE_PATH)
        self.eval_package()
        write_json(package_path, self.to_dict)

    @ handle_errors
    def cmd_run(self, script):
        """Executes predefined script"""
        script = ' '.join(script)
        self.shell_manager.execute(script)

    # @ handle_errors
    @ load_package
    def cmd_install(self, packages):
        for package in packages:
            package_name, version = get_package_info(package)
            install_script = package_name if version == 'latest'\
                else f'{package_name}=={version}'

            res = self.shell_manager.execute(
                f"./{self.virtual_env}/bin/pip install {install_script}"
            )
            if res.returncode == 1:
                raise ValueError("Not a valid package")

            if version == 'latest':
                res = self.shell_manager.execute(
                    f"./{self.virtual_env}/bin/pip show {package_name}"
                )
            res.stdout.split("\n")
            # TODO: get installed package info from stdout
