#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name='wgnamed',
    version='0.1.0',
    python_requires='>=3.2',
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "wg-names=wgname.name:main",
            "wg-whois=wgname.whois:main",
        ],
    }
)
