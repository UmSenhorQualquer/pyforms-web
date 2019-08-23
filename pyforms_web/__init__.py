#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__      = "Ricardo Ribeiro"
__credits__     = ["Ricardo Ribeiro"]
__license__     = 'GNU GPLv3'
__version__ = "4.1.4"
__maintainer__  = "Ricardo Ribeiro"
__email__       = "ricardojvr@gmail.com"
__status__      = "Development"


from confapp import conf;
conf += 'pyforms_web.settings'

#force the load of the local settings if exists
try:
    import local_settings
    conf += local_settings
except:
    pass
