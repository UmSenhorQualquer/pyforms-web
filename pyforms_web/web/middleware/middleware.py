import dill
import filelock
import os
import threading

from confapp import conf

from .apps_2_update import Apps2Update


class PyFormsMiddleware(object):
    _request = {}
    _users = {}

    USER = None

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        request.updated_apps = Apps2Update()
        self.__class__._request[threading.current_thread()] = request

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        self.__class__._request.pop(threading.current_thread(), None)
        return response

    @classmethod
    def get_request(cls, default=None):
        """Retrieve request"""
        return cls._request.get(threading.current_thread(), default)

    ##################################################################################################
    ##################################################################################################
    ##################################################################################################
    @classmethod
    def user(cls):
        return cls.get_request().user

    @classmethod
    def add(cls, app):
        cls.get_request().updated_apps.add_top(app)

    @classmethod
    def get_instance(cls, app_id):
        user = cls.user()

        if conf.PYFORMS_APPS_IN_MEMORY:
            cls._users.setdefault(user.pk, {})
            return cls._users[user.pk].get(app_id, None)
        else:
            app_path = os.path.join(
                conf.PYFORMS_WEB_APPS_CACHE_DIR,
                '{0}-{1}'.format(user.pk, user.username),
                "{0}.app".format(app_id)
            )

            if os.path.isfile(app_path):
                lock = filelock.FileLock(conf.PYFORMS_WEB_LOCKFILE)
                with lock.acquire(timeout=10):
                    with open(app_path, 'rb') as f:
                        return dill.load(f)
            else:
                return None

    @classmethod
    def commit_instance(cls, app):
        user = cls.user()

        if conf.PYFORMS_APPS_IN_MEMORY:
            cls._users.setdefault(user.pk, {})
            cls._users[user.pk][app.uid] = app
        else:
            # save the modifications
            userpath = os.path.join(
                conf.PYFORMS_WEB_APPS_CACHE_DIR,
                '{0}-{1}'.format(user.pk, user.username)
            )
            if not os.path.exists(userpath): os.makedirs(userpath)

            app_path = os.path.join(userpath, "{0}.app".format(app.uid))

            lock = filelock.FileLock(conf.PYFORMS_WEB_LOCKFILE)
            with lock.acquire(timeout=4):
                with open(app_path, 'wb') as f:
                    dill.dump(app, f, protocol=4)

    @classmethod
    def remove_instance(cls, app_id):
        user = cls.user()

        if conf.PYFORMS_APPS_IN_MEMORY:
            cls._users.setdefault(user.pk, {})
            if app_id in cls._users[user.pk]:
                del cls._users[user.pk][app_id]
                return True
            else:
                return False
        else:

            app_path = os.path.join(
                conf.PYFORMS_WEB_APPS_CACHE_DIR,
                '{0}-{1}'.format(user.pk, user.username),
                "{0}.app".format(app_id)
            )
            if os.path.isfile(app_path):
                lock = filelock.FileLock(conf.PYFORMS_WEB_LOCKFILE)
                with lock.acquire(timeout=10):
                    os.remove(app_path)
                return True
            else:
                return False
