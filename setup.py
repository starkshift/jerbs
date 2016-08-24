# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='jerbs',
    version='0.0.1 ALPHA',
    description='A Python package to help figure out who took our jerbs.',
    long_description=readme,
    author='Russell Miller',
    author_email='russlmiller@gmail.com',
    url='https://github.com/starkshift/jerbs',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
