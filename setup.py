from setuptools import setup, find_packages

setup(
    name="dirfetch",
    version="1.0.17,
    packages=find_packages("source"),
    package_dir={"": "source"},  # Map the root of the packages to "source"
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "dirfetch = main:main",  # Directly reference the `main` function in `main.py`
        ],
    },
)
