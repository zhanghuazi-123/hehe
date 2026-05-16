from setuptools import setup, find_namespace_packages

setup(
    name="cli-anything-bailongma",
    version="0.1.0",
    description="CLI harness for Bailongma - AI consciousness experiment framework",
    author="CLI-Anything",
    packages=find_namespace_packages(include=["cli_anything.*"]),
    install_requires=[
        "click>=8.0",
    ],
    entry_points={
        "console_scripts": [
            "bailongma=cli_anything.bailongma.bailongma_cli:main",
            "cli-anything-bailongma=cli_anything.bailongma.bailongma_cli:main",
        ],
    },
    python_requires=">=3.10",
)
