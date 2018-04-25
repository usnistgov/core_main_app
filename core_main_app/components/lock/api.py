"""
    Lock API
"""
import datetime

from core_main_app.commons.exceptions import LockError
from core_main_app.components.lock.models import Lock
from core_main_app.settings import LOCK_OBJECT_TTL


def is_object_locked(object, user):
    """ Check if the object is locked.

    Args:
        object:
    Returns:
    """
    try:
        lock = Lock.acquire()
        _check_object_locked(object, user, lock)
        return False
    except LockError, ler:
        return True
    finally:
        Lock.release()


def set_lock_object(object, user):
    """ Set lock on object.

    Args:
        object:
        user:
    Returns:
    """
    try:
        lock = Lock.acquire()
        if not _check_object_locked(object, user, lock):
            lock.set_lock(object, user)
    except LockError, ler:
        raise ler
    finally:
        Lock.release()


def remove_lock_on_object(object, user):
    """ Remove lock on object.

    Args:
        object:
        user:
    Returns:
    """
    try:
        lock = Lock.acquire()
        database_lock_object = lock.get_object_locked(object)
        # Only the user who created the lock can remove it
        if database_lock_object.user_id == str(user.id):
            lock.remove_lock(database_lock_object)
    except:
        pass
    finally:
        Lock.release()


def _check_object_locked(object, user, lock):
    """ Check all conditions of a lock object to define if it is locked or not.
        If there is no lock on object, return false.
        If there is a lock but owned by the user, return true.
        If there is a lock no owned by the user, raise LockError exception.

    Args:
        object:
        user:
        lock:

    Returns:
    """
    try:
        database_lock_object = lock.get_object_locked(object)
    except:
        return False

    # Check if lock has expired
    date = database_lock_object.lock_date
    if (datetime.datetime.now() - date).total_seconds() > LOCK_OBJECT_TTL:
        lock.remove_lock(database_lock_object)
        return False

    # If the user who requested the object is the same as the one who locked the object
    # then it is not locked for him
    if database_lock_object.user_id == str(user.id):
        return True

    raise LockError('The object is used by another user and is locked.')
