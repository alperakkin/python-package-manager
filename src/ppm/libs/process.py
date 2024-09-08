import subprocess
import platform
import os


class Shell:
    def __init__(self, shell='cmd'):
        self.proc = None
        self.shell = shell
        self.system = platform.system()

    def activate_virtual_env(self, project, virtual_env):
        script = ""
        cwd = os.getcwd()
        match self.system:
            case 'Darwin' | 'Linux':
                script = f'"cd {cwd}/{project} && source {virtual_env}/bin/activate"'
            case 'Windows':
                script = rf'cd {cwd}\{project} &&  {virtual_env}\Scripts\activate.bat'
            case _:
                raise ValueError("Can not create activation script")

        self.terminal_script(script)

    def install_package(self, virtual_env, package):
        script = ""
        output = None
        match self.system:
            case 'Darwin' | 'Linux':
                script = f"./{virtual_env}/bin/pip install {package}"
                output = self.execute(script)
            case 'Windows':
                script = rf'{virtual_env}\Scripts\pip install {package}'
                output = self.execute(script, {'shell': True})
            case _:
                raise ValueError("Can execute install script")
        if output.returncode != 0:
                raise ValueError("Not a valid package")

    def show_package(self, virtual_env, package):
        script = ""
        output = None
        match self.system:
            case 'Darwin' | 'Linux':
                script =  f"./{self.virtual_env}/bin/pip show {package}"
                output =  self.execute(script)
            case 'Windows':
                script = rf'{virtual_env}\Scripts\pip show {package}'
                output = self.execute(['cmd', '/c', script])
            case _:
                raise ValueError("Can execute package show script")
        return output.stdout


    def terminal_script(self, script):
        match self.system:
            case 'Darwin':
                script = 'tell application "Terminal" to do script ' + \
                    script + ' in front window'
                self.execute(['osascript', '-e', script])
            case 'Linux':
                self.execute(['gnome-terminal', '--', 'bash', '-c', script])
            case 'Windows':
                self.execute(['cmd', '/k', script], {'shell': True})
            case '_':
                raise ValueError("Can not execute terminal due to unknown OS!")

    def execute(self, cmd,  kwargs={
                                'shell': False,
                                'stdout':subprocess.PIPE,
                                'stderr':subprocess.PIPE}):
        return subprocess.run(cmd, **kwargs)
   
