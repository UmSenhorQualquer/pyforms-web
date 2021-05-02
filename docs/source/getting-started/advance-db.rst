******************************************
From SQL to Django models' apps
******************************************

This example demonstrates how to start from a raw database and end up with the forms to manage it in few steps.

.. note::

    This examples is based on the code available at the folder tutorials/tutorial_advance_db



First of all start your django project:

.. code:: console

    > django-admin startproject tutorial_advance_db

Configure your django app settings.py file to point your database and include the pyforms configurations.

.. code:: python

    ...

    INSTALLED_APPS = [
        'tutorial',

        'orquestra',
        'pyforms_web.web',
        'jfu',

        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
    ]

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'pyforms_web.web.middleware.PyFormsMiddleware'
    ]
    ...

Enter in the project folder and create the tutorial app:

.. code:: console

    > cd tutorial_advance_db
    > mkdir tutorial


Generate the Django models from your SQL database.

.. code:: console

    > python manage.py inspectdb > tutorial/models.py

Generate the Pyforms apps to manage the models by executing the next command:

.. code:: console

    > python manage.py export_pyforms_apps tutorial

Run migrations and execute the django project:

.. code:: console

    > python manage.py migrate
    > python manage.py runserver