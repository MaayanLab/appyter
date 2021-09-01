from setuptools import setup, find_packages

setup(
  name='appyter',
  python_requires='>=3.7.0',
  version=open('appyter/VERSION', 'r').read(),
  url='https://github.com/maayanLab/appyter/',
  author='Daniel J. B. Clarke',
  author_email='u8sand@gmail.com',
  long_description=open('README.md', 'r').read(),
  long_description_content_type='text/markdown; charset=UTF-8',
  license='CC-BY-NC-SA-4.0',
  classifiers=[
    "Development Status :: 4 - Beta",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3",
    "Topic :: Scientific/Engineering",
    "Topic :: Software Development :: Libraries :: Application Frameworks",
    "Framework :: Jupyter",
  ],
  install_requires=list(map(str.strip, open('requirements.txt', 'r').readlines())),
  extras_require={
    'appyter_init': 'cookiecutter',
    'production': list(map(str.strip, open('requirements.production.txt', 'r').readlines())),
  },
  packages=find_packages(exclude=('example',)),
  include_package_data=True,
  entry_points={
    'console_scripts': ['appyter=appyter.__main__:main'],
  }
)
