import os
from pathlib import Path

from ppm.libs.utils import (write_json, read_json,
                            handle_errors, load_package, get_package_info,
                            get_version_info, create_file)
from ppm.libs.process import Shell


class PackageManager:
    PACKAGE_PATH = "pyconfig.json"
    LOCK_PATH = "pyconfig.lock.json"

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
        self.module = "python"
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
        # create project folder
        project_path.mkdir(parents=True, exist_ok=True)

        # create .env
        create_file(f"{self.project}/{self.env_file}")

        # create virtual env
        self.shell_manager.execute(f"{self.module} -m venv {self.env_path}")
        cwd = os.getcwd()
        cmd = 'tell application "Terminal" to do script ' + \
            f'"cd {cwd}/{self.project} &&' + \
            'source {self.virtual_env}/bin/activate"' + ' in front window'

        # Execute shell & activate environment
        self.shell_manager.execute(['osascript', '-e', cmd], active=False)
        # TODO: execute shell for all operating systems

    def execute_package_scripts(self, script_name):
        package = read_json(self.PACKAGE_PATH)
        script = package["scripts"].get(script_name)
        if not script:
            raise ValueError(
                f"Please provide a {script_name} "
                f"script in to {self.PACKAGE_PATH}"
            )

        self.shell_manager.execute(script)

    def remove_previous_packages(self, package_name):
        for package_def, info in self.packages.copy().items():
            if info['name'] == package_name:

                res = self.shell_manager.execute(
                    [f"./{self.virtual_env}/bin/pip", "uninstall", "-y"
                     f"{package_name}"]
                )

                if res.returncode == 0:
                    print(f"{package_name} previous version removed!")
                    self.packages.pop(package_def)
                else:
                    raise ValueError(f"Previous version for {package_name}"
                                     "could not be removed")

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

    @ handle_errors
    @ load_package
    def cmd_install(self, packages):
        """Installs python packages"""
        first_use = False
        if not packages:
            first_use = True
            packages = self.packages.copy().keys()
            write_json(self.LOCK_PATH, self.to_dict)
        for package in packages:
            package_name, version = get_package_info(package)
            install_script = package_name if version == 'latest'\
                else f'{package_name}=={version}'

            if not first_use:
                self.remove_previous_packages(package_name)

            install_args = \
                f"./{self.virtual_env}/bin/pip install {install_script}"

            install_result = self.shell_manager.execute(install_args)

            if install_result.returncode != 0:
                raise ValueError("Not a valid package")

            pip_show_result = self.shell_manager.execute(
                f"./{self.virtual_env}/bin/pip show {package_name}"
            )

            info = get_version_info(pip_show_result.stdout)
            installed_version = info['version']
            package_def = f'{package_name}@{installed_version}'
            self.packages[package_def] = info
            print(f"{package_def} successfully installed!")
            write_json(self.PACKAGE_PATH, self.to_dict)
