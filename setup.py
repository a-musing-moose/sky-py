#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='sky',
    version='0.0.1',
    url='https://github.com/a-musing-moose/sky-py',
    author="Jonathan Moss",
    author_email="jonathan.moss@tangentsnowball.com.au",
    description="Python client for skydb",
    long_description=open('README.rst').read(),
    keywords="skydb, behavioral database",
    license='BSD',
    packages=find_packages(exclude=['tests','sandbox']),
    install_requires=[
        'requests',
        'pytz'
    ],
    # See http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: pypy',
    ]
)
