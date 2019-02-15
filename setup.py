#!/usr/bin/env python

from distutils.core import setup

setup(name='Camera Sorter',
      version='1.0',
      description='Sorts camera pictures',
      author='Volodymyr Sereda',
      author_email='me@infraviolet.io',
      packages=['pytest'],
      package_dir={'src', 'test'}
     )