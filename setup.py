#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__      = "Ricardo Ribeiro"
__credits__     = ["Ricardo Ribeiro"]
__license__     = "MIT"
__version__     = '0.1.5'
__maintainer__  = "Ricardo Ribeiro"
__email__       = "ricardojvr@gmail.com"
__status__      = "Production"




from setuptools import setup
import os, fnmatch


def find_files(package_name,directory, pattern):
    for root, dirs, files in os.walk(os.path.join(package_name, directory)):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                filename = os.path.join(root[len(package_name)+1:], basename)
                yield filename

setup(

	name				='PyForms-Web',
	version 			='0.1.5',
	description 		="""Pyforms is a Python 2.7 and 3.0 framework to develop GUI application,
		which promotes modular software design and code reusability with minimal effort.""",
	author  			='Ricardo Ribeiro',
	author_email		='ricardojvr@gmail.com',
	license 			='MIT',

	url 				='https://github.com/UmSenhorQualquer/pyforms',
	include_package_data=True,
	packages=[
		'pyforms_web',
		'pyforms_web.web',
		'pyforms_web.web.storage',
		'pyforms_web.web.Controls',
		'pyforms_web.web.djangoapp',		
		'pyforms_web.web.djangoapp.model_admin',
		'pyforms_web.web.djangoapp.middleware',
		'pyforms_web.web.djangoapp.templatetags',
		],
	package_data={'pyforms_web':
		list(find_files('pyforms_web','web/djangoapp/static/', '*.*'))+list(find_files('pyforms_web','web/djangoapp/templates/', '*.*'))
		},

	install_requires=[
		#"numpy >= 1.6.1",
		#"matplotlib"
	],
)
