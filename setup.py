import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "f5_cli",
    version = "0.0.3",
    author = "Victor Daskalov",
    author_email = "victor.daskalov@itgix.com",
    entry_points={
        'console_scripts': [ 'f5_cli = f5_modules.f5_cli:main'
        ]
    },
    install_requires = [ "f5-sdk" ],
    description = ("A command line tool that makes it easy to control F5 nodes"),
    packages=['f5_modules'],
    long_description=read('README'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
