# -*- coding: utf-8 -*-
import io
import re
from setuptools import setup, find_packages

with io.open('lleida_net/__init__.py', 'rt', encoding='utf8') as f:
    version = re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)

INSTALL_REQUIRES = ['Munch', 'Marshmallow']

setup(
    name='lleida_net',
    description='Python client desired to interact with the Click&Sign API',
    version=version,
    url='https://www.gisce.net',
    author='Xavi Torelló',
    author_email='xtorello@gisce.net',
    packages=find_packages(),
    install_requires=INSTALL_REQUIRES,
    license='General Public Licence 3',
    provides=['lleida_net'],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6"
    ]
)
