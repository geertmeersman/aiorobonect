"""Setuptools for aiorobonect."""

import setuptools

with open("README.md") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aiorobonect",
    author="Geert Meersman",
    author_email="geertmeersman@gmail.com",
    description="Module to communicate to the Robonect API",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/geertmeersman/aiorobonect",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    install_requires=[],  # no runtime dependencies
    version="v1.3.1",
)
