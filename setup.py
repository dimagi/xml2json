from __future__ import absolute_import
from __future__ import unicode_literals
from setuptools import setup

setup(
    name='xml2json',
    version='0.1.0',
    author='Danny Roberts',
    author_email='droberts@dimagi.com',
    description='A library for converting XML to JSON',
    long_description=open('README.md').read(),
    url='',
    packages=['xml2json'],
    install_requires=['lxml'],
    test_suite='test',
)
