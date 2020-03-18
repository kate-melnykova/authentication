from setuptools import setup
from setuptools import find_packages
from pip._internal.req import parse_requirements
import pkg_resources
import pathlib

with open("README.md", "r+") as fh:
    long_description = fh.read()

setup(
    name='authentication',
    version='1.1.0',
    packages=find_packages(),
    package_data={'authentication': ['templates/*']},
    install_requires=['Flask >= 1.0', 'pycryptodome', 'wtforms', 'passlib', 'redis'],
    url='',
    license='MIT',
    author='Kateryna Melnykova',
    author_email='forkatemelnikova@gmail.com',
    description='Learning authentication',
    long_description=long_description,
    long_description_content_type="text/markdown"
)
