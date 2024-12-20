from setuptools import setup, find_packages

setup(
    name="dirfetch",
    version="1.0.0",
    author="herb",
    author_email="",
    description="A customizable directory-fetching tool like neofetch",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/herb-chan/dirfetch",
    packages=find_packages(where="source"),
    package_dir={"": "source"},
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=[
        "rich",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "dirfetch=main:main",  # Run with `dirfetch` in terminal
        ],
    },
)
