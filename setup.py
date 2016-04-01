import os
import re

from setuptools import setup, find_packages

from dokang import __version__


def read(filename):
    with open(filename) as fp:
        return fp.read().strip()


setup(
    name='Dokang',
    version='0.9.0',
    description="Lightweight web documentation repository with a search engine",
    long_description='%s\n\n%s' % (read('README.rst'), read('CHANGES.rst')),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "Topic :: Text Processing :: Markup :: HTML",
    ],
    author="Polyconseil",
    author_email="opensource+dokang@polyconseil.fr",
    url='https://dokang.readthedocs.org/',
    keywords='documentation repository search engine',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'beautifulsoup4==4.4.0',
        'Chameleon==2.22',
        'pyramid==1.5.7',
        'pyramid_chameleon==0.3',
        'Whoosh==2.7.0',
        'WTForms==2.0.2',
    ],
    entry_points={
        'paste.app_factory': [
            'main=dokang.app:make_app',
        ],
        'console_scripts': [
            'dokang=dokang.cli:main',
        ],
    },
)
