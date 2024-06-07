from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.2'
DESCRIPTION = "DocsGen is a Python library that generates docs for python libs."

LONG_DESCRIPTION = """
DocsGen is a Python library that generates docs for python libs.

Lib Features:
- Generate Docs in markdown.
- Simple to use.
- Automatic docs generator.
- Support making example for use.

For more information, please visit the [GitHub repository](https://github.com/IceBytes/DocsGen).
"""


setup(
    name="docsgen",
    version=VERSION,
    author="Just Ice",
    author_email="MrAws.developer@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['docstring-parser'],
    keywords=["Auto docs", "Generate docs"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    url='https://github.com/IceBytes/DocsGen/',
    project_urls={
        'Source': 'https://github.com/IceBytes/DocsGen/',
        'Bug Reports': 'https://github.com/IceBytes/DocsGen/issues',
        'Documentation': 'https://github.com/IceBytes/DocsGen/'
    },
    entry_points={
        'console_scripts': [
            'docsgen = docsgen.cli:main'
        ]
    }
)