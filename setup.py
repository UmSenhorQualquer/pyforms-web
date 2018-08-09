#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os, fnmatch, re

version = ''
license = ''
with open('pyforms_web/__init__.py', 'r') as fd:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(), re.MULTILINE).group(1)

    license = re.search(
        r'^__license__\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(), re.MULTILINE).group(1)

if not version: raise RuntimeError('Cannot find version information')
if not license: raise RuntimeError('Cannot find license information')


def find_files(package_name,directory, pattern):
    for root, dirs, files in os.walk(os.path.join(package_name, directory)):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                filename = os.path.join(root[len(package_name)+1:], basename)
                yield filename


setup(
    name                 = 'PyForms-Web',
    version              = version,
    description          = """Pyforms Web is Python 3 framework to create single-page web applications.""",
    author               = 'Ricardo Ribeiro',
    author_email         = 'ricardojvr@gmail.com',
    license              = license,
    url                  = 'https://github.com/UmSenhorQualquer/pyforms-web',
    include_package_data = True,
    packages=find_packages(),
    package_data={
        'pyforms_web':
        list( find_files('pyforms_web','web/static/', '*.*') )
    },
    install_requires=[
        'django-jfu-pyforms',
        'orquestra',
        'numpy',
        'opencv-python',
        'django>2.0',
        'simplejson',
        'sorl-thumbnail',
        'dill',
        'filelock',
        'Pillow',
        'python-dateutil',
        'confapp'
    ],
)
