import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'requirements.txt')) as f:
    required = f.read().splitlines()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name="core_main_app",
    version="0.0.1-alpha1",
    description=("core main Django package",),
    author="no_author",
    author_email="contact@example.com",

    packages=find_packages(),
    include_package_data=True,
    # package_dir={
    #     '': 'src',
    # },
    #
    install_requires=required,
)
