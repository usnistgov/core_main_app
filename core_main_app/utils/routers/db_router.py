""" DB Router for Primary/Replica
"""


class PrimaryReplicaRouter:
    def db_for_read(self, model, **hints):
        """
        Reads go to replica.
        """
        return "replica1"

    def db_for_write(self, model, **hints):
        """
        Writes always go to primary.
        """
        return "default"

    def allow_relation(self, obj1, obj2, **hints):
        """
        Relations between objects are allowed if both objects are
        in the primary/replica pool.
        """
        db_set = {"default", "replica1"}
        if obj1._state.db in db_set and obj2._state.db in db_set:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        All models.
        """
        return True
