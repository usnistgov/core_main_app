"""
 Lock model
"""
import datetime
import threading

from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from core_main_app.commons import exceptions
from core_main_app.components.data.models import Data

sem = threading.Semaphore()


class Lock:
    """
    Class Lock. Singleton thread safe.
    Only this object should be called to be used for an action regarding locking a Document.
    """

    __singleton_lock = threading.Lock()
    __singleton_instance = None

    @classmethod
    def acquire(cls):
        """acquire.

        Args:
            cls:

        Returns:
        """
        if not cls.__singleton_instance:
            with cls.__singleton_lock:
                if not cls.__singleton_instance:
                    cls.__singleton_instance = cls()
        sem.acquire()
        return cls.__singleton_instance

    @classmethod
    def release(cls):
        """release.

        Args:
            cls:

        Returns:
        """
        sem.release()

    def set_lock(self, object, user):
        """Set lock on a Document.

        Args:
            object:
            user:

        Returns:
        """
        database_lock_object = DatabaseLockObject()
        database_lock_object.object = object
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
        except ObjectDoesNotExist as exception:
            raise exceptions.DoesNotExist(str(exception))
        except Exception as ex:
            raise exceptions.ModelError(str(ex))


class DatabaseLockObject(models.Model):
    """
    Class DatabaseLockObject.
    """

    object = models.ForeignKey(Data, blank=False, on_delete=models.CASCADE)
    user_id = models.CharField(blank=False, max_length=200)
    lock_date = models.DateTimeField(blank=False)

    @staticmethod
    def get_lock_by_object(obj):
        """Get lock relative to the given object.

        Args:
            obj:

        Returns:

        """
        return DatabaseLockObject.objects.get(object=obj)

    def __str__(self):
        """Database Lock as string

        Returns:

        """
        return str(self.object)
