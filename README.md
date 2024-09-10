# python-package-manager

NPM like package manager written for Python built on Python Pip module


## Install

Download the repo
```sh

$ git clone https://github.com/alperakkin/python-package-manager.git

```

Change current directory to python-package-manager folder

```sh

$ cd python-package-manager
```

Run pip install to install the ppm module

```sh

$> pip install .
```


This commands will install ppm as a package to your local environment.

You can set an alias to use ppm directly

On Windows:

```cmd

C:\> doskey ppm="python -m ppm"
```

On MacOs & Linux:

```sh

$> alias ppm=python -m ppm
```


## Quick Start

### Init
To initialize a new Python project

```bash
$> ppm init
```
ppm will ask you to fill up some information about the project as it follows:

Project Name: Give a name describing you project
Author: Author of your project
Author URL: Web Page of the author
Version: Project Version
Virtual Environment: Python environment name to be created
Env File: Creates .env file
Shell: Project runs on given shell
Module: Select installed Python executable for the project virtual environment

```sh
project:  -> My_Project
author:  -> John Doe
author_url:  -> https://github.com/johndoe/myproject
version: 1.0.0 ->
virtual_env:  -> my_venv
env_file: .env ->
shell: cmd -> sh
module: python ->
```

After entering the required project information, ppm will create a project folder, changes cd
to the project folder and activates the virtual environment.

In the project folder files named "pyconfig.json" and ".env"  will be created.

```plaintext
My_Project  
    ├── my_venv  
    ├── .env  
    ├── pyconfig.json  
  
```


```sh
(my_env) $ ~/My_Project >
```

### Install Dependencies

If you previously created a project you can just type the following command to install all dependencies


```sh
$ ~/My_Project > python -m ppm install
```

If you just initialized a new project you can  simply type a requirement with/without version
as it is shown below:


```sh
# To install elasticsearch package
$ ~/My_Project > python -m ppm install elasticsearch@8.15.0
```

Elasticsearch dependency automatically added to project config file as shown below:

```json
{
    "project": "My_Project",
    "author": "",
    "author_url": "",
    "version": "1.0.0",
    "virtual_env": "my_venv",
    "env_file": ".env",
    "scripts": {
        "start": "",
        "build": "",
        "test": ""
    },
    "shell": "cmd",
    "module": "python",
    "packages": {
        "elasticsearch@8.15.0": {
            "name": "elasticsearch",
            "version": "8.15.0",
            "summary": "Python client for Elasticsearch",
            "home_page": "https://github.com/elastic/elasticsearch-py",
            "author": "",
            "author_email": "Elastic Client Library Maintainers <client-libs@elastic.co>",
            "license": "",
            "location": "My_Project/my_env/Lib/site-packages",
            "requires": "elastic-transport",
            "required_by": ""
        }
    }
}
```

### Scripting

#### Start
It is possible to define a start script for your project

Assuming you have a project structure as shown below:

```plaintext
My_Project  
    ├── my_venv  
    ├── .env  
    ├── pyconfig.json  
    └── src  
        └── main.py  
```
  

Add your start script to pyconfig.json

```json
{
    "project": "My_Project",
    "author": "",
    "author_url": "",
    "version": "1.0.0",
    "virtual_env": "my_venv",
    "env_file": ".env",
    "scripts": {
        "start": "python src/main.py arg1 arg2",
        "build": "",
        "test": ""
    },
    "shell": "cmd",
    "module": "python",
    "packages": {
        "elasticsearch@8.15.0": {
            "name": "elasticsearch",
            "version": "8.15.0",
            "summary": "Python client for Elasticsearch",
            "home_page": "https://github.com/elastic/elasticsearch-py",
            "author": "",
            "author_email": "Elastic Client Library Maintainers <client-libs@elastic.co>",
            "license": "",
            "location": "My_Project/my_env/Lib/site-packages",
            "requires": "elastic-transport",
            "required_by": ""
        }
    }
}
```
Then just type

```sh
(my_env) $ ~/My_Project > ppm start
Hello World
```

Your project will be started automatically

To build & test your project you can define related scripts to "build" and "test" keys in pyconfig.json file

You can define any shell script to your scripting keys.

```json
{
    "project": "My_Project",
    "author": "",
    "author_url": "",
    "version": "1.0.0",
    "virtual_env": "my_venv",
    "env_file": ".env",
    "scripts": {
        "start": "echo Hello World!",
        "build": "",
        "test": ""
    },
    "shell": "sh",
    "module": "python",
    "packages": {
        "elasticsearch@8.15.0": {
            "name": "elasticsearch",
            "version": "8.15.0",
            "summary": "Python client for Elasticsearch",
            "home_page": "https://github.com/elastic/elasticsearch-py",
            "author": "",
            "author_email": "Elastic Client Library Maintainers <client-libs@elastic.co>",
            "license": "",
            "location": "My_Project/my_env/Lib/site-packages",
            "requires": "elastic-transport",
            "required_by": ""
        }
    }
}
```

```sh
(my_env) $ ~/My_Project > ppm start
Hello World!
```

#### Run

You can run any shell script by typing

```sh
(my_env) $ ~/My_Project > ppm run "echo Hello World!"
Hello World!
```

### Get Project Info
#### Package Info
To get the package info, type:
```sh
$ (my_env) $ ~/My_Project > ppm list packages

{'pandas@2.0.3': {'name': 'pandas',
                  'version': '2.0.3',
                  'summary': 'Powerful data structures for data analysis, time '
                             'series, and statistics',
                  'home_page': '',
                  'author': '',
                  'author_email': 'The Pandas Development Team '
                                  '<pandas-dev@python.org>',
                  'license': 'BSD 3-Clause License',
                  'location': '/Users/alperakkin/Documents/alper/new_project/test/lib/python3.8/site-packages',
                  'requires': 'numpy, python-dateutil, pytz, tzdata',
                  'required_by': ''},
 'numpy@1.24.4': {'name': 'numpy',
                  'version': '1.24.4',
                  'summary': 'Fundamental package for array computing in '
                             'Python',
                  'home_page': 'https://www.numpy.org',
                  'author': 'Travis E. Oliphant et al.',
                  'author_email': '',
                  'license': 'BSD-3-Clause',
                  'location': '/Users/alperakkin/Documents/alper/new_project/test/lib/python3.8/site-packages',
                  'requires': '',
                  'required_by': 'pandas'}}
```

#### Env Info
To get the environement file info, type:

```sh
$ (my_env) $ ~/My_Project > ppm list env
env=PROD
username=johndoe
email=johndoe@acme.com
```
## Dependencies
Python 3.12 and above
