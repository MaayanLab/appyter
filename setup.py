from setuptools import setup, find_packages

setup(
  name='appyter',
  version='0.10.3',
  url='https://github.com/maayanLab/appyter/',
  author='Daniel J. B. Clarke',
  author_email='u8sand@gmail.com',
  long_description=open('README.md', 'r').read(),
  license='CC-BY-NC-SA-4.0',
  install_requires=list(map(str.strip, open('requirements.txt', 'r').readlines())),
  extras_require={
    'production': list(map(str.strip, open('requirements.production.txt', 'r').readlines())),
  },
  packages=find_packages(exclude=('example',)),
  include_package_data=True,
  entry_points={
    'console_scripts': ['appyter=appyter.__main__:main'],
  }
)
