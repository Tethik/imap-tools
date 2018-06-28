import re
import sys
from setuptools import setup, find_packages

with open("LICENSE") as f:
    LICENSE = f.read()

setup(
    name='imap-tools',
    version='1.0.0',
    author='Joakim Uddholm',
    author_email='tethik@gmail.com',
    description='Commandline Interface to load .env from vault',
    url='https://github.com/Tethik/imap-tools',
    py_modules=['download','upload'],
    entry_points = {
        'console_scripts': ['imap-download=download:cli', 'imap-upload=upload:cli'],
    },
    zip_safe=True,
    package_data={'': ['LICENSE', 'README.md']},
    include_package_data=True,
    install_requires=[
        "click"
    ],
    license=LICENSE,
    classifiers=[
        'Development Status :: 3 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT',        
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python',
    ]
)