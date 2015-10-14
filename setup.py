# -*- coding: utf-8 -*-
#歧視無邊，回頭是岸。鍵起鍵落，情真情幻。
import os
from setuptools import find_packages, setup
import codecs

## From ggplot setup.py
def extract_version():
    """
    Extracts version values from the main matplotlib __init__.py and
    returns them as a dictionary.
    """
    withcodecs.open('pyCountrySize/__init__.py', "r", "utf-8") as fd:
        for line in fd.readlines():
            if (line.startswith('__version__')):
                exec(line.strip())
    return locals()["__version__"]

def get_package_data():
    baseline_images = [
        'pyCountrySize/%s/*' % x
        for x in os.listdir('pyCountrySize')]

    return {
        'pyCountrySize':
        baseline_images +
        [
            "sizedb/*.py",
            "sizedb/*.pkl", 
            "datapkl/*.pkl", 
            "sizepkl/*.pkl"
        ]} 


setup(
    name="pyCountrySize",
    packages = ['pyCountrySize'],
    version=extract_version(),
    author="Hanteng Liao",
    author_email="hanteng@gmail.com",
    url="https://github.com/hanteng/pyCountrySize/",
    download_url = 'https://github.com/hanteng/pyCountrySize/zipball/master',
    license="GPLv3",
    package_dir={"pyCountrySize": "pyCountrySize"},
    package_data=get_package_data(),
    description="pyCountrySize for python",
    # run pandoc --from=markdown --to=rst --output=README.rst README.md
    long_description=open("README.rst").read(),
    # numpy is here to make installing easier... Needs to be at the last position,
    # as that's the first installed with "python setup.py install"
    install_requires=["pandas", "numpy"],
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
