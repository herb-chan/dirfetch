from setuptools import setup, find_packages

setup(
    name="dirfetch",
    version="1.0.22",
    description="Dirfetch",
    author="herb",
    packages=find_packages(where="source"),
    package_dir={"": "source"},  # Map the root package to "source"
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "dirfetch=source.main:main",  # Adjusted import path to look inside "source"
        ],
    },
)
