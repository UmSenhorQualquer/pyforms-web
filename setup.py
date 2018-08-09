#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os, fnmatch, re

version = ''
license = ''
with open('pyforms_web/__init__.py', 'r') as fd:
    content = fd.read()
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', content, re.MULTILINE).group(1)

    license = re.search(
        r'^__license__\s*=\s*[\'"]([^\'"]*)[\'"]', content, re.MULTILINE).group(1)

if not version: raise RuntimeError('Cannot find version information')
if not license: raise RuntimeError('Cannot find license information')


def find_files(package_name,directory, pattern):
    for root, dirs, files in os.walk(os.path.join(package_name, directory)):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                filename = os.path.join(root[len(package_name)+1:], basename)
                yield filename

with open('README.md', 'r') as fd:
    long_description = fd.read()

setup(
    name                 = 'PyForms-Web',
    version              = version,
    description          = """Pyforms Web is Python 3 framework to create single-page web applications.""",
    author               = 'Ricardo Ribeiro',
    author_email         = 'ricardojvr@gmail.com',
    license              = license,
    url                  = 'https://github.com/UmSenhorQualquer/pyforms-web',
    
    long_description     = long_description,
    long_description_content_type = 'text/markdown',
    
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

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        
        'Topic :: Software Development :: Build Tools',
        
        'Programming Language :: Python :: 3',

        'Environment :: Web Environment',

        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Unix',

        'Topic :: Artistic Software',
        'Topic :: Games/Entertainment',
        'Topic :: Multimedia :: Graphics :: 3D Rendering',
        'Topic :: Multimedia :: Graphics :: Capture :: Digital Camera',
        'Topic :: Multimedia :: Graphics :: Presentation',
        'Topic :: Multimedia :: Graphics :: Viewers',
        'Topic :: Multimedia :: Video :: Display',
        'Topic :: Scientific/Engineering :: Human Machine Interfaces',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: User Interfaces',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Browsers',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Content Management System',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
        'Topic :: Internet :: WWW/HTTP :: Site Management :: Link Checking',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Server',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Widget Sets',

        'Framework :: Django :: 2.0'
    ],



    keywords='web development single-page-application pyforms'
)
