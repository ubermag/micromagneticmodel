from setuptools import setup

with open('README.rst') as f:
    readme = f.read()

setup(
    name='micromagneticmodel',
    version='0.1',
    description='A Python-based micromagnetic model.',
    long_description=readme,
    author='Computational Modelling Group',
    author_email='fangohr@soton.ac.uk',
    url = 'https://github.com/joommf/micromagneticmodel',
    download_url = 'https://github.com/joommf/micromagneticmodel/tarball/0.1',
    packages=['micromagneticmodel',
              'micromagneticmodel.energies',
              'micromagneticmodel.dynamics'],
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ]
)
