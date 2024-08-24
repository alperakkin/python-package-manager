
import argparse

from ppm.libs.manager import PackageManager

pkg_manager = PackageManager()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="PPM", description="Python Package Manager"
    )
    subparsers = parser.add_subparsers(title="Commands", dest="command")
    for func in dir(pkg_manager):
        if func.startswith("cmd_"):
            func_name = pkg_manager.get_func_name(func)
            cmd = getattr(pkg_manager, func)
            doc = cmd.__doc__

            command_parser = subparsers.add_parser(func_name,
                                                   help=doc)
            command_parser.set_defaults(func=cmd)

    args = parser.parse_args()

    match args.command:
        case "init":
            args.func()
        case "start":
            args.func()
        case "run":
            args.func("script")
        case _:
            parser.print_help()
