#!/usr/bin/env python
from setuptools import setup


def readme():
    with open('readMe.rst') as f:
        return f.read()


setup(name='yahoo_fb_stat_analysis',
      version='5.0.2',
      description='Python module to allow for advanced statistical analysis',
      long_description=readme(),
      url='https://github.com/KipFeher85/Fantasy-Baseball',
      author='Kip Feher',
      author_email='kipfeher85@gmail.com',
      license='MIT',
      packages=['yahoo_fb_stat_analysis'],
      classifiers=[
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.9',
      ],
      install_requires=['yahoo_oauth', 'yahoo_fantasy_api', 'MLB-StatsAPI', 'pandas', 'datetime', 'lxml', 'python-dateutil', 'setuptools', 'requests', 'pip'],
      zip_safe=False)
