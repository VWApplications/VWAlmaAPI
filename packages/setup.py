import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# Allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-vwa-accounts',
    version='0.1.1',
    packages=find_packages(),
    include_package_data=True,
    license='GENERAL PUBLIC LICENSE',
    description='A simple Django app to manage users',
    long_description=README,
    long_description_content_type="text/markdown",
    keywords='api accounts rest users',
    url='https://github.com/VictorArnaud/vwa-accounts',
    author='Victor Arnaud',
    author_email='victorhad@gmail.com',
    install_requires=['django', 'djangorestframework', 'pytest-django', 'pillow'],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.1',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
    ],
)
