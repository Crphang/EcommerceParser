#!/usr/bin/env python

from setuptools import setup

setup(name='EcommerceParser',
      version='0.01',
      description='HTML Parser for HTML Dumps from Ecommerce Sites',
      author='Phang Chun Rong',
      author_email='chunrong@u.nus.edu',
      license='MIT',
      install_requires=[
          'beautifulsoup4'
      ],
      zip_safe=False
     )
