"""
    Xml operation test class
"""

import core_main_app.commons.exceptions as exceptions
from unittest import TestCase
from core_main_app.utils.xml import raw_xml_to_dict, get_namespaces, get_default_prefix, build_tree, \
    get_element_by_xpath, set_attribute, delete_attribute, add_appinfo_element, delete_appinfo_element
from collections import OrderedDict
from lxml import etree


class TestRawToDict(TestCase):
    def test_raw_to_dict_valid(self):
        # Arrange
        raw_xml = '<root><test>Hello</test></root>'
        expected_dict = OrderedDict([(u'root', OrderedDict([(u'test', u'Hello')]))])

        # Act
        xml_dict = raw_xml_to_dict(raw_xml)

        # Assert
        self.assertEquals(expected_dict, xml_dict)

    def test_raw_to_dict_throws_exception_when_invalid_xml(self):
        # Arrange
        raw_xml = '<root><test>Hello</test?</root>'

        # Act # Assert
        with self.assertRaises(exceptions.XMLError):
            raw_xml_to_dict(raw_xml)


class TestGetNamespaces(TestCase):
    def test_get_namespaces_one_namespace_prefix_is_key(self):
        xsd_string = "<xs:schema xmlns:xs='http://www.w3.org/2001/XMLSchema'></xs:schema>"
        namespaces = get_namespaces(xsd_string)
        self.assertTrue('xs' in namespaces.keys())

    def test_get_namespaces_one_namespace_namespace_is_value(self):
        xsd_string = "<xs:schema xmlns:xs='http://www.w3.org/2001/XMLSchema'></xs:schema>"
        namespaces = get_namespaces(xsd_string)
        self.assertTrue(namespaces['xs'] == 'http://www.w3.org/2001/XMLSchema')

    def test_get_namespaces_two_namespaces(self):
        xsd_string = "<xs:schema xmlns:xs='http://www.w3.org/2001/XMLSchema' xmlns:test='test'></xs:schema>"
        namespaces = get_namespaces(xsd_string)
        self.assertTrue('xs' in namespaces.keys() and 'test' in namespaces.keys())

    def test_get_namespaces_invalid_file(self):
        xsd_string = "invalid"
        with self.assertRaises(etree.XMLSyntaxError):
            get_namespaces(xsd_string)

    def test_get_namespaces_xml_namespace(self):
        xsd_string = "<xs:schema xmlns:xs='http://www.w3.org/2001/XMLSchema'></xs:schema>"
        namespaces = get_namespaces(xsd_string)
        self.assertTrue('xml' in namespaces.keys())


class TestGetDefautPrefix(TestCase):
    def test_get_xs_prefix(self):
        xsd_string = "<xs:schema xmlns:xs='http://www.w3.org/2001/XMLSchema'></xs:schema>"
        namespaces = get_namespaces(xsd_string)
        prefix = get_default_prefix(namespaces)
        self.assertTrue(prefix == 'xs')

    def test_get_xsd_prefix(self):
        xsd_string = "<xsd:schema xmlns:xsd='http://www.w3.org/2001/XMLSchema'></xsd:schema>"
        namespaces = get_namespaces(xsd_string)
        prefix = get_default_prefix(namespaces)
        self.assertTrue(prefix == 'xsd')

    def test_get_no_prefix(self):
        xsd_string = "<schema></schema>"
        namespaces = get_namespaces(xsd_string)
        prefix = get_default_prefix(namespaces)
        self.assertTrue(prefix == '')


class TestGetElementByXpath(TestCase):
    def test_get_element_xpath_matching_element(self):
        xsd_string = "<xs:schema xmlns:xs='http://www.w3.org/2001/XMLSchema'><root><test></test></root></xs:schema>"
        xpath = "root/test"
        xsd_tree = build_tree(xsd_string)
        element = get_element_by_xpath(xsd_tree, xpath)
        self.assertTrue(element is not None)

    def test_get_element_xpath_matching_element_with_xs_namespace_prefix(self):
        xsd_string = "<xs:schema xmlns:xs='http://www.w3.org/2001/XMLSchema'><xs:element><xs:complexType>" \
                     "</xs:complexType></xs:element></xs:schema>"
        xpath = "xs:element/xs:complexType"
        xsd_tree = build_tree(xsd_string)
        namespaces = get_namespaces(xsd_string)
        element = get_element_by_xpath(xsd_tree, xpath, namespaces)
        self.assertTrue(element is not None)

    def test_get_element_xpath_matching_element_with_xsd_namespace_prefix(self):
        xsd_string = "<xsd:schema xmlns:xsd='http://www.w3.org/2001/XMLSchema'><xsd:element><xsd:complexType>" \
                     "</xsd:complexType></xsd:element></xsd:schema>"
        xpath = "xsd:element/xsd:complexType"
        xsd_tree = build_tree(xsd_string)
        namespaces = get_namespaces(xsd_string)
        element = get_element_by_xpath(xsd_tree, xpath, namespaces)
        self.assertTrue(element is not None)

    def test_get_element_xpath_not_matching_element_with_different_namespace_prefix(self):
        xsd_string = "<xsd:schema xmlns:xsd='http://www.w3.org/2001/XMLSchema'><xsd:element><xsd:complexType>" \
                     "</xsd:complexType></xsd:element></xsd:schema>"
        xpath = "xs:element/xs:complexType"
        xsd_tree = build_tree(xsd_string)
        namespaces = get_namespaces(xsd_string)
        with self.assertRaises(exceptions.XSDError):
            get_element_by_xpath(xsd_tree, xpath, namespaces)

    def test_get_element_xpath_not_matching_element_without_namespace_prefix(self):
        xsd_string = "<xsd:schema xmlns:xsd='http://www.w3.org/2001/XMLSchema'><xsd:element><xsd:complexType>" \
                     "</xsd:complexType></xsd:element></xsd:schema>"
        xpath = "element/complexType"
        xsd_tree = build_tree(xsd_string)
        namespaces = get_namespaces(xsd_string)
        with self.assertRaises(exceptions.XSDError):
            get_element_by_xpath(xsd_tree, xpath, namespaces)

    def test_get_element_xpath_not_matching_element(self):
        xsd_string = "<xs:schema xmlns:xs='http://www.w3.org/2001/XMLSchema'><root><test></test></root></xs:schema>"
        xpath = "root/name"
        xsd_tree = build_tree(xsd_string)
        with self.assertRaises(exceptions.XSDError):
            get_element_by_xpath(xsd_tree, xpath)

    def test_get_element_invalid_xpath(self):
        xsd_string = "<xs:schema xmlns:xs='http://www.w3.org/2001/XMLSchema'><root><test></test></root></xs:schema>"
        xpath = "invalid"
        xsd_tree = build_tree(xsd_string)
        with self.assertRaises(exceptions.XSDError):
            get_element_by_xpath(xsd_tree, xpath)


class TestSetAttribute(TestCase):
    def test_set_attribute_invalid_xsd_raises_xsd_error(self):
        xsd_string = "invalid"
        with self.assertRaises(etree.XMLSyntaxError):
            set_attribute(xsd_string, "", "", "")

    def test_set_attribute_invalid_xpath_raises_xsd_error(self):
        xsd_string = "<xs:schema xmlns:xs='http://www.w3.org/2001/XMLSchema'><root><test></test></root></xs:schema>"
        xpath = "invalid"
        with self.assertRaises(exceptions.XSDError):
            set_attribute(xsd_string, xpath, "", "")

    def test_set_attribute_adds_attribute(self):
        xsd_string = "<xs:schema xmlns:xs='http://www.w3.org/2001/XMLSchema'><root><test></test></root></xs:schema>"
        xpath = "root/test"
        attribute_name = "attr"
        updated_xsd_string = set_attribute(xsd_string, xpath, attribute_name, "")
        self.assertTrue('<test attr=' in updated_xsd_string)

    def test_set_attribute_adds_attribute_with_value(self):
        xsd_string = "<xs:schema xmlns:xs='http://www.w3.org/2001/XMLSchema'><root><test></test></root></xs:schema>"
        xpath = "root/test"
        attribute_name = "attr"
        attribute_value = "value"
        updated_xsd_string = set_attribute(xsd_string, xpath, attribute_name, attribute_value)
        self.assertTrue('<test attr="value"' in updated_xsd_string)

    def test_set_attribute_if_present(self):
        xsd_string = "<xs:schema xmlns:xs='http://www.w3.org/2001/XMLSchema'>" \
                     "<root><test attr='old'></test></root></xs:schema>"
        xpath = "root/test"
        attribute_name = "attr"
        attribute_value = "new"
        updated_xsd_string = set_attribute(xsd_string, xpath, attribute_name, attribute_value)
        self.assertTrue('<test attr="new"' in updated_xsd_string)


class TestDeleteAttribute(TestCase):
    def test_delete_attribute_invalid_xsd_raises_xsd_error(self):
        xsd_string = "invalid"
        with self.assertRaises(etree.XMLSyntaxError):
            delete_attribute(xsd_string, "", "")

    def test_delete_attribute_invalid_xpath_raises_xsd_error(self):
        xsd_string = "<xs:schema xmlns:xs='http://www.w3.org/2001/XMLSchema'><root><test></test></root></xs:schema>"
        xpath = "invalid"
        with self.assertRaises(exceptions.XSDError):
            delete_attribute(xsd_string, xpath, "")

    def test_delete_attribute_removed_if_exists(self):
        xsd_string = "<xs:schema xmlns:xs='http://www.w3.org/2001/XMLSchema'>" \
                     "<root><test attr='value'></test></root></xs:schema>"
        xpath = "root/test"
        attribute_name = "attr"
        updated_xsd_string = delete_attribute(xsd_string, xpath, attribute_name)
        self.assertTrue('attr=' not in updated_xsd_string)

    def test_delete_attribute_does_not_fail_if_not_present(self):
        xsd_string = "<xs:schema xmlns:xs='http://www.w3.org/2001/XMLSchema'>" \
                     "<root><test></test></root></xs:schema>"
        xpath = "root/test"
        attribute_name = "attr"
        delete_attribute(xsd_string, xpath, attribute_name)


class TestAddAppInfoElement(TestCase):
    def test_add_appinfo_element_invalid_xsd_raises_xsd_error(self):
        xsd_string = "invalid"
        with self.assertRaises(etree.XMLSyntaxError):
            add_appinfo_element(xsd_string, "", "", "")

    def test_add_appinfo_element_invalid_xpath_raises_xsd_error(self):
        xsd_string = "<xs:schema xmlns:xs='http://www.w3.org/2001/XMLSchema'><root><test></test></root></xs:schema>"
        xpath = "invalid"
        with self.assertRaises(exceptions.XSDError):
            add_appinfo_element(xsd_string, xpath, "attribute", "value")

    def test_add_appinfo_element_no_annotation_adds_it(self):
        xsd_string = "<xs:schema xmlns:xs='http://www.w3.org/2001/XMLSchema'><xs:element name='root'/></xs:schema>"
        xpath = "xs:element"

        updated_xsd_string = add_appinfo_element(xsd_string, xpath, "attribute", "value")

        expected_string = '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema"><xs:element name="root">' \
                          '<xs:annotation><xs:appinfo><attribute>value</attribute></xs:appinfo></xs:annotation>' \
                          '</xs:element></xs:schema>'
        self.assertEquals(updated_xsd_string, expected_string)

    def test_add_appinfo_element_no_appinfo_adds_it(self):
        xsd_string = "<xs:schema xmlns:xs='http://www.w3.org/2001/XMLSchema'><xs:element name='root'><xs:annotation>" \
                     "</xs:annotation></xs:element></xs:schema>"
        xpath = "xs:element"

        updated_xsd_string = add_appinfo_element(xsd_string, xpath, "attribute", "value")

        expected_string = '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema"><xs:element name="root">' \
                          '<xs:annotation><xs:appinfo><attribute>value</attribute></xs:appinfo></xs:annotation>' \
                          '</xs:element></xs:schema>'
        self.assertEquals(updated_xsd_string, expected_string)

    def test_add_appinfo_element_no_element_adds_it(self):
        xsd_string = "<xs:schema xmlns:xs='http://www.w3.org/2001/XMLSchema'><xs:element name='root'><xs:annotation>" \
                     "<xs:appinfo></xs:appinfo></xs:annotation></xs:element></xs:schema>"
        xpath = "xs:element"

        updated_xsd_string = add_appinfo_element(xsd_string, xpath, "attribute", "value")

        expected_string = '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema"><xs:element name="root">' \
                          '<xs:annotation><xs:appinfo><attribute>value</attribute></xs:appinfo></xs:annotation>' \
                          '</xs:element></xs:schema>'
        self.assertEquals(updated_xsd_string, expected_string)

    def test_add_appinfo_element_annotation_present_updates_it(self):
        xsd_string = "<xs:schema xmlns:xs='http://www.w3.org/2001/XMLSchema'><xs:element name='root'><xs:annotation>" \
                     "</xs:annotation></xs:element></xs:schema>"
        xpath = "xs:element"

        updated_xsd_string = add_appinfo_element(xsd_string, xpath, "attribute", "value")

        expected_string = '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema"><xs:element name="root">' \
                          '<xs:annotation><xs:appinfo><attribute>value</attribute></xs:appinfo></xs:annotation>' \
                          '</xs:element></xs:schema>'
        self.assertEquals(updated_xsd_string, expected_string)

    def test_add_appinfo_element_appinfo_present_updates_it(self):
        xsd_string = "<xs:schema xmlns:xs='http://www.w3.org/2001/XMLSchema'><xs:element name='root'><xs:annotation>" \
                     "<xs:appinfo></xs:appinfo></xs:annotation></xs:element></xs:schema>"
        xpath = "xs:element"

        updated_xsd_string = add_appinfo_element(xsd_string, xpath, "attribute", "value")

        expected_string = '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema"><xs:element name="root">' \
                          '<xs:annotation><xs:appinfo><attribute>value</attribute></xs:appinfo></xs:annotation>' \
                          '</xs:element></xs:schema>'
        self.assertEquals(updated_xsd_string, expected_string)

    def test_add_appinfo_element_element_present_updates_it(self):
        xsd_string = "<xs:schema xmlns:xs='http://www.w3.org/2001/XMLSchema'><xs:element name='root'><xs:annotation>" \
                     "<xs:appinfo><attribute>old</attribute></xs:appinfo></xs:annotation></xs:element></xs:schema>"
        xpath = "xs:element"

        updated_xsd_string = add_appinfo_element(xsd_string, xpath, "attribute", "new")

        expected_string = '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema"><xs:element name="root">' \
                          '<xs:annotation><xs:appinfo><attribute>new</attribute></xs:appinfo></xs:annotation>' \
                          '</xs:element></xs:schema>'
        self.assertEquals(updated_xsd_string, expected_string)

    def test_add_appinfo_element_element_absent_from_two_appinfo(self):
        xsd_string = "<xs:schema xmlns:xs='http://www.w3.org/2001/XMLSchema'><xs:element name='root'><xs:annotation>" \
                     "<xs:appinfo></xs:appinfo><xs:appinfo></xs:appinfo></xs:annotation></xs:element></xs:schema>"
        xpath = "xs:element"

        updated_xsd_string = add_appinfo_element(xsd_string, xpath, "attribute", "new")

        expected_string = '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema"><xs:element name="root">' \
                          '<xs:annotation><xs:appinfo><attribute>new</attribute></xs:appinfo><xs:appinfo/>' \
                          '</xs:annotation></xs:element></xs:schema>'
        self.assertEquals(updated_xsd_string, expected_string)

    def test_add_appinfo_element_element_present_in_first_of_two_appinfo(self):
        xsd_string = "<xs:schema xmlns:xs='http://www.w3.org/2001/XMLSchema'><xs:element name='root'><xs:annotation>" \
                     "<xs:appinfo><attribute>old</attribute></xs:appinfo>" \
                     "<xs:appinfo></xs:appinfo></xs:annotation></xs:element></xs:schema>"
        xpath = "xs:element"

        updated_xsd_string = add_appinfo_element(xsd_string, xpath, "attribute", "new")

        expected_string = '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema"><xs:element name="root">' \
                          '<xs:annotation><xs:appinfo><attribute>new</attribute></xs:appinfo><xs:appinfo/>' \
                          '</xs:annotation></xs:element></xs:schema>'
        self.assertEquals(updated_xsd_string, expected_string)

    def test_add_appinfo_element_element_present_in_second_of_two_appinfo(self):
        xsd_string = "<xs:schema xmlns:xs='http://www.w3.org/2001/XMLSchema'><xs:element name='root'><xs:annotation>" \
                     "<xs:appinfo></xs:appinfo>" \
                     "<xs:appinfo><attribute>old</attribute></xs:appinfo></xs:annotation></xs:element></xs:schema>"
        xpath = "xs:element"

        updated_xsd_string = add_appinfo_element(xsd_string, xpath, "attribute", "new")

        expected_string = '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema"><xs:element name="root">' \
                          '<xs:annotation><xs:appinfo/><xs:appinfo><attribute>new</attribute></xs:appinfo>' \
                          '</xs:annotation></xs:element></xs:schema>'
        self.assertEquals(updated_xsd_string, expected_string)

    def test_add_appinfo_element_element_present_in_two_appinfo_raises_exception(self):
        xsd_string = "<xs:schema xmlns:xs='http://www.w3.org/2001/XMLSchema'><xs:element name='root'><xs:annotation>" \
                     "<xs:appinfo><attribute>old</attribute></xs:appinfo>" \
                     "<xs:appinfo><attribute>old</attribute></xs:appinfo></xs:annotation></xs:element></xs:schema>"
        xpath = "xs:element"

        with self.assertRaises(exceptions.XSDError):
            add_appinfo_element(xsd_string, xpath, "attribute", "new")


class TestDeleteAppInfoElement(TestCase):
    def test_delete_appinfo_element_invalid_xsd_raises_xsd_error(self):
        xsd_string = "invalid"
        with self.assertRaises(etree.XMLSyntaxError):
            delete_appinfo_element(xsd_string, "", "")

    def test_delete_appinfo_element_invalid_xpath_raises_xsd_error(self):
        xsd_string = "<xs:schema xmlns:xs='http://www.w3.org/2001/XMLSchema'><root><test></test></root></xs:schema>"
        xpath = "invalid"
        with self.assertRaises(exceptions.XSDError):
            delete_appinfo_element(xsd_string, xpath, "")

    def test_delete_appinfo_element_removed_if_exists(self):
        xsd_string = '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema"><xs:element name="root">' \
                     '<xs:annotation><xs:appinfo><attribute>value</attribute></xs:appinfo></xs:annotation>' \
                     '</xs:element></xs:schema>'
        xpath = "xs:element"
        attribute_name = "attribute"
        updated_xsd_string = delete_appinfo_element(xsd_string, xpath, attribute_name)

        expected_string = '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema"><xs:element name="root">' \
                          '<xs:annotation><xs:appinfo/></xs:annotation>' \
                          '</xs:element></xs:schema>'
        self.assertEquals(updated_xsd_string, expected_string)

    def test_delete_attribute_does_not_fail_if_not_present(self):
        xsd_string = '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema"><xs:element name="root">' \
                     '<xs:annotation><xs:appinfo></xs:appinfo></xs:annotation>' \
                     '</xs:element></xs:schema>'
        xpath = "xs:element"
        attribute_name = "attribute"
        delete_appinfo_element(xsd_string, xpath, attribute_name)

    def test_delete_appinfo_element_element_absent_from_two_appinfo_does_not_fail(self):
        xsd_string = "<xs:schema xmlns:xs='http://www.w3.org/2001/XMLSchema'><xs:element name='root'><xs:annotation>" \
                     "<xs:appinfo></xs:appinfo><xs:appinfo></xs:appinfo></xs:annotation></xs:element></xs:schema>"
        xpath = "xs:element"

        delete_appinfo_element(xsd_string, xpath, "attribute")

    def test_delete_appinfo_element_element_present_in_first_of_two_appinfo(self):
        xsd_string = "<xs:schema xmlns:xs='http://www.w3.org/2001/XMLSchema'><xs:element name='root'><xs:annotation>" \
                     "<xs:appinfo><attribute>old</attribute></xs:appinfo>" \
                     "<xs:appinfo></xs:appinfo></xs:annotation></xs:element></xs:schema>"
        xpath = "xs:element"

        updated_xsd_string = delete_appinfo_element(xsd_string, xpath, "attribute")

        expected_string = '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema"><xs:element name="root">' \
                          '<xs:annotation><xs:appinfo/><xs:appinfo/>' \
                          '</xs:annotation></xs:element></xs:schema>'
        self.assertEquals(updated_xsd_string, expected_string)

    def test_add_appinfo_element_element_present_in_second_of_two_appinfo(self):
        xsd_string = "<xs:schema xmlns:xs='http://www.w3.org/2001/XMLSchema'><xs:element name='root'><xs:annotation>" \
                     "<xs:appinfo></xs:appinfo>" \
                     "<xs:appinfo><attribute>old</attribute></xs:appinfo></xs:annotation></xs:element></xs:schema>"
        xpath = "xs:element"

        updated_xsd_string = delete_appinfo_element(xsd_string, xpath, "attribute")

        expected_string = '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema"><xs:element name="root">' \
                          '<xs:annotation><xs:appinfo/><xs:appinfo/>' \
                          '</xs:annotation></xs:element></xs:schema>'
        self.assertEquals(updated_xsd_string, expected_string)

    def test_add_appinfo_element_element_present_in_two_appinfo_raises_exception(self):
        xsd_string = "<xs:schema xmlns:xs='http://www.w3.org/2001/XMLSchema'><xs:element name='root'><xs:annotation>" \
                     "<xs:appinfo><attribute>old</attribute></xs:appinfo>" \
                     "<xs:appinfo><attribute>old</attribute></xs:appinfo></xs:annotation></xs:element></xs:schema>"
        xpath = "xs:element"

        with self.assertRaises(exceptions.XSDError):
            delete_appinfo_element(xsd_string, xpath, "attribute")