"""
Setup script for AbuLang Browser Package
This allows the package to be installed in Pyodide
"""

from setuptools import setup, find_packages

setup(
    name="abulang-browser",
    version="4.0.0",
    description="AbuLang programming language for browser (Pyodide)",
    author="Abu",
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
