from setuptools import setup, find_packages

setup(
    name="dirfetch",
    version="1.0.21",
    description="Dirfetch",
    author="herb",
    packages=find_packages(where="source"),  # Look for packages inside "source"
    package_dir={"": "source"},  # Map the root package to "source"
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "dirfetch=main:main"
        ],  # Use "main" directly if it’s in the root of "source"
    },
)
