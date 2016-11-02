"""
Version Manager unit tests
"""
from unittest.case import TestCase
from bson.objectid import ObjectId
from mock.mock import Mock, patch
from core_main_app.commons.exceptions import MDCSError
from core_main_app.components.version_manager.api import vm_get, vm_get_from_version, vm_disable, vm_restore, \
    vm_disable_version, vm_restore_version, vm_get_current
from core_main_app.components.version_manager.models import VersionManager


class TestVersionManagerGet(TestCase):

    @patch('core_main_app.components.version_manager.models.VersionManager.get_by_id')
    def test_vm_get_return_vm(self, mock_get_by_id):
        # Arrange
        mock_vm = Mock(spec=VersionManager)
        mock_vm.title = "Schema"
        mock_vm.id = ObjectId()

        mock_get_by_id.return_value = mock_vm

        # Act
        result = vm_get(mock_vm.id)

        # Assert
        self.assertIsInstance(result, VersionManager)
        self.assertEquals(result.title, mock_vm.title)

    @patch('core_main_app.components.version_manager.models.VersionManager.get_by_id')
    def test_vm_get_throws_exception_if_object_does_not_exists(self, mock_get_by_id):
        # Arrange
        mock_absent_id = ObjectId()
        mock_get_by_id.side_effect = Exception()

        # Act + Assert
        with self.assertRaises(MDCSError):
            vm_get(mock_absent_id)


class TestVersionManagerGetFromVersionId(TestCase):

    @patch('core_main_app.components.version_manager.models.VersionManager.get_all_version_managers')
    def test_vm_get_from_version_id_return_vm(self, mock_get_all_version_managers):
        # Arrange
        id_version1 = ObjectId()
        mock_vm1 = Mock(spec=VersionManager)
        mock_vm1.title = "Schema1"
        mock_vm1.versions = [str(id_version1)]
        mock_vm1.id = ObjectId()

        id_version2 = ObjectId()
        mock_vm2 = Mock(spec=VersionManager)
        mock_vm2.title = "Schema2"
        mock_vm2.versions = [str(id_version2)]
        mock_vm2.id = ObjectId()

        mock_get_all_version_managers.return_value = [mock_vm1, mock_vm2]

        # Act
        result = vm_get_from_version(id_version1)

        # Assert
        self.assertIsInstance(result, VersionManager)
        self.assertEquals(result.title, mock_vm1.title)

    @patch('core_main_app.components.version_manager.models.VersionManager.get_all_version_managers')
    def test_vm_get_from_version_id_throws_exception_if_id_absent(self, mock_get_all_version_managers):
        # Arrange
        id_version1 = ObjectId()
        mock_vm1 = Mock(spec=VersionManager)
        mock_vm1.title = "Schema1"
        mock_vm1.versions = [str(id_version1)]
        mock_vm1.id = ObjectId()

        id_version2 = ObjectId()
        mock_vm2 = Mock(spec=VersionManager)
        mock_vm2.title = "Schema2"
        mock_vm2.versions = [str(id_version2)]
        mock_vm2.id = ObjectId()

        mock_get_all_version_managers.return_value = [mock_vm1, mock_vm2]

        mock_absent_id = ObjectId()

        # Act + Assert
        with self.assertRaises(MDCSError):
            vm_get_from_version(mock_absent_id)


class TestVersionManagerDisable(TestCase):
    @patch('core_main_app.components.version_manager.models.VersionManager.get_by_id')
    def test_vm_get_throws_exception_if_object_does_not_exists(self, mock_get_by_id):
        # Arrange
        mock_absent_id = ObjectId()
        mock_get_by_id.side_effect = Exception()

        # Act + Assert
        with self.assertRaises(MDCSError):
            vm_disable(mock_absent_id)


class TestVersionManagerRestore(TestCase):
    @patch('core_main_app.components.version_manager.models.VersionManager.get_by_id')
    def test_vm_get_throws_exception_if_object_does_not_exists(self, mock_get_by_id):
        # Arrange
        mock_absent_id = ObjectId()
        mock_get_by_id.side_effect = Exception()

        # Act + Assert
        with self.assertRaises(MDCSError):
            vm_restore(mock_absent_id)


class TestVersionManagerRestoreVersion(TestCase):
    @patch('core_main_app.components.version_manager.models.VersionManager.get_all_version_managers')
    def test_vm_get_throws_exception_if_object_does_not_exists(self, mock_get_all_version_managers):
        # Arrange
        mock_absent_id = ObjectId()

        version_id = ObjectId()
        mock_vm = Mock(spec=VersionManager)
        mock_vm.current = str(version_id)
        mock_vm.versions = [str(version_id)]
        mock_vm.id = ObjectId()

        mock_get_all_version_managers.return_value = [mock_vm]

        # Act + Assert
        with self.assertRaises(MDCSError):
            vm_restore_version(mock_absent_id)


class TestVersionManagerDisableVersion(TestCase):

    @patch('core_main_app.components.version_manager.models.VersionManager.get_all_version_managers')
    def test_vm_disable_version_throws_exception_if_object_does_not_exist(self, mock_get_all_version_managers):
        # Arrange
        mock_absent_id = ObjectId()

        version_id = ObjectId()
        mock_vm = Mock(spec=VersionManager)
        mock_vm.current = str(version_id)
        mock_vm.versions = [str(version_id)]
        mock_vm.id = ObjectId()

        mock_get_all_version_managers.return_value = [mock_vm]

        # Act + Assert
        with self.assertRaises(MDCSError):
            vm_disable_version(mock_absent_id)

    @patch('core_main_app.components.version_manager.models.VersionManager.get_all_version_managers')
    def test_vm_disable_current_version_throws_exception(self, mock_get_all_version_managers):
        # Arrange
        version_id = ObjectId()
        mock_vm = Mock(spec=VersionManager)
        mock_vm.current = str(version_id)
        mock_vm.versions = [str(version_id)]
        mock_vm.id = ObjectId()

        mock_get_all_version_managers.return_value = [mock_vm]

        # Act + Assert
        with self.assertRaises(MDCSError):
            vm_disable_version(version_id)

    @patch('core_main_app.components.version_manager.models.VersionManager.get_all_version_managers')
    def test_vm_disable_version_throws_exception_if_new_current_does_not_exist(self, mock_get_all_version_managers):
        # Arrange
        version_id = ObjectId()
        mock_vm = Mock(spec=VersionManager)
        mock_vm.current = str(version_id)
        mock_vm.versions = [str(version_id)]
        mock_vm.id = ObjectId()

        mock_get_all_version_managers.return_value = [mock_vm]

        # Act + Assert
        with self.assertRaises(MDCSError):
            vm_disable_version(mock_vm.current, version_id)


class TestVersionManagerGetCurrent(TestCase):
    @patch('core_main_app.components.version_manager.models.VersionManager.get_by_id')
    def test_vm_get_return_vm(self, mock_get_by_id):
        # Arrange
        current_version_id = str(ObjectId())
        mock_vm = Mock(spec=VersionManager)
        mock_vm.current = current_version_id
        mock_vm.id = ObjectId()

        mock_get_by_id.return_value = mock_vm

        # Act
        result = vm_get_current(mock_vm.id)

        # Assert
        self.assertEquals(result, current_version_id)

    @patch('core_main_app.components.version_manager.models.VersionManager.get_by_id')
    def test_vm_get_throws_exception_if_object_does_not_exists(self, mock_get_by_id):
        # Arrange
        mock_absent_id = ObjectId()
        mock_get_by_id.side_effect = Exception()

        # Act + Assert
        with self.assertRaises(MDCSError):
            vm_get_current(mock_absent_id)
