from setuptools import setup, find_packages

setup(
    name="dirfetch",
    version="1.0.11",
    packages=find_packages(where='source'),  # Finds the source directory
    include_package_data=True,
    install_requires=[],
    entry_points={
        'console_scripts': [
            'dirfetch = source.main:main',  # The entry point for the CLI
        ],
    },
)
