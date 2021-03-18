# Copyright 2021, Ryan P. Kelly.

from setuptools import setup


setup(
    name="fatpacker",
    version="0.1",
    description="package python applications as standalone scripts",
    author="Ryan P. Kelly",
    author_email="ryan@ryankelly.us",
    url="https://github.com/f0rk/fatpacker",
    install_requires=[
        "spindrift",
    ],
    tests_require=[
        "pytest",
    ],
    package_dir={"": "lib"},
    packages=["fatpacker"],
    scripts=["tools/fatpacker"],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Libraries",
    ],
)
