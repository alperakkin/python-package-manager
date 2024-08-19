
import argparse

from ppm.libs.commands import Command

command = Command()


template = {
    "author": "",
    "author-url": "",
    "license": "",
    "version": "1.0.0",
    "virtual-env": "",
    ".env": "",
    "scripts": {
        "start": "",
        "build": "",
        "test": ""
    },
    "shell": "sh",
    "module": "python",
    "packages": {},
}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="PPM", description="Python Package Manager"
    )
    subparsers = parser.add_subparsers(title="Commands", dest="command")
    for arg, meta in command.map.items():
        command_parser = subparsers.add_parser(arg,
                                               help=meta["help"])
        command_parser.set_defaults(func=meta['command'])

args = parser.parse_args()

if args.command == 'init':
    args.func(template)
