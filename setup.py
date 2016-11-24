import os
from io import open
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst'), encoding='utf-8') as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name = 'django-wechat-base',
    version = '1.1.4',
    packages = ['wechat'],
    include_package_data = True,
    install_requires = ['future','xmltodict>=0.9.2'],
    license = 'BSD License',
    description = 'fixed api error',
    long_description = README,
    url = 'https://github.com/ChanMo/django-wechat-base/',
    author = 'ChanMo',
    author_email = 'chen.orange@aliyun.com',
    classifiers = [
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License', # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        # Replace these appropriately if you are stuck on Python 2.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
