import os
import re

from setuptools import setup, find_packages

# Do not try to import the package to get its version.
_version_file = open(os.path.join(os.path.dirname(__file__), 'dokang', 'version.py'))
VERSION = re.compile(r"^VERSION = '(.*?)'", re.S).match(_version_file.read()).group(1)


def load_requirements(path):
    with open(path) as fp:
        return [line for line in fp.read().split("\n")
            if line and not line.startswith(("-r", "#"))]


here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README')).read().strip()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read().strip()

setup(name='Dokang',
      private_repository="https://@pypi.autolib.polyconseil.fr/",
      version=VERSION,
      license="Proprietary",
      description="Lightweight search engine with a web frontend",
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "Topic :: Text Processing :: Markup :: HTML",
        ],
      author="Polyconseil",
      author_email="",
      url='',
      keywords='full-text search engine',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=load_requirements('requirements.txt'),
      tests_require=load_requirements('requirements_dev.txt'),
      test_suite='tests',
      entry_points="""\
      [paste.app_factory]
      main = dokang.app:make_app

      [console_scripts]
      dokang = dokang.cli:main
      """,
      )
