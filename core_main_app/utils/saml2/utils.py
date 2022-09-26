""" Utils for djangosaml2 package
"""
import os

import saml2
import saml2.saml


def load_attribute_map_from_env():
    """Load attribute map from environment (https://pysaml2.readthedocs.io/en/latest/howto/config.html#attribute-map-dir)

    Returns:

    """
    return {
        "identifier": os.environ["SAML_ATTRIBUTES_MAP_IDENTIFIER"],
        "fro": {
            os.environ["SAML_ATTRIBUTES_MAP_UID"]: os.environ[
                "SAML_ATTRIBUTES_MAP_UID_FIELD"
            ],
            os.environ["SAML_ATTRIBUTES_MAP_EMAIL"]: os.environ[
                "SAML_ATTRIBUTES_MAP_EMAIL_FIELD"
            ],
            os.environ["SAML_ATTRIBUTES_MAP_SN"]: os.environ[
                "SAML_ATTRIBUTES_MAP_SN_FIELD"
            ],
            os.environ["SAML_ATTRIBUTES_MAP_CN"]: os.environ[
                "SAML_ATTRIBUTES_MAP_CN_FIELD"
            ],
        },
        "to": {
            os.environ["SAML_ATTRIBUTES_MAP_UID_FIELD"]: os.environ[
                "SAML_ATTRIBUTES_MAP_UID"
            ],
            os.environ["SAML_ATTRIBUTES_MAP_EMAIL_FIELD"]: os.environ[
                "SAML_ATTRIBUTES_MAP_EMAIL"
            ],
            os.environ["SAML_ATTRIBUTES_MAP_SN_FIELD"]: os.environ[
                "SAML_ATTRIBUTES_MAP_SN"
            ],
            os.environ["SAML_ATTRIBUTES_MAP_CN_FIELD"]: os.environ[
                "SAML_ATTRIBUTES_MAP_CN"
            ],
        },
    }


def load_django_attribute_map_from_env():
    """Load attribute mapping for Django from environment (https://djangosaml2.readthedocs.io/contents/setup.html#users-attributes-and-account-linking)

    Returns:

    """
    return {
        os.environ["SAML_ATTRIBUTES_MAP_UID_FIELD"]: ("username",),
        os.environ["SAML_ATTRIBUTES_MAP_EMAIL_FIELD"]: ("email",),
        os.environ["SAML_ATTRIBUTES_MAP_CN_FIELD"]: ("first_name",),
        os.environ["SAML_ATTRIBUTES_MAP_SN_FIELD"]: ("last_name",),
    }


def load_saml_config_from_env(server_uri, base_dir):
    """Load SAML configuration from environment (https://pysaml2.readthedocs.io/en/latest/howto/config.html#configuration-of-pysaml2-entities)

    Args:
        server_uri:
        base_dir:

    Returns:

    """

    contact_person = load_contact_person_from_env()
    organization = load_organization_from_env()
    return {
        # full path to the xmlsec1 binary programm
        "xmlsec_binary": os.getenv("SAML_XMLSEC_BIN_PATH", "/usr/bin/xmlsec1"),
        # your entity id, usually your subdomain plus the url to the metadata view
        "entityid": f"{server_uri}/saml2/metadata/",
        # directory with attribute mapping
        "attribute_map_dir": os.path.join(
            base_dir, os.getenv("SAML_ATTRIBUTE_MAP_DIR", "attr-maps")
        ),
        # this block states what services we provide
        "service": {
            # we are just a lonely SP
            "sp": {
                "want_response_signed": os.getenv(
                    "SAML_WANT_RESPONSE_SIGNED", "False"
                ).lower()
                == "true",
                "want_assertions_signed": os.getenv(
                    "SAML_WANT_ASSERTIONS_SIGNED", "False"
                ).lower()
                == "true",
                "name": os.getenv("SERVER_NAME", "Curator"),
                "name_id_format": saml2.saml.NAMEID_FORMAT_TRANSIENT,
                # For Okta add signed logout requets. Enable this:
                "logout_requests_signed": os.getenv(
                    "SAML_LOGOUT_REQUESTS_SIGNED", "True"
                ).lower()
                == "true",
                "logout_responses_signed": os.getenv(
                    "SAML_LOGOUT_RESPONSES_SIGNED", "False"
                ).lower()
                == "true",
                "signing_algorithm": os.getenv(
                    "SAML_SIGNING_ALGORITHM",
                    "http://www.w3.org/2001/04/xmldsig-more#rsa-sha512",
                ),
                "digest_algorithm": os.getenv(
                    "SAML_DIGEST_ALGORITHM",
                    "http://www.w3.org/2001/04/xmlenc#sha512",
                ),
                "endpoints": {
                    # url and binding to the assertion consumer service view
                    # do not change the binding or service name
                    "assertion_consumer_service": [
                        (f"{server_uri}/saml2/acs/", saml2.BINDING_HTTP_POST),
                    ],
                    # url and binding to the single logout service view
                    # do not change the binding or service name
                    "single_logout_service": [
                        # Disable next two lines for HTTP_REDIRECT for IDP's that only support HTTP_POST. Ex. Okta:
                        (
                            f"{server_uri}/saml2/ls/",
                            saml2.BINDING_HTTP_REDIRECT,
                        ),
                        (
                            f"{server_uri}/saml2/ls/post/",
                            saml2.BINDING_HTTP_POST,
                        ),
                    ],
                },
                # Mandates that the identity provider MUST authenticate the
                # presenter directly rather than rely on a previous security context.
                "force_authn": False,
                # Enable AllowCreate in NameIDPolicy.
                "name_id_format_allow_create": False,
                # attributes that this project need to identify a user
                "required_attributes": ["givenName", "sn", "mail"],
            },
        },
        # where the remote metadata is stored, local, remote or mdq server.
        # One metadata store or many ...
        "metadata": {
            "remote": [
                {
                    "url": os.environ["SAML_METADATA_REMOTE"],
                    "cert": os.getenv("SAML_METADATA_REMOTE_CERT"),
                },
            ]
            if "SAML_METADATA_REMOTE" in os.environ
            else [],
            "local": [os.environ["SAML_METADATA_LOCAL"]]
            if "SAML_METADATA_LOCAL" in os.environ
            else [],
        },
        # Signing
        "key_file": os.getenv("SAML_KEY_FILE", None),  # private part
        "cert_file": os.getenv("SAML_CERT_FILE", None),  # public part
        # Encryption
        "encryption_keypairs": [
            {
                "key_file": os.getenv("SAML_KEY_FILE", None),  # private part
                "cert_file": os.getenv("SAML_CERT_FILE", None),  # public part
            }
        ],
        "contact_person": contact_person,
        "organization": organization,
    }


def load_contact_person_from_env():
    """Load PySAML2 contact person configurations from environment (https://pysaml2.readthedocs.io/en/latest/howto/config.html#contact-person)

    Examples:
        CONTACT_PERSON_1=Firstname1,Lastname1,Example Co.,contact1@example.com,technical
        CONTACT_PERSON_2=Firstname2,Lastname2,Example Co.,contact2@example.com,administrative

    Returns:

    """
    contact_person_list = list()
    contact_person_count = 0
    while 1:
        contact_person = os.getenv(
            f"CONTACT_PERSON_{str(contact_person_count+1)}"
        )
        if contact_person:
            contact_person_info = contact_person.split(",")
            contact_person_list.append(
                {
                    "given_name": contact_person_info[0],
                    "sur_name": contact_person_info[1],
                    "company": contact_person_info[2],
                    "email_address": contact_person_info[3],
                    "contact_type": contact_person_info[4],
                }
            )
            contact_person_count += 1
        else:
            break

    return contact_person_list


def load_organization_from_env():
    """Load PySAML2 organization configurations from environment (https://pysaml2.readthedocs.io/en/latest/howto/config.html#organization)

    Examples:
        ORGANIZATION_NAME_1=Example Company,en
        ORGANIZATION_NAME_2=Exempel AB,se
        ORGANIZATION_DISPLAY_NAME_1=Exempel AB,se
        ORGANIZATION_URL_1=http://example.com,en
        ORGANIZATION_URL_2=http://exemple.se,se

    Returns:

    """
    organization_dict = dict()

    for organization_config in ["name", "display_name", "url"]:
        organization_dict[organization_config] = list()
        organization_config_count = 0
        while 1:
            organization_config_value = os.getenv(
                f"ORGANIZATION_{organization_config.upper()}_{str(organization_config_count+1)}"
            )
            if organization_config_value:
                organization_dict[organization_config].append(
                    tuple(organization_config_value.split(","))
                )
                organization_config_count += 1
            else:
                break

    return organization_dict
