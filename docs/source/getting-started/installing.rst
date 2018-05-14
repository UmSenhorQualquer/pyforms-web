******************************
Install & configure
******************************

On this page is explained how to configure your environment and your django app to start using pyforms.

.. note:: The instructions on this page assumes you know how the `Django framework <https://www.djangoproject.com/>`_ works.

Configure the environment
=================================

* First clone the `Pyforms <https://bitbucket.org/UmSenhorQualquer/pyforms-web/>`_ git project at bitbucket.

.. code:: bash

    git clone https://bitbucket.org/UmSenhorQualquer/pyforms-web.git

* Then open the terminal and install the **requirements.txt** in the pyforms-web directory to configure your environment.

.. code:: bash

    pip install -r pyforms-web/requirements.txt
    pip install pyforms-web/. 


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
        'pyforms_web.web'
        ...
    ]

    MIDDLEWARE = [
        ...
        'pyforms_web.web.middleware.PyFormsMiddleware'
    ]

    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "static", 'semantic-ui'),
        os.path.join(BASE_DIR, "static", 'jquery-ui'),
        os.path.join(BASE_DIR, "static", 'js'),
        os.path.join(BASE_DIR, "static", 'css'),
    ]

    TEMPLATES = [
        {
            ...
            'DIRS': [os.path.join(BASE_DIR, 'templates')],
            ...
        },
    ]



Edit the django project **urls.py** file to include the next urls configurations.


.. code:: python

    from django.conf    import settings
    from django.contrib import admin
    from django.urls    import include, path

    urlpatterns = [
        path('',          include('orquestra.urls')       ),
        path('pyforms/',  include('pyforms_web.web.urls') ),
    ]

    if settings.DEBUG:
        from django.conf.urls.static import static
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

Run the project
=================================

.. code:: bash

    cd <project-name>
    python3 manage.py migrate
    python3 manage.py runserver


Access to `http://localhost:8000 <http://localhost:8000/>`_ 

.. image:: /_static/imgs/demo-app.png
    :width: 100%
    :align: center