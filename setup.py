# -*- coding: utf-8 -*-
#歧視無邊，回頭是岸。鍵起鍵落，情真情幻。
import os
from setuptools import find_packages, setup

setup(
    name="pyCountrySize",
    author="Hanteng Liao",
    author_email="hanteng@gmail.com",
    url="https://github.com/hanteng/pyCountrySize/",
    license="GPLv3",
    package_dir={"pyCountrySize": "pyCountrySize"},
    description="pyCountrySize for python",
    # run pandoc --from=markdown --to=rst --output=README.rst README.md
    long_description=open("README.rst").read(),
    # numpy is here to make installing easier... Needs to be at the last position,
    # as that's the first installed with "python setup.py install"
    install_requires=["pandas", ""],
    classifiers=['Intended Audience :: Science/Research',
                 'Intended Audience :: Developers',
                 'Programming Language :: Python',
                 'Topic :: Software Development',
                 'Topic :: Scientific/Engineering',
                 'Operating System :: Microsoft :: Windows',
                 'Operating System :: POSIX',
                 'Operating System :: Unix',
                 'Operating System :: MacOS',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.3'],
    zip_safe=False)
