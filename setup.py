from setuptools import find_packages, setup

setup(
    name="task-tracker-cli",
    version="1.0.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "task-cli=src.main:main",
        ],
    },
)
