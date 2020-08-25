"""
 Lock model
"""
import datetime
import threading

from bson.dbref import DBRef
from django_mongoengine import Document, fields
from mongoengine import errors as mongoengine_errors

from core_main_app.commons import exceptions

sem = threading.Semaphore()


class Lock(object):
    """
    Class Lock. Singleton thread safe.
    Only this object should be called to be used for an action regarding locking a Document.
    """

    __singleton_lock = threading.Lock()
    __singleton_instance = None

    @classmethod
    def acquire(cls):
        if not cls.__singleton_instance:
            with cls.__singleton_lock:
                if not cls.__singleton_instance:
                    cls.__singleton_instance = cls()
        sem.acquire()
        return cls.__singleton_instance

    @classmethod
    def release(cls):
        sem.release()

    def set_lock(self, object, user):
        """Set lock on a Document.

        Args:
            object:
            user:

        Returns:
        """
        database_lock_object = DatabaseLockObject()
        database_lock_object.object = DBRef(object._class_name, object.id)
        database_lock_object.user_id = str(user.id)
        database_lock_object.lock_date = datetime.datetime.now()
        database_lock_object.save()

    def remove_lock(self, database_lock_object):
        """Remove a lock.

        Args:
            database_lock_object:

        Returns:
        """
        database_lock_object.delete()

    def get_object_locked(self, object):
        """Get the locked object.

        Args:
            object:
        Returns:
        """
        try:
            return DatabaseLockObject.get_lock_by_object(object)
        except mongoengine_errors.DoesNotExist as e:
            raise exceptions.DoesNotExist(str(e))
        except Exception as ex:
            raise exceptions.ModelError(str(ex))


class DatabaseLockObject(Document):
    """
    Class DatabaseLockObject.
    """

    object = fields.ReferenceField(Document, blank=False)
    user_id = fields.StringField(blank=False)
    lock_date = fields.DateTimeField(blank=False)

    @staticmethod
    def get_lock_by_object(object):
        """Get lock relative to the given object.

        Args:
            object:

        Returns:

        """
        return DatabaseLockObject.objects.get(object=object)
