#!/usr/bin/env python3
import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='pyceditor',
    version='0.9.0',
    author='Komissarov Andrey',
    author_email='komissar.off.andrey@gmail.com',
    description='Tool for editing PYC files and Python bytecode in runtime',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/moff4/pyceditor',
    install_requires=[],
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
