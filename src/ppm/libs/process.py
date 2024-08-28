import subprocess
import platform
import os


class Shell:
    def __init__(self, shell='sh'):
        self.proc = None
        self.shell = shell
        self.system = platform.system()

    def activate_virtual_env(self, project, virtual_env):
        script = ""
        cwd = os.getcwd()
        match self.system:
            case 'Darwin' | 'Linux':
                script = f'"cd {cwd}/{project} && source\
                      {virtual_env}/bin/activate"'
            case 'Windows':
                script = f'"cd {cwd}/{project} &&\
                      {virtual_env}\\Scripts\\activate"'
            case _:
                raise ValueError("Can not create activation script")

        self.terminal_script(script)

    def terminal_script(self, script):
        match self.system:
            case 'Darwin':
                script = 'tell application "Terminal" to do script ' + \
                    script + ' in front window'
                self.execute(['osascript', '-e', script], active=False)
            case 'Linux':
                self.execute(['gnome-terminal', '--', 'bash', '-c', script],
                             active=False)
            case 'Windows':
                subprocess.run(['start', 'cmd', '/k', script], active=False)
            case '_':
                raise ValueError("Can not execute terminal due to unknown OS!")

    def execute(self, cmd, active=True):
        return subprocess.run(cmd, stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT, timeout=10,
                              shell=active)
