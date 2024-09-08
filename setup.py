from setuptools import setup, find_packages

setup(
    name="ppm",
    version="1.0",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[],
    author="Alper Akkın",
    description="NPM like package manager to build projects",
)
