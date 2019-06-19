"""
Version Manager unit tests
"""
from unittest.case import TestCase

from bson.objectid import ObjectId
from mock.mock import Mock, patch
from mongoengine import errors as mongoengine_errors

from core_main_app.commons import exceptions
from core_main_app.components.version_manager import api as version_manager_api
from core_main_app.components.version_manager.models import VersionManager


class TestVersionManagerGet(TestCase):

    @patch('core_main_app.components.version_manager.models.VersionManager.get_by_id')
    def test_version_manager_get_returns_version_manager(self, mock_get_by_id):
        # Arrange
        mock_version_manager = _create_mock_version_manager(title="Schema")

        mock_get_by_id.return_value = mock_version_manager

        # Act
        result = version_manager_api.get(mock_version_manager.id)

        # Assert
        self.assertIsInstance(result, VersionManager)

    @patch('core_main_app.components.version_manager.models.VersionManager.get_by_id')
    def test_version_manager_get_raises_exception_if_object_does_not_exist(self, mock_get_by_id):
        # Arrange
        mock_absent_id = ObjectId()
        mock_get_by_id.side_effect = mongoengine_errors.DoesNotExist

        # Act + Assert
        with self.assertRaises(mongoengine_errors.DoesNotExist):
            version_manager_api.get(mock_absent_id)


class TestVersionManagerGetFromVersionId(TestCase):

    @patch('core_main_app.components.version_manager.models.VersionManager.get_all')
    def test_version_manager_get_from_version_id_returns_version_manager(self, mock_get_all):
        # Arrange
        mock_version_manager_1 = _create_mock_version_manager(title="Schema1")
        version = _create_mock_object()
        mock_version_manager_1.versions.append(str(version.id))

        mock_version_manager_2 = _create_mock_version_manager(title="Schema2")

        mock_get_all.return_value = [mock_version_manager_1, mock_version_manager_2]

        # Act
        result = version_manager_api.get_from_version(version)

        # Assert
        self.assertIsInstance(result, VersionManager)

    @patch('core_main_app.components.version_manager.models.VersionManager.get_all')
    def test_version_manager_get_from_version_id_throws_exception_if_id_absent(self, mock_get_all):
        # Arrange
        mock_version_manager_1 = _create_mock_version_manager(title="Schema1")
        mock_version_manager_2 = _create_mock_version_manager(title="Schema2")

        mock_get_all.return_value = [mock_version_manager_1, mock_version_manager_2]

        mock_absent = _create_mock_object()

        # Act + Assert
        with self.assertRaises(exceptions.ApiError):
            version_manager_api.get_from_version(mock_absent)


class TestVersionManagerRestoreVersion(TestCase):
    @patch('core_main_app.components.version_manager.models.VersionManager.get_all')
    def test_version_manager_get_raises_exception_if_object_does_not_exist(self, mock_get_all):
        # Arrange
        mock_absent = _create_mock_object()
        mock_version_manager = _create_mock_version_manager()

        mock_get_all.return_value = [mock_version_manager]

        # Act + Assert
        with self.assertRaises(exceptions.ApiError):
            version_manager_api.restore_version(mock_absent)


class TestVersionManagerDisableVersion(TestCase):

    @patch('core_main_app.components.version_manager.models.VersionManager.get_all')
    def test_version_manager_disable_version_raises_exception_if_object_does_not_exist(self, mock_get_all):
        # Arrange
        mock_absent = _create_mock_object()
        mock_version_manager = _create_mock_version_manager()

        mock_get_all.return_value = [mock_version_manager]

        # Act + Assert
        with self.assertRaises(exceptions.ApiError):
            version_manager_api.disable_version(mock_absent)

    @patch('core_main_app.components.version_manager.models.VersionManager.get_all')
    def test_version_manager_disable_current_version_throws_exception(self, mock_get_all):
        # Arrange
        mock_version_manager = _create_mock_version_manager()
        mock_current = _create_mock_object()
        mock_version_manager.versions.append(str(mock_current.id))
        mock_version_manager.current = str(mock_current.id)

        mock_get_all.return_value = [mock_version_manager]

        # Act + Assert
        with self.assertRaises(exceptions.ApiError):
            version_manager_api.disable_version(mock_current)

    @patch('core_main_app.components.version_manager.models.VersionManager.get_all')
    def test_version_manager_disable_version_raises_exception_if_new_current_does_not_exist(self, mock_get_all):
        # Arrange
        mock_version_manager = _create_mock_version_manager()
        mock_absent = _create_mock_object()
        mock_current = _create_mock_object()
        mock_version_manager.versions.append(str(mock_current.id))
        mock_version_manager.current = str(mock_current.id)

        mock_get_all.return_value = [mock_version_manager]

        # Act + Assert
        with self.assertRaises(exceptions.ApiError):
            version_manager_api.disable_version(mock_current, mock_absent)


class TestVersionManagerGetCurrent(TestCase):
    def test_version_manager_get_current_return_current_version_id(self):
        # Arrange
        mock_version_manager = _create_mock_version_manager()

        # Act
        result = version_manager_api.get_current(mock_version_manager)

        # Assert
        self.assertEquals(result, mock_version_manager.current)


class TestVersionManagerSetCurrent(TestCase):
    @patch('core_main_app.components.version_manager.models.VersionManager.get_all')
    @patch('core_main_app.components.version_manager.models.VersionManager.get_disabled_versions')
    def test_version_manager_set_current_raises_api_error_if_disabled(self, mock_get_disabled_versions, mock_get_all):
        # Arrange
        to_disable = _create_mock_object()
        mock_vm = _create_mock_version_manager()

        mock_get_all.return_value = [mock_vm]
        mock_get_disabled_versions.return_value = [str(to_disable.id)]

        # Act + Assert
        with self.assertRaises(exceptions.ApiError):
            version_manager_api.set_current(to_disable)


class TestVersionManagerInsert(TestCase):
    @patch('core_main_app.components.version_manager.models.VersionManager.save')
    def test_version_manager_insert_first_version_adds_versions(self, mock_save):
        # Arrange
        version_manager = _create_version_manager()
        version = _create_mock_object()
        mock_save.return_value = None

        # Act + Assert
        version_manager_api.insert_version(version_manager, version)

        self.assertEquals(version_manager.versions[0], str(version.id))

    @patch('core_main_app.components.version_manager.models.VersionManager.save')
    def test_version_manager_insert_first_version_sets_current(self, mock_save):
        # Arrange
        version_manager = _create_version_manager()
        version = _create_mock_object()
        mock_save.return_value = None

        # Act + Assert
        version_manager_api.insert_version(version_manager, version)

        self.assertEquals(version_manager.current, str(version.id))


class TestVersionManagerGetActiveGlobalVersionManagerByTitle(TestCase):

    @patch.object(VersionManager, 'get_active_global_version_manager_by_title')
    def test_version_manager_get_returns_version_manager(self, mock_get_active_global):
        # Arrange
        title = "Schema"
        mock_version_manager = _create_mock_version_manager(title=title)

        mock_get_active_global.return_value = mock_version_manager

        # Act
        result = version_manager_api.get_active_global_version_manager_by_title(title)

        # Assert
        self.assertIsInstance(result, VersionManager)

    @patch.object(VersionManager, 'get_active_global_version_manager_by_title')
    def test_version_manager_get_raises_exception_if_object_does_not_exist(self, mock_get_active_global):
        # Arrange
        mock_absent_title = "Schema"
        mock_get_active_global.side_effect = mongoengine_errors.DoesNotExist

        # Act + Assert
        with self.assertRaises(mongoengine_errors.DoesNotExist):
            version_manager_api.get_active_global_version_manager_by_title(mock_absent_title)


class TestVersionManagerGetVersionByNumber(TestCase):

    def test_version_manager_get_returns_version(self):
        # Arrange
        version = str(ObjectId())
        version_manager = _create_version_manager("Schema1", [version])

        # Act
        result = version_manager_api.get_version_by_number(version_manager, 1)

        # Assert
        self.assertEquals(result, version)

    def test_version_manager_get_raises_exception_if_object_does_not_exist(self):
        # Arrange
        version = str(ObjectId())
        version_manager = _create_version_manager("Schema1", [version])

        # Act + Assert
        with self.assertRaises(exceptions.DoesNotExist):
            version_manager_api.get_version_by_number(version_manager, 2)


class TestVersionManagerGetVersionNumber(TestCase):

    def test_version_manager_get_returns_number(self):
        # Arrange
        version = str(ObjectId())
        version_manager = _create_version_manager("Schema1", [version])

        # Act
        result = version_manager_api.get_version_number(version_manager, version)

        # Assert
        self.assertEquals(result, 1)

    def test_version_manager_get_raises_exception_if_object_does_not_exist(self):
        # Arrange
        version = str(ObjectId())
        absent_version = str(ObjectId())
        version_manager = _create_version_manager("Schema1", [version])

        # Act + Assert
        with self.assertRaises(exceptions.DoesNotExist):
            version_manager_api.get_version_number(version_manager, absent_version)


def _create_mock_version_manager(title=""):
    """
    Create a mock version manager
    :param title:
    :return:
    """
    mock_vm = Mock(spec=VersionManager)
    mock_vm.title = title
    mock_vm.current = ObjectId()
    mock_vm.versions = [str(mock_vm.current)]
    mock_vm.id = ObjectId()
    return mock_vm


def _create_mock_object():
    """
    Create a mock object
    :return:
    """
    mock_object = Mock()
    mock_object.id = ObjectId()
    return mock_object


def _create_version_manager(title="", versions=[]):
    """
    Returns a templates version manager
    :param title:
    :return:
    """
    return VersionManager(
        id=ObjectId(),
        title=title,
        versions=versions,
        disabled_versions=[]
    )
