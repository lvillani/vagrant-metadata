#!/usr/bin/env python

from setuptools import setup

setup(
    name="vagrant-metadata",
    version="1.1.2",
    description="Vagrant metadata.json generator",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/lvillani/vagrant-metadata/",
    author="Lorenzo Villani",
    author_email="lorenzo@villani.me",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
    ],
    scripts=["bin/vagrant-metadata"],
    py_modules=["vagrant_metadata"],
)
