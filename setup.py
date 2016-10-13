from setuptools import setup

with open('README.rst') as f:
    readme = f.read()

setup(
    name="micromagneticmodel",
    version="0.5.4.2",
    description="A Python-based micromagnetic model.",
    long_description=readme,
    author="Computational Modelling Group",
    author_email="fangohr@soton.ac.uk",
    url="https://github.com/joommf/micromagneticmodel",
    download_url="https://github.com/joommf/micromagneticmodel/tarball/0.5.4.2",
    packages=["micromagneticmodel",
              "micromagneticmodel.util",
              "micromagneticmodel.hamiltonian",
              "micromagneticmodel.dynamics",
              "micromagneticmodel.drivers",
              "micromagneticmodel.tests"],
    install_requires=["discretisedfield"],
    classifiers=["License :: OSI Approved :: BSD License",
                 "Programming Language :: Python :: 3"]
)
