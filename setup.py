#!/usr/bin/env python3
"""
Setup script for mufetch Python version
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="mufetch",
    version="1.0.0",
    author="Python port of mufetch by ashish0kumar",
    description="Neofetch-style CLI for music",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ashish0kumar/mufetch",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: System :: System Shells",
        "Topic :: Terminals",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "mufetch=mufetch:main",
        ],
    },
    include_package_data=True,
)
