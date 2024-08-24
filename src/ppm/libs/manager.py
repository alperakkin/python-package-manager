from pathlib import Path

from ppm.libs.utils import write_json, handle_errors
from ppm.libs.process import Shell


class PackageManager:
    PACKAGE_FILE = "pyconfig.json"

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
        env_path = Path(self.project) / self.virtual_env
        self.shell_manager.execute(f"python -m venv {env_path}")
        # TODO: Activate the virtual environment here
        # TODO: Set project file as active dir

    @ handle_errors
    def cmd_start(self):
        """Executes start script"""

        raise NotImplementedError("PPM Start not impleneted yet")

    @ handle_errors
    def cmd_init(self):
        """Initializes a new project"""

        for key, val in self.to_dict.items():
            if isinstance(val, str):
                out = input(f"{key}: {val} -> ")
                setattr(self, key, out or val)
                self.validate(key)

        package_path = Path(self.project) / Path(self.PACKAGE_FILE)
        write_json(package_path, self.to_dict)
        self.eval_package()

    @ handle_errors
    def cmd_run(self, script):
        """Executes predefined script"""
        raise NotImplementedError(script)
