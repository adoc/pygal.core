import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'pillow',
    'sqlalchemy'
    ]

setup(name='galcore',
      version='0.0.2',
      description='',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
          "Programming Language :: Python"
          ],
      author='Nicholas Long',
      author_email='adoc@webmob.net',
      url='https://github.com/adoc/',
      keywords='gallery media',
      packages=find_packages(),
      package_data={'galcore': ['tests/data/*.*']},
      include_package_data=True,
      zip_safe=False,
      test_suite='tests',
      install_requires=requires,
      tests_require=['nose'],
      entry_points= """\
      """
      )
