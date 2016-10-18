from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

setup(
    name='micromagneticmodel',
    version='0.5.4.3',
    description='A Python-based micromagnetic model.',
    long_description=readme,
    url='https://github.com/joommf/micromagneticmodel',
    author='Computational Modelling Group',
    author_email='fangohr@soton.ac.uk',
    download_url='https://github.com/joommf/micromagneticmodel/tarball/0.5.4.3',
    packages=find_packages(),
    install_requires=['discretisedfield'],
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: OSI Approved :: BSD License',
                 'Topic :: Scientific/Engineering :: Physics',
                 'Intended Audience :: Science/Research',
                 'Programming Language :: Python :: 3 :: Only']
)
