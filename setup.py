# try:
#     from setuptools import setup
# except ImportError:
#     from distutils.core import setup

from setuptools import setup, find_packages

setup(
    name='osisoftpy',
    description='OSIsoft PI Web WebAPI client',
    version='1.2.0',
    url='https://gitlab.com/dstcontrols/pge-piclient-python',
    license='MIT',
    author='Andrew Pong <apong@dstcontrols.com>, Alan Kenyon <akenyon@dstcontrols.com>',
    install_requires=[
        'nose',
        'requests',
        'requests-kerberos',
        'rx', 'colorlog', 'six', 'arrow', 'pytest'
    ],
    # packages=['OSIsoftPy'],
    packages=find_packages(),
    scripts=[],
)
