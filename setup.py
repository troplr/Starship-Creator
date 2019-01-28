#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="requirements.txt",
    version="0.1",
    author="James Brown",
    author_email="Roguelazer@gmail.com",
    url="https://github.com/troplr/Starship-Creator/requirements.txt",
    license="MIT",
    packages=find_packages(exclude=['tests']),
    keywords=["troll"],
    description="making your pip installs do something",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ]
)