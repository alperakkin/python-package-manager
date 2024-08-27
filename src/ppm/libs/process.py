import subprocess


class Shell:
    def __init__(self, shell='sh'):
        self.proc = None
        self.shell = shell

    def execute(self, cmd, active=True):
        return subprocess.run(cmd, stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT, timeout=10,
                              shell=active)
