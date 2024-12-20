from setuptools import setup, find_packages

setup(
    name="dirfetch",
    version="1.0.12",
    packages=find_packages(where='source'),  # Ensures source directory is included
    include_package_data=True,
    install_requires=[],
    package_dir={"": "source"},  # This tells setuptools where to find your package
    entry_points={
        'console_scripts': [
            'dirfetch = main:main',  # Entry point should be from the main module
        ],
    },
)
