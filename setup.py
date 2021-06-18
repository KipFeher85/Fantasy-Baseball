#!/usr/bin/env python

from setuptools import setup


def readme():
    with open('readMe.rst') as f:
        return f.read()

setup(name='yahoo_fantasy_baseball_stat_analysis',
      version='0.1',
      description='Python module to allow for advanced statistical analysis',
      long_description=readme(),
      url='http://github.com/kipfeher85/yahoo_fantasy_baseball_stat_analysis',
      author='Kip Feher',
      author_email='kipfeher85@gmail.com',
      license='MIT',
      packages=['yahoo_fantasy_baseball_stat_analysis'],
      classifiers=[
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.7',
      ],
      install_requires=['yahoo_oauth', 'yahoo_fantasy_api', 'statsapi'],
      zip_safe=False,
      )