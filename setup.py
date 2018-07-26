# -*- coding: utf-8 -*-
import io
import re
from setuptools import setup, find_packages

with io.open('lleida_net/__init__.py', 'rt', encoding='utf8') as f:
    version = re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)

with open(f'requirements.txt', 'r') as f:
    INSTALL_REQUIRES = f.readlines()

try:
    with open(f'requirements-dev.txt', 'r') as f:
        TESTS_REQUIRE = f.readlines()
except:
        TESTS_REQUIRE = None

try:
    with open("README.md", "r") as readmefile:
        long_description = readmefile.read()
except:
        long_description = None

setup(
    name='lleida_net',
    description='Python client desired to interact with the Click&Sign API',
    long_description=long_description,
    long_description_content_type="text/markdown",
    version=version,
    url='https://www.gisce.net',
    author='Xavi Torelló',
    author_email='xtorello@gisce.net',
    packages=find_packages(),
    install_requires=INSTALL_REQUIRES,
    tests_require=TESTS_REQUIRE,
    license='General Public Licence 3',
    provides=['lleida_net'],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6"
    ]
)
