import setuptools
from distutils.core import setup

from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='telegram-handler',
      version='1.4.1',
      description='async telegram handler',
      author='Guyshe',
      url='https://github.com/guyshe/telegram_handler',
      long_description=long_description,
      long_description_content_type='text/markdown',
      packages=setuptools.find_packages(),
      install_requires=['requests~=2.27.0', 'retry~=0.9.0'])
