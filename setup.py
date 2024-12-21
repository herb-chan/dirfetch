from setuptools import setup

setup(
    name="dirfetch",
    version="1.0.24",
    description="Dirfetch",
    author="herb",
    py_modules=["main"],  # Specify main.py as the module
    include_package_data=True,
    install_requires=[
        "rich",
    ],
    entry_points={
        "console_scripts": [
            "dirfetch=main:main",  # Adjusted to import directly from main.py
        ],
    },
)
