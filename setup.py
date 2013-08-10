#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='atlas',
      version='1.0',
      description='Atlas is aimed to be a lightweight, fast and generic python interface to Titan DB.',
      author='Alexandre Valette',
      author_email='alexandre.valette@snips.net',
      packages=find_packages(exclude=['*test*']),
     )