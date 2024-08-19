from ppm.libs.utils import write_json


class Command:
    def __init__(self):
        self.map = {

            "init": {
                "command": self.init,
                "help": "Initialize Package",

            },
            "run": {
                "command": self.run,
                "help": "Executes Predefined Script",

            },
            "start": {
                "command": self.start,
                "help": "Executes Start Script",

            }
        }

    def __dict__(self):
        return self.COMMANDS_MAP

    def start(self, script):
        NotImplementedError(script)

    def init(self, package):
        for key, val in package.copy().items():
            if isinstance(val, str):
                out = input(f"{key}: {val}")
                package[key] = val + out
        write_json("package.json", package)

    def run(self, script):
        NotImplementedError(script)
