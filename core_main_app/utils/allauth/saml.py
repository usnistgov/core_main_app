""" Utils for allauth saml configuration
"""

import os


def load_allauth_saml_conf_from_env():
    """Load allauth saml conf from env
    Doc: https://docs.allauth.org/en/latest/socialaccount/providers/saml.html

    Returns:

    """
    return {
        "EMAIL_AUTHENTICATION": os.getenv(
            "SAML_EMAIL_AUTHENTICATION", "False"
        ).lower()
        == "true",
        "VERIFIED_EMAIL": load_verified_email_from_env(),
        # Here, each app represents the SAML provider configuration of one
        # organization.
        "APPS": [
            {
                # Used for display purposes, e.g. over by: {% get_providers %}
                "name": os.getenv("SAML_PROVIDER_NAME"),
                # Accounts signed up via this provider will have their
                # `SocialAccount.provider` value set to this ID. The combination
                # of this value and the `uid` must be unique. The IdP entity ID is a
                # good choice for this.
                "provider_id": os.getenv("SAML_PROVIDER_ID"),
                # The organization slug is configured by setting the
                # `client_id` value. In this example, the SAML login URL is:
                #
                #     /accounts/saml/mdcs/login/
                "client_id": os.getenv("SAML_CLIENT_ID"),
                # The fields above are common `SocialApp` fields. For SAML,
                # additional configuration is needed, which is placed in
                # `SocialApp.settings`:
                "settings": {
                    # Mapping account attributes to upstream (IdP specific) attributes.
                    # If left empty, an attempt will be done to map the attributes using
                    # built-in defaults.
                    "attribute_mapping": {
                        os.getenv("SAML_ATTRIBUTES_MAP_UID_FIELD"): os.getenv(
                            "SAML_ATTRIBUTES_MAP_UID"
                        ),
                        os.getenv(
                            "SAML_ATTRIBUTES_MAP_EMAIL_FIELD"
                        ): os.getenv("SAML_ATTRIBUTES_MAP_EMAIL"),
                        os.getenv("SAML_ATTRIBUTES_MAP_CN_FIELD"): os.getenv(
                            "SAML_ATTRIBUTES_MAP_CN"
                        ),
                        os.getenv("SAML_ATTRIBUTES_MAP_SN_FIELD"): os.getenv(
                            "SAML_ATTRIBUTES_MAP_SN"
                        ),
                    },
                    # The following setting allows you to force the use of nameID as email.
                    # This can be useful if you are using a SAML IdP that is broken in some way and
                    # does not allow use of the emailAddress nameid format
                    "use_nameid_for_email": os.getenv(
                        "SAML_USE_NAMEID_FOR_EMAIL", "False"
                    ).lower()
                    == "true",
                    # The configuration of the IdP.
                    "idp": {
                        # The entity ID of the IdP is required.
                        "entity_id": os.getenv("SAML_IDP_ENTITY_ID"),
                        # Then, you can either specify the IdP's metadata URL:
                        "metadata_url": os.getenv("SAML_IDP_METADATA_URL"),
                        # Or, you can inline the IdP parameters here as follows:
                        # "sso_url": "https://example.com/saml2/sso",
                        # "slo_url": "https://example.com/saml2/slo",
                        # "x509cert": """
                        # """,
                    },
                    # The configuration of the SP.
                    "sp": {
                        # Optional entity ID of the SP. If not set, defaults to the `saml_metadata` urlpattern
                        "entity_id": os.getenv("SAML_SP_ENTITY_ID", None),
                    },
                    # Advanced settings.
                    "advanced": {
                        "allow_repeat_attribute_name": os.getenv(
                            "SAML_ALLOW_REPEAT_ATTRIBUTE_NAME", "True"
                        ).lower()
                        == "true",
                        "allow_single_label_domains": os.getenv(
                            "SAML_ALLOW_SINGLE_LABEL_DOMAINS", "False"
                        ).lower()
                        == "true",
                        "authn_request_signed": os.getenv(
                            "SAML_AUTHN_REQUEST_SIGNED", "False"
                        ).lower()
                        == "true",
                        "digest_algorithm": os.getenv(
                            "SAML_DIGEST_ALGORITHM",
                            "http://www.w3.org/2001/04/xmldsig-more#rsa-sha256",
                        ),
                        "logout_request_signed": os.getenv(
                            "SAML_LOGOUT_REQUEST_SIGNED", "False"
                        ).lower()
                        == "true",
                        "logout_response_signed": os.getenv(
                            "SAML_LOGOUT_RESPONSE_SIGNED", "False"
                        ).lower()
                        == "true",
                        "metadata_signed": os.getenv(
                            "SAML_METADATA_SIGNED", "False"
                        ).lower()
                        == "true",
                        "name_id_encrypted": os.getenv(
                            "SAML_NAME_ID_ENCRYPTED", "False"
                        ).lower()
                        == "true",
                        "name_id_format": os.getenv(
                            "SAML_NAME_ID_FORMAT",
                            "urn:oasis:names:tc:SAML:1.1:nameid-format:unspecified",
                        ),
                        "private_key": os.getenv("SAML_PRIVATE_KEY", None),
                        "reject_deprecated_algorithm": os.getenv(
                            "SAML_REJECT_DEPRECATED_ALGORITHM", "True"
                        ).lower()
                        == "true",
                        # Due to security concerns, IdP initiated SSO is rejected by default.
                        "reject_idp_initiated_sso": os.getenv(
                            "SAML_REJECT_IDP_INITIATED_SSO", "True"
                        ).lower()
                        == "true",
                        "signature_algorithm": os.getenv(
                            "SAML_SIGNATURE_ALGORITHM",
                            "http://www.w3.org/2001/04/xmldsig-more#rsa-sha256",
                        ),
                        "want_assertion_encrypted": os.getenv(
                            "SAML_WANT_ASSERTION_ENCRYPTED", "False"
                        ).lower()
                        == "true",
                        "want_assertion_signed": os.getenv(
                            "SAML_WANT_ASSERTION_SIGNED", "False"
                        ).lower()
                        == "true",
                        "want_attribute_statement": os.getenv(
                            "SAML_WANT_ATTRIBUTE_STATEMENT", "True"
                        ).lower()
                        == "true",
                        "want_message_signed": os.getenv(
                            "SAML_WANT_MESSAGE_SIGNED", "False"
                        ).lower()
                        == "true",
                        "want_name_id": os.getenv(
                            "SAML_WANT_NAME_ID", "False"
                        ).lower()
                        == "true",
                        "want_name_id_encrypted": os.getenv(
                            "SAML_WANT_NAME_ID_ENCRYPTED", "False"
                        ).lower()
                        == "true",
                        "x509cert": os.getenv("SAML_X509CERT", None),
                    },
                    "contact_person": load_allauth_contact_person_dict_from_env(),
                },
            },
        ],
    }


def load_allauth_contact_person_dict_from_env():
    """Load Django Allauth contact person configurations from environment

    Examples:
        CONTACT_PERSON_1=Firstname1,Lastname1,Example Co.,contact1@example.com,technical
        CONTACT_PERSON_2=Firstname2,Lastname2,Example Co.,contact2@example.com,administrative

    Returns:

    """
    contact_person_dict = dict()
    contact_person_count = 0
    while 1:
        contact_person = os.getenv(
            f"CONTACT_PERSON_{str(contact_person_count+1)}"
        )
        if contact_person:
            contact_person_info = contact_person.split(",")
            contact_person_dict[contact_person_info[4]] = {
                "givenName": contact_person_info[0],
                "surName": contact_person_info[1],
                "company": contact_person_info[2],
                "emailAddress": contact_person_info[3],
            }

            contact_person_count += 1
        else:
            break

    return contact_person_dict


def load_verified_email_from_env():
    """Load verified email from environment

    Returns:

    """
    verified_emails_env = os.getenv("SAML_VERIFIED_EMAIL", None)

    # SAML_VERIFIED_EMAIL not set, return False
    if not verified_emails_env:
        return False

    # SAML_VERIFIED_EMAIL is a boolean, return True
    if verified_emails_env.lower() == "true":
        return True

    # SAML_VERIFIED_EMAIL is a boolean, return False
    if verified_emails_env.lower() == "false":
        return False

    # SAML_VERIFIED_EMAIL is a list of domains
    return verified_emails_env.split(",")
