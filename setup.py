from setuptools import setup, find_packages

setup(
    name="dirfetch",
    version="1.0.16",
    packages=find_packages(),
    package_dir={"": "source"},  # Corrects where the modules are
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "dirfetch = source.main:main",
        ],
    },
)
