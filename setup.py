import sys

import codecs
import os.path

PACKAGE_NAME = "typingstat"

def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

rel_path = PACKAGE_NAME + "/__init__.py"

def _get(query):
    for line in read(rel_path).splitlines():
        if line.startswith(query):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name=PACKAGE_NAME,
    version=_get("__version__"),
    description="A customizable command line touch typing tutor",
    long_description=open("README.md").read().strip(),
    long_description_content_type="text/markdown",
    author=_get("__author__"),
    author_email=_get("__email__"),
    url="http://github.com/Irreq/typingstat",
    python_requires=">=3.4",
    classifiers=[
        "Development Status :: %s" % _get("__status__"),
        "Environment :: Console",
        "Environment :: Daemon",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: %s License" % _get("__license__"),
        "Operating System :: Linux",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Utilities",
    ],
)
