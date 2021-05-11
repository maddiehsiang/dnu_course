#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()


requirements = []

setup_requirements = ['pytest-runner', 'numpy', 'xarray', 'altair',
                      'pandas', 'arviz', 'nbval', 'bokeh', 'hvplot']

test_requirements = ['pytest>=3', ]

setup(
    author="Maxym Myroshnychenko",
    author_email='mmyros@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="",
    entry_points={
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n',
    include_package_data=True,
    keywords='',
    name='dnu_course',
    # packages=find_packages(include=['bayes_window', 'bayes_window.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    version='0.1.1',
    zip_safe=False,
)
