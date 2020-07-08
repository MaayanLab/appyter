from setuptools import setup, find_packages

requirements = list(map(str.strip, open('requirements.txt', 'r').readlines()))

setup(
  name='appyter',
  version='0.6.6',
  url='https://github.com/maayanLab/appyter/',
  author='Daniel J. B. Clarke',
  author_email='u8sand@gmail.com',
  long_description=open('README.md', 'r').read(),
  license='Apache-2.0',
  install_requires=[requirement for requirement in requirements if '://' not in requirement],
  dependency_links=[requirement for requirement in requirements if '://' in requirement],
  packages=find_packages(exclude=('example',)),
  include_package_data=True,
  entry_points={
    'console_scripts': ['appyter=appyter.__main__:main'],
  }
)
