# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open

def readme():
    with open('README.rst') as f:
        return f.read()
# Get the long description from the relevant file


setup(
    name='finist',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='0.1.2',

    description='Redis based Finite State Machine.',
    long_description=readme(),
    # The project's main homepage.
    url='https://github.com/sumanau7/finist',

    # Author details
    author='Sumanau Sareen',
    author_email='finist-python@googlegroups.com',

    # Choose your license
    license='APACHE',

    # What does your project relate to?
    keywords='redis state machine python',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=['finist'],

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=['redis'],
    # include_package_data=True,
    # zip_safe=False
)

