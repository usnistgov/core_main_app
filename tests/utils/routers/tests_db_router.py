""" Unit Test Primary/Replica Router
"""
from unittest.case import TestCase
from unittest.mock import MagicMock

from core_main_app.utils.routers.db_router import PrimaryReplicaRouter


class TestPrimaryReplicaRouter(TestCase):
    """TestPrimaryReplicaRouter"""

    def setUp(self):
        self.router = PrimaryReplicaRouter()

    def test_db_for_read_return_replica1(self):
        """test_db_for_read_return_replica1"""
        self.assertEqual(
            self.router.db_for_read(model=MagicMock()), "replica1"
        )

    def test_db_for_write_return_default(self):
        """test_db_for_write_return_default"""
        self.assertEqual(
            self.router.db_for_write(model=MagicMock()), "default"
        )

    def test_allow_relation_return_true_if_objs_in_db_set(self):
        """test_allow_relation_return_true_if_objs_in_db_set"""
        obj1 = MagicMock()
        obj1._state.db = "default"
        obj2 = MagicMock()
        obj2._state.db = "replica1"
        self.assertTrue(self.router.allow_relation(obj1, obj2))

    def test_allow_relation_return_false_if_objs_not_in_db_set(self):
        """test_allow_relation_return_false_if_objs_not_in_db_set"""
        obj1 = MagicMock()
        obj1._state.db = "default"
        obj2 = MagicMock()
        obj2._state.db = "replica2"
        self.assertFalse(self.router.allow_relation(obj1, obj2))

    def test_allow_migrate_return_true(self):
        """test_allow_migrate_return_true"""
        self.assertTrue(
            self.router.allow_migrate(
                db="db", app_label="label", model_name="model"
            )
        )
