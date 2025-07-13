#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name='wg-name',
    version='0.1.0',
    python_requires='>=3.2',
    packages=find_packages(),
    scripts=["wg-name", "wg-whois"],
)
