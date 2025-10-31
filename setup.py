"""Setup configuration for Anada.

This file is kept for backward compatibility.
Modern Python projects should use pyproject.toml instead.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="anada",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Terminal-based Obsidian-like note-taking tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/anada",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "anada=anada.cli:cli",
        ],
    },
    include_package_data=True,
)

