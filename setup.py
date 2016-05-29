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

setup(

	name				='PyForms-Web',
	version 			='0.1.5',
	description 		="""Pyforms is a Python 2.7 and 3.0 framework to develop GUI application, 
		which promotes modular software design and code reusability with minimal effort.""",
	author  			='Ricardo Ribeiro',
	author_email		='ricardojvr@gmail.com',
	license 			='MIT',

	download_urlname	='https://github.com/UmSenhorQualquer/pyforms',
	url 				='https://github.com/UmSenhorQualquer/pyforms',
	include_package_data=True,
	packages=[
		'pyforms_web',
		'pyforms_web.web',
		'pyforms_web.web.Controls', 
		'pyforms_web.web.django', 
		'pyforms_web.web.django.templatetags', 
		],
	package_data={'pyforms_web': [
			'web/django/*.js',
			'web/django/static/*.js',
			'web/django/static/jqplot/*.js',
			'web/django/static/jqplot/*.css',
			'web/django/static/jqplot/plugins/*.js',
			'web/django/static/pyformsjs/*.js']
		},

	install_requires=[
		"numpy >= 1.6.1",
		#"matplotlib"
	],
)