from setuptools import setup, find_packages

DISTNAME = 'secdetect'
DESCRIPTION = 'secdetect: detecting tissue sections on ITO-coated glass'
MAINTAINER = 'Ryan Lane'
MAINTAINER_EMAIL = 'r.i.lane@tudelft.nl'
LICENSE = 'LICENSE.txt'
URL = 'https://github.com/lanery/secdetect'
VERSION = '0.1.dev'
PACKAGES = [
    'secdetect',
    'secdetect.data',
]
INSTALL_REQUIRES = [
    'numpy',
    'scipy',
    'scikit-image',
]

if __name__ == '__main__':

    setup(
        name=DISTNAME,
        version=VERSION,
        author=MAINTAINER,
        author_email=MAINTAINER_EMAIL,
        packages=PACKAGES,
        include_package_data=True,
        url=URL,
        license=LICENSE,
        description=DESCRIPTION,
        long_description=open('README.md').read(),
        install_requires=INSTALL_REQUIRES,
    )
