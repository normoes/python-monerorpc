#!/usr/bin/env python

from setuptools import setup

__version__ = "v0.6.0"

setup(
    name="python-monerorpc",
    version=__version__,
    description="Enhanced version of python-jsonrpc for Monero (monerod, monero-wallet-rpc).",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Norman Moeschter-Schenck",
    author_email="<norman.moeschter@gmail.com>",
    maintainer="Norman Moeschter-Schenck",
    maintainer_email="<norman.moeschter@gmail.com>",
    url="https://www.github.com/monero-ecosystem/python-monerorpc",
    download_url=f"https://github.com/monero-ecosystem/python-monerorpc/archive/{__version__}.tar.gz",
    packages=["monerorpc"],
    install_requires=["requests>=2.24.0"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
