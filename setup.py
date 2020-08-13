from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='100_millions_requests',
    version='0.1.0',
    url='https://github.com/rcv911/100_millions_requests.git',
    install_requires=[
        'aiohttp',
        'pytoml',
    ],
    include_package_data=True,
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    license='Free',
    author='chub',
    author_email='r.chub90@yandex.ru',
    description='',
)
