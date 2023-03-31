from setuptools import setup

setup(
    name='nsidc_projections',
    version='0.1.0',
    author='Andrew P. Barrett',
    author_email='andrew.barrett@colorado.edu',
    packages=["nsidc_projections"],
    install_requires=[
        'pytest',
        ],
    license='license',
    description='A package containing projection and grid definitions used in NSIDC data',
    long_description=open('README.md').read(),
)
