#!/usr/bin/env python

from setuptools import setup, find_packages
import os

ZTHREADS_CYTHON = os.getenv("Zsql_CYTHON", None)


if ZTHREADS_CYTHON:
    from Cython.Build import cythonize
    cythonkw = {
        "ext_modules": cythonize(
            ["zsql/zmodel.py",
             "zsql/zhandle.py"
             ])
    }
else:
    cythonkw = {}
try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    long_description = ''


setup(
    name='zsql',
    version='1.00',
    description='A Python Interface to TDX protocol',
    long_description=long_description,
    author='allisnone',
    author_email='i@allisnone.cc',
    url='https://github.com/allisnone/zsql',
    packages=find_packages(),
    install_requires=[
            'sqlalchemy',
            #'shutil',
            #'hashlib',
    ],
    entry_points={
          'console_scripts': [
              'test=zsql_session:main',
          ]
      },
    **cythonkw
    )

