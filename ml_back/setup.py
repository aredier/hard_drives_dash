#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('requirements.txt') as requirements_file:
    requirements = list(requirements_file.readlines())

setup(
    author='Antoine Redier',
    author_email='antoine.redier2@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    entry_points={
        'console_scripts': [
            'ml_back=ml_back.cli:main',
        ],
    },
    install_requires=requirements,
    license='GNU General Public License v3',
    include_package_data=True,
    name='ml_back',
    packages=find_packages(include=['ml_back']),
    zip_safe=False,
)
