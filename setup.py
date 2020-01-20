from setuptools import setup
from setuptools import find_packages

setup(
    name='authentication',
    version='1.0',
    packages=find_packages(),
    package_data={'authentication': ['templates/*']},
    install_requires=['Flask >= 1.0', 'pycryptodome', 'wtforms', 'passlib'],
    url='',
    license='MIT',
    author='katyandrey',
    author_email='forkatemelnikova@gmail.com',
    description='Learning authentication'
)
