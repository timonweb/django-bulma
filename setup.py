#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open("README.md") as readme_file:
    readme = readme_file.read()

setup(
    name="django-bulma",
    description="""Bulma CSS Framework for Django projects""",
    long_description=readme,
    author="Tim Kamanin",
    author_email="tim@timonweb.com",
    url="https://timonweb.com/oss/django-bulma/",
    packages=["bulma"],
    include_package_data=True,
    use_scm_version={
        'write_to': "bulma/version.py",
        'version_scheme': 'guess-next-dev',
        'local_scheme': 'node-and-date',
    },
    setup_requires=[
        'setuptools_scm'
    ],
    install_requires=[],
    license="The MIT License (MIT)",
    zip_safe=False,
    keywords="django-bulma",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.6",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
        "Environment :: Web Environment",
        "Framework :: Django",
    ],
)
