from setuptools import find_packages
import os

from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install

dir_path = os.path.dirname(os.path.realpath(__file__))


class PostDevelopCommand(develop):
    """Post-installation for development mode."""

    def run(self):
        # PUT YOUR POST-INSTALL SCRIPT HERE or CALL A FUNCTION
        develop.run(self)


class PostInstallCommand(install):
    """Post-installation for installation mode."""

    def run(self):
        # PUT YOUR POST-INSTALL SCRIPT HERE or CALL A FUNCTION
        install.run(self)


setup(
    name='ybsapi',
    url='https://github.com/nickyfoster/ybsapi2',
    description='YBS Api server',
    keywords='YBS nlu server API',
    packages=find_packages(exclude=['test', 'test.*']),
    install_requires=[
        "Django==2.2.13",
        "psycopg2==2.8.4",
        "djangorestframework==3.10.3",
        "mysqlclient",
        "idna",
        "ufal.udpipe",
        "conllu",
        "pytest"
    ],
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
    },
)
