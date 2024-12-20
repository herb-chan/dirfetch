from setuptools import setup, find_packages

setup(
    name='dirfetch',
    version='1.0.8',
    packages=find_packages(where='source'),
    install_requires=[
        # List any dependencies here (e.g., 'requests')
    ],
    entry_points={
        'console_scripts': [
            'dirfetch=source.main:main',  # Assumes 'main.py' has a function 'main()'
        ],
    },
)
