from distutils.core import setup

setup(
    name='secdetect',
    version='0.1.0',
    author='Ryan Lane',
    author_email='r.i.lane@tudelft.nl',
    packages=['secdetect'],
    scripts=[],
    url='https://github.com/lanery/secdetect',
    license='LICENSE.txt',
    description='Detecting tissue sections on ITO-coated glass',
    long_description=open('./README.md').read(),
    install_requires=[
        "numpy >= 1.14",
        "scikit-image >= 0.14.2",
    ],
)
