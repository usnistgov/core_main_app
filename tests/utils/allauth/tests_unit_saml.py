""" Allauth SAML utils test class
"""

import os
from unittest import TestCase

from core_main_app.utils.allauth.saml import (
    load_verified_email_from_env,
    load_allauth_contact_person_dict_from_env,
    load_allauth_saml_conf_from_env,
)


class TestLoadAllauthSamlConfFromEnv(TestCase):
    """TestLoadAllauthSamlConfFromEnv"""

    def test_load_allauth_saml_conf_from_env_returns_correct_conf(self):
        """test_load_allauth_saml_conf_from_env_returns_correct_conf

        Returns:

        """
        os.environ["SAML_CLIENT_ID"] = "mdcs"
        os.environ["SAML_PROVIDER_NAME"] = "Test Keycloak"
        os.environ["SAML_PROVIDER_ID"] = "Keycloak"
        os.environ["SAML_IDP_ENTITY_ID"] = (
            "http://localhost:8080/auth/realms/cdcs-realm"
        )
        os.environ["SAML_IDP_METADATA_URL"] = (
            "http://localhost:8080/auth/realms/cdcs-realm/protocol/saml/descriptor/"
        )
        os.environ["SAML_ATTRIBUTES_MAP_UID_FIELD"] = "uid"
        os.environ["SAML_ATTRIBUTES_MAP_EMAIL_FIELD"] = "email"
        os.environ["SAML_ATTRIBUTES_MAP_CN_FIELD"] = "first_name"
        os.environ["SAML_ATTRIBUTES_MAP_SN_FIELD"] = "last_name"

        os.environ["SAML_ATTRIBUTES_MAP_UID"] = (
            "urn:oid:0.9.2342.19200300.100.1.1"
        )
        os.environ["SAML_ATTRIBUTES_MAP_EMAIL"] = (
            "urn:oid:1.2.840.113549.1.9.1"
        )
        os.environ["SAML_ATTRIBUTES_MAP_CN"] = "urn:oid:2.5.4.42"
        os.environ["SAML_ATTRIBUTES_MAP_SN"] = "urn:oid:2.5.4.4"

        self.assertEqual(
            {
                "EMAIL_AUTHENTICATION": False,
                "VERIFIED_EMAIL": False,
                "APPS": [
                    {
                        "name": "Test Keycloak",
                        "provider_id": "Keycloak",
                        "client_id": "mdcs",
                        "settings": {
                            "attribute_mapping": {
                                "uid": "urn:oid:0.9.2342.19200300.100.1.1",
                                "email": "urn:oid:1.2.840.113549.1.9.1",
                                "first_name": "urn:oid:2.5.4.42",
                                "last_name": "urn:oid:2.5.4.4",
                            },
                            "use_nameid_for_email": False,
                            "idp": {
                                "entity_id": "http://localhost:8080/auth/realms/cdcs-realm",
                                "metadata_url": "http://localhost:8080/auth/realms/cdcs-realm/protocol/saml/descriptor/",
                            },
                            "sp": {"entity_id": None},
                            "advanced": {
                                "allow_repeat_attribute_name": True,
                                "allow_single_label_domains": False,
                                "authn_request_signed": False,
                                "digest_algorithm": "http://www.w3.org/2001/04/xmldsig-more#rsa-sha256",
                                "logout_request_signed": False,
                                "logout_response_signed": False,
                                "metadata_signed": False,
                                "name_id_encrypted": False,
                                "name_id_format": "urn:oasis:names:tc:SAML:1.1:nameid-format:unspecified",
                                "private_key": None,
                                "reject_deprecated_algorithm": True,
                                "reject_idp_initiated_sso": True,
                                "signature_algorithm": "http://www.w3.org/2001/04/xmldsig-more#rsa-sha256",
                                "want_assertion_encrypted": False,
                                "want_assertion_signed": False,
                                "want_attribute_statement": True,
                                "want_message_signed": False,
                                "want_name_id": False,
                                "want_name_id_encrypted": False,
                                "x509cert": None,
                            },
                            "contact_person": {},
                        },
                    }
                ],
            },
            load_allauth_saml_conf_from_env(),
        )


class TestLoadAllauthContactPersonDictFromEnv(TestCase):
    """TestLoadAllauthContactPersonDictFromEnv"""

    def test_load_allauth_contact_person_dict_from_env_returns_dict(self):
        """test_load_allauth_contact_person_dict_from_env_returns_dict

        Returns:

        """
        os.environ["CONTACT_PERSON_1"] = (
            "Firstname1,Lastname1,Example Co.,contact1@example.com,technical"
        )
        self.assertEqual(
            {
                "technical": {
                    "givenName": "Firstname1",
                    "surName": "Lastname1",
                    "company": "Example Co.",
                    "emailAddress": "contact1@example.com",
                }
            },
            load_allauth_contact_person_dict_from_env(),
        )

    def test_load_allauth_contact_person_dict_from_env_returns_dict_with_two_contacts(
        self,
    ):
        """test_load_allauth_contact_person_dict_from_env_returns_dict_with_two_contacts

        Returns:

        """
        os.environ["CONTACT_PERSON_1"] = (
            "Firstname1,Lastname1,Example Co.,contact1@example.com,technical"
        )
        os.environ["CONTACT_PERSON_2"] = (
            "Firstname2,Lastname2,Example Co.,contact2@example.com,administrative"
        )
        self.assertEqual(
            {
                "technical": {
                    "givenName": "Firstname1",
                    "surName": "Lastname1",
                    "company": "Example Co.",
                    "emailAddress": "contact1@example.com",
                },
                "administrative": {
                    "givenName": "Firstname2",
                    "surName": "Lastname2",
                    "company": "Example Co.",
                    "emailAddress": "contact2@example.com",
                },
            },
            load_allauth_contact_person_dict_from_env(),
        )

    def test_load_allauth_contact_person_dict_from_env_returns_empty_dict(
        self,
    ):
        """test_load_allauth_contact_person_dict_from_env_returns_empty_dict

        Returns:

        """
        if "CONTACT_PERSON_1" in os.environ:
            del os.environ["CONTACT_PERSON_1"]
        if "CONTACT_PERSON_2" in os.environ:
            del os.environ["CONTACT_PERSON_2"]

        self.assertEqual({}, load_allauth_contact_person_dict_from_env())


class TestLoadVerifiedEmailFromEnv(TestCase):
    """TestLoadVerifiedEmailFromEnv"""

    def test_load_verified_email_from_env_returns_true_if_env_true(self):
        """test_load_verified_email_from_env_returns_true_if_env_true

        Returns:

        """
        os.environ["SAML_VERIFIED_EMAIL"] = "True"
        self.assertTrue(load_verified_email_from_env())

    def test_load_verified_email_from_env_returns_false_if_env_false(self):
        """test_load_verified_email_from_env_returns_false_if_env_false

        Returns:

        """
        os.environ["SAML_VERIFIED_EMAIL"] = "False"
        self.assertFalse(load_verified_email_from_env())

    def test_load_verified_email_from_env_returns_list_if_env_string(self):
        """test_load_verified_email_from_env_returns_list_if_env_string

        Returns:

        """
        os.environ["SAML_VERIFIED_EMAIL"] = "example.com"
        self.assertEqual(["example.com"], load_verified_email_from_env())

    def test_load_verified_email_from_env_returns_list_if_env_comma_separated_list(
        self,
    ):
        """test_load_verified_email_from_env_returns_list_if_env_comma_separated_list

        Returns:

        """
        os.environ["SAML_VERIFIED_EMAIL"] = "example.com,test.example.com"
        self.assertEqual(
            ["example.com", "test.example.com"], load_verified_email_from_env()
        )

    def test_load_verified_email_from_env_returns_false_if_env_not_set(self):
        """test_load_verified_email_from_env_returns_false_if_env_not_set

        Returns:

        """
        if "SAML_VERIFIED_EMAIL" in os.environ:
            del os.environ["SAML_VERIFIED_EMAIL"]
        self.assertFalse(load_verified_email_from_env())
