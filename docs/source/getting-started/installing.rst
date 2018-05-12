******************************
Install & configure
******************************

On this page is explained how to configure your environment and your django app to start using pyforms.

.. note:: The instructions on this page assumes you know how the `Django framework <https://www.djangoproject.com/>`_ works.

Configure the environment
=================================

* First clone the git project at `bitbucket <https://bitbucket.org/UmSenhorQualquer/pyforms-web.git>`_.
* Then open the terminal and install the **requirements.txt** in the pyforms-web directory to configure your environment.

.. code:: bash

    pip install -r requirements.txt
        


Configure a django project
=================================

Execute the next command in the terminal to start a Django project.

.. code:: bash

    django-admin startproject <project-name>

Edit the django project **settings.py** file to include the next configurations.

.. code:: python

    INSTALLED_APPS = [
        'jfu',
        'sorl.thumbnail',
        'orquestra',
        'pyforms_web.web',
        'allauth',
        'allauth.account',
        'allauth.socialaccount',
        'allauth.socialaccount.providers.google',
        'django.contrib.sites',
        ...
    ]

    MIDDLEWARE = [
        ...
        'pyforms_web.web.middleware.PyFormsMiddleware'
    ]

    AUTHENTICATION_BACKENDS = [
        ...,
        'allauth.account.auth_backends.AuthenticationBackend',
    ]

    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "static", 'semantic-ui'),
        os.path.join(BASE_DIR, "static", 'jquery-ui'),
        os.path.join(BASE_DIR, "static", 'js'),
        os.path.join(BASE_DIR, "static", 'css'),
    ]

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql', # You can use any other database type
            'NAME': <database>,
            'USER': <user>,
            'PASSWORD': <password>,
            'HOST': 'localhost',
            'PORT': '3306',
        }
    }

    TEMPLATES = [
        {
            ...
            'DIRS': [os.path.join(BASE_DIR, 'templates')],
            ...
        },
    ]

    SITE_ID = 1



Edit the django project **urls.py** file to include the next urls configurations.


.. code:: python

    from django.conf.urls import url, include
    from django.conf import settings

    urlpatterns = [
        url(r'', include('orquestra.urls')),
        url(r'^accounts/', include('allauth.urls')),
        url(r'^pyforms/', include('pyforms_web.web.urls') ),
    ]

    if settings.DEBUG:
        from django.conf.urls.static import static
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)