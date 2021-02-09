********************
Install & configure
********************

On this page it is explained how to configure your environment and your django app to start using pyforms.

.. note:: The instructions on this page assumes you know how the `Django framework <https://www.djangoproject.com/>`_ works.

Configure the environment
==========================

* Install Pyforms using **pip**.

.. code:: bash

    pip install pyforms-web


Configure a django project
===========================

Execute the next command in the terminal to start a Django project.

.. code:: bash

    django-admin startproject <project-name>

Edit the django project **settings.py** file to include the next configurations.

.. code:: python

    INSTALLED_APPS = [
        'orquestra',
        'pyforms_web.web',
        'jfu',
        'sorl.thumbnail',
        ...
    ]

    MIDDLEWARE = [
        ...
        'pyforms_web.web.middleware.PyFormsMiddleware'
    ]


Edit the django project **urls.py** file to include the next urls configurations.


.. code:: python

    from django.conf    import settings
    from django.contrib import admin
    from django.urls    import include, path

    urlpatterns = [
        path('pyforms/',  include('pyforms_web.web.urls') ),
        path('',          include('orquestra.urls')       ),
    ]

    if settings.DEBUG:
        from django.conf.urls.static import static
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


Create a pyforms settings file
================================

In the django project root folder (same folder of the manage.py file) create the local_settings.py file with the next content.

.. code:: python

   SETTINGS_PRIORITY = 0 # Will define this settings file as priority. Will override all the settings with lower priority.
   PYFORMS_MODE = 'WEB' # Will configure pyforms to run as WEB mode.




Run the project
================

.. code:: bash

    cd <project-name>
    python3 manage.py migrate
    python3 manage.py runserver


Access to `http://localhost:8000 <http://localhost:8000/>`_ 

.. image:: /_static/imgs/demo-app.png
    :width: 100%
    :align: center

|

------------------------------

(optional)

Configure django-allauth
=========================

django-allauth is a reusable Django app that allows for both local and social authentication, with flows that just work.

To make it work with Orquestra follow the instructions described `@django-allauth documentation 
<http://django-allauth.readthedocs.io/en/latest/installation.html>`_.

Typical django-allauth configuration
______________________________________

.. code:: shell

    pip install django-allauth


Add the next configuration to your Django project setttings.

.. code:: python

    ...

    INSTALLED_APPS = [
        ...
        'allauth',
        'allauth.account',
        'allauth.socialaccount',
        'allauth.socialaccount.providers.google',
        'django.contrib.sites',
        ...
    ]

    AUTHENTICATION_BACKENDS = [
        'django.contrib.auth.backends.ModelBackend',
        'allauth.account.auth_backends.AuthenticationBackend',
    ]

    LOGIN_URL = '/accounts/login/'
    LOGIN_REDIRECT_URL = '/'

Edit the urls.py file to add the next code.

.. code:: python

    from django.urls import path

    urlpatterns = [
        path(r'^accounts/', include('allauth.urls')),
        ...
    ]

Add the next configuration to the **local_settings.py** file to configure **orquestra** to require always authentication before accessing the applications.

.. code:: python

   ORQUESTRA_REQUIREAUTH = True

.. note::
   
   Do not forget to apply the db migrations to your project.

Initialize allauth configuration by adding a new register to the sites.Site model, using the next command.

.. code:: shell

   python manage.py loaddata conf-allauth-site