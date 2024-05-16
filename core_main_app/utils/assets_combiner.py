""" Assets combiner utils
"""


def join_assets(*dicts):
    joined_assets = {}
    # Create a set of all keys present in any of the dictionaries
    all_keys = set().union(*[d.keys() for d in dicts])

    # Iterate over each key
    for key in all_keys:
        # Sum up the values from all dictionaries, using an empty list as default
        joined_assets[key] = sum((d.get(key, []) for d in dicts), [])

    return joined_assets
