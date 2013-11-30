#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='remote-fixtures',
    version='0.1.0',
    description='Django remote fixture loading',
    author='Gizmag',
    author_email='tech@gizmag.com',
    url='https://github.com/gizmag/remote-fixtures',
    packages=find_packages(),
    install_requires=['django', 'boto', 'python-dateutil']
)
