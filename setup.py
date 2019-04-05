import os
import sys

from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # Import here, cause outside the eggs aren't loaded.
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup(
    name='django-bi',
    version='1.0.29',
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    license='GPLv3 License',
    description='A simple Django app to conduct business intelligence.',
    long_description=README,
    url='https://zhelyabuzhsky.com/',
    author='Ilya Zhelyabuzhsky',
    author_email='zhelyabuzhsky@icloud.com',
    install_requires=['Django', 'pandas'],
    test_suite='tests',
    tests_require=['pytest-django'],
    cmdclass={'test': PyTest},
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.1',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
