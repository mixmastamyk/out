#!/usr/bin/env python3
import sys
from os.path import dirname, join
from setuptools import setup


# additional metadata, requirements
keywords = 'log logging events levels color terminal console standard out err '
install_requires = ['console',]
tests_require = ('pyflakes', 'readme_renderer'),
extras_require = dict(
    highlight=('pygments',),
)


def slurp(filename):
    try:
        with open(join(dirname(__file__), filename), encoding='utf8') as infile:
            return infile.read()
    except FileNotFoundError:
        pass  # needed at upload time, not install time


if sys.version_info.major < 3:
    raise NotImplementedError('Sorry, only Python 3 and above is supported.')


setup(
    name                = 'out',
    description         = 'Simple, fun take on logging for non-huge projects.'
                          ' Gets "outta" the way.',
    author_email        = 'mixmastamyk@github.com',
    author              = 'Mike Miller',
    keywords            = keywords,
    license             = 'LGPL 3',
    long_description    = slurp('readme.rst'),
    packages            = ('out',),
    url                 = 'https://github.com/mixmastamyk/out',
    version             = '0.57',

    extras_require      = extras_require,
    install_requires    = install_requires,
    python_requires     = '>=3.2',
    setup_requires      = install_requires,
    tests_require       = tests_require,

    classifiers         = [
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries',
    ],
)
