from setuptools import setup, find_packages

setup(
    name="dirfetch",
    version="1.0.13",
    packages=find_packages(where='source'),
    include_package_data=True,
    package_dir={'': 'source'},  # Tell setuptools where the source files are
    install_requires=[],
    entry_points={
        'console_scripts': [
            'dirfetch = main:main',  # main function inside the main.py file
        ],
    },
)
