#!/usr/bin/python3

import os
import sys

from setuptools import find_packages
from setuptools import setup
from setuptools.command.install import install

NAME = 'f8a_tagger'


def get_requirements():
    with open('requirements.txt') as fd:
        return fd.read().splitlines()


if sys.version_info[0] != 3:
    sys.exit("Python3 is required in order to install f8a_tagger")


setup(
    name=NAME,
    version='0.1',
    packages=find_packages(),
    package_data={
        'f8a_tagger': [
            os.path.join('data', '*.yaml'),
            os.path.join('data', '*.txt')
        ]
    },
    install_requires=get_requirements(),
    scripts=['f8a_tagger_cli.py'],
    author='Fridolin Pokorny',
    author_email='fridolin@redhat.com',
    maintainer='Fridolin Pokorny',
    maintainer_email='fridolin@redhat.com',
    description='Natural language processing for keyword extraction',
    url='https://github.com/fabric8-analytics/fabric8-analytics-tagger',
    license='ASL 2.0',
    keywords='tags topics keywords',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy"
    ]
)
