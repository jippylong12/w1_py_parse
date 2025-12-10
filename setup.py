from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="w1_py_parse",
    version="0.12.0",
    description="Parser for Texas RRC W-1 data files",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Marcus Salinas",
    packages=find_packages(),
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
