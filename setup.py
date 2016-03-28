# !/usr/bin/env python
# coding=utf-8


from setuptools import setup, find_packages
import SillyNews

setup(
    name="SillyBlog",
    version=SillyNews.__VERSION__,
    author=SillyNews.__AUTHOR__,
    url=SillyNews.__URL__,
    license=SillyNews.__LICENSE__,
    packages=find_packages(),
    description="A silly news platform",
    keywords="silly news",
    test_suite="nose.collector"
)
