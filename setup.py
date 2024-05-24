from setuptools import setup, find_packages

with open('requirements.txt') as file:
    required = file.read().splitlines()

setup(name='bd-api-task',
      version='0.1',
      packages=find_packages(where='src'),
      package_dir={'':'src'},
      install_requires=required
)