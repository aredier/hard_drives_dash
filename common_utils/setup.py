#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('requirements.txt') as requirements_file:
    requirements = list(requirements_file.readlines())

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', 'numpy', 'scikit-learn']

setup(
    author='Antoine Redier',
    author_email='antoine.redier2@gmail.com',
    description='utils for all the different python modules',
    install_requires=requirements,
    license='GNU General Public License v3',
    long_description=readme + '\n\n',
    include_package_data=True,
    name='common_utils',
    packages=find_packages(include=['common_utils']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    zip_safe=False,
)
