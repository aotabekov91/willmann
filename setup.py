from setuptools import setup, find_packages

setup(name="willmann",
      version="0.0.1",
      description='Willmann',
      packages=find_packages(),
      include_package_data=True,
      entry_points = {
          'console_scripts': ['willmann = willmann.run:main']
          },
      )
