from setuptools import setup, find_packages

setup(
    name="dirfetch",
    version="1.0.14",
    packages=find_packages(where='source'),
    include_package_data=True,
    package_dir={'': 'source'},  # Tell setuptools where the source files are
    install_requires=[],
    entry_points={
        'console_scripts': [
            'dirfetch = source.main:main',  # Fix: Correct path to main.py
        ],
    },
)
