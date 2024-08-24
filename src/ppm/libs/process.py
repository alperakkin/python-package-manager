import subprocess


class Shell:
    def __init__(self, shell='sh'):
        self.proc = None
        self.shell = shell

    def execute(self, cmd):
        subprocess.run(cmd, shell=True)
