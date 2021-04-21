""" Utils for djangosaml2 package
"""
import os


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
        contact_person = os.getenv(f"CONTACT_PERSON_{str(contact_person_count+1)}")
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
