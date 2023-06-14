from setuptools import setup, find_packages

setup(name="willmann",
      version="1.0.0",
      description='Willmann',
      packages=find_packages(),
      include_package_data=True,
      package_data={
          '':['*.*']
          },
      entry_points = {
          'console_scripts': [
              'willmann = willmann.run:main',
              ], 
          },
      )
