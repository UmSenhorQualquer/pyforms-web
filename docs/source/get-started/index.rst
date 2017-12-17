================
Get started
================

Download and prepare the environment.
-------------------------------------------

.. code::
    
    pip install git+https://bitbucket.org/UmSenhorQualquer/pyforms-web.git
    pip install git+https://bitbucket.org/UmSenhorQualquer/orquetra
    

Create a django project.
------------------------------

.. code::

    django-admin startproject mysite


Add the next applications in the django project **setting.py** file.

.. code:: python

    INSTALLED_APPS = [
        ...
        
        'jfu',
        'sorl.thumbnail',
        'orquestra',
        'pyforms_web.web.django_pyforms',

        ...
    ]

Write your first app.
------------------------------



Run & test the app.
------------------------------


