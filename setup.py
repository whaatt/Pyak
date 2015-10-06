# File: setup.py
# Pyak Install Script

from setuptools import setup
from setuptools import find_packages

setup(name ='pyak', # just run python setup.py install
      description = 'A Python client for the Yik Yak API',
      author = 'Jared Smith and Sanjay Kannan [maintainer]',
      version = '0.2.0',
      packages = find_packages(),
      package_data = {},
      include_package_data = True,
      install_requires = ['requests'],
      entry_points = {})
