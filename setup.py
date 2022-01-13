from os import chdir, pardir
from os.path import join, exists, dirname, normpath, abspath
from re import sub

from setuptools import find_packages, setup


def req_link(external_url):
    egg_link = sub(r"https://[^=]+=", "", external_url)
    return "==".join(egg_link.rsplit("-", 1))


def read_requirements_file(requirements_filepath):
    requirements = list()

    if not exists(requirements_filepath):
        return requirements

    with open(requirements_filepath) as requirements_fp:
        requirements += requirements_fp.read().splitlines()

    return requirements


reqs_dev = join(dirname(__file__), "requirements.dev.txt")
reqs_default = join(dirname(__file__), "requirements.txt")
reqs_core = join(dirname(__file__), "requirements.core.txt")
required = []

required += read_requirements_file(reqs_default)
required += read_requirements_file(reqs_core)

extra = read_requirements_file(reqs_dev)

dep_links = [r for r in required if r.startswith("https://")]
required = [req_link(r) if r.startswith("https://") else r for r in required]

with open(join(dirname(__file__), "README.rst")) as f:
    long_desc = f.read()

# Allow setup.py to be run from any path
chdir(normpath(join(abspath(__file__), pardir)))

setup(
    name="core_main_app",
    version="1.20.0",
    description="Main functionalities for the curator core project",
    long_description=long_desc,
    author="NIST IT Lab",
    author_email="itl_inquiries@nist.gov",
    url="https://github.com/usnistgov/core_main_app",
    packages=find_packages(),
    include_package_data=True,
    install_requires=required,
    dependency_links=dep_links,
    extras_require={"develop": extra},
)
