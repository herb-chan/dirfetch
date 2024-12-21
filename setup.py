from setuptools import setup, find_packages

setup(
    name="dirfetch",
    version="1.0.20",
    description="Dirfetch",
    author="herb",
    packages=find_packages(include=["source", "source.*"]),
    package_dir={"": "source"},  # Map the root of the packages to "source"
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": ["dirfetch=source.main:main"],
    },
)
