## Install Apache2

## Install mod_python for python3

## Activate mod_python:

.. code-block::

    sudo a2enmod mod_python

## Go to /var/www/ and clone our project to the folder.

.. code-block::

    cd /var/www
    git clone [app git repositiory]

## Collect static

.. code-block::

    cd [app directory]
    python manage.py collectstatic

## Change files rights access.

.. code-block::

    cd [app directory]
    sudo chown www-data -R *

## Configure Apache for Debian

Create file in /etc/apache2/sites-available/[name of the app].conf with the next configuration:

.. code-block::

    NameVirtualHost 0.0.0.0:80

    <VirtualHost *:80>
        ServerName  [Name of the server]
        ServerAlias [Name of the server] [Machine IP address]
        ServerAdmin [Email of the administrator]

        ErrorLog  /var/log/[name of the app]_error.log
        CustomLog /var/log/[name of the app]_access.log combined

        #WSGIPythonExecutable /usr/bin/python3.5
        WSGIDaemonProcess [name of the app] python-path=/usr/local/lib/python3.5/dist-packages:/var/www/[name of the app] display-name=%{GROUP}
        WSGIProcessGroup [name of the app]
        WSGIScriptAlias / /var/www/[name of the app]/config/wsgi.py


        Alias /static/ /var/www/[name of the app]/static/

        <Directory /var/www/[name of the app]>
            <Files wsgi.py>
            Require all granted
            </Files>
        </Directory>

        <Directory /var/www/[name of the app]/static>
            Require all granted
        </Directory>

        <Directory /var/www/[name of the app]/config>
            Options Indexes FollowSymLinks
            AllowOverride None
            Order allow,deny
            Allow from all
        </Directory>

        # Optional for SSL encryption.
        SSLEngine on
        SSLCertificateFile    /etc/ssl/certs/apache-selfsigned.crt
        SSLCertificateKeyFile /etc/ssl/private/apache-selfsigned.key

    </VirtualHost>


## Activate apache2 configuration

.. code-block::

    sudo a2ensite [name of the app].conf
    sudo service apache2 restart