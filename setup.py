import os
from setuptools import setup

readme_path = os.path.join(os.path.dirname(
  os.path.abspath(__file__)),
  'README.rst',
)
long_description = open(readme_path).read()
version_path = os.path.join(os.path.dirname(
  os.path.abspath(__file__)),
  'VERSION',
)
version = open(version_path).read()

setup(
  name='wtforms-webwidgets',
  version=version,
  packages=['wtforms_webwidgets'],
  author="Nick Whyte",
  author_email='nick@nickwhyte.com',
  description="Additional Widgets for WTForms for common web libraries",
  long_description=long_description,
  url='https://github.com/nickw444/wtforms-webwidgets',
  zip_safe=False,
  include_package_data=True,
  install_requires=[
        "wtforms",
  ],
  classifiers=[
    'Intended Audience :: Developers',
    'Programming Language :: Python',
    'Environment :: Web Environment',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 2.6',
  ],
)
