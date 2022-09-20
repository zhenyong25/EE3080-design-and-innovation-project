#!/usr/bin/env python3
from setuptools import find_packages
from setuptools import setup

setup(
    name='edlib',
    version='1.0.0',
    packages=find_packages(exclude=['examples', 'tests']),

    description='Espdrone python driver',
    url='https://github.com/NelsenEW/espdrone-lib-python',

    author='Bitcraze and contributors',
    author_email='contact@bitcraze.io',
    license='GPLv3',
    maintainer='Nelsen, Andrian, Justin',

    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Topic :: System :: Hardware :: Hardware Drivers',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3'
    ],

    keywords='driver espdrone quadcopter',

    install_requires=['pyusb==1.0.0b2', 'opencv-python<4.3'],
)
