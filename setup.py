import setuptools

with open("README.rst") as f:
    readme = f.read()

setuptools.setup(
    name="micromagneticmodel",
    version="0.5.6",
    description="A Python-based micromagnetic model.",
    long_description=readme,
    url="https://joommf.github.io",
    author="Marijan Beg, Ryan A. Pepper, and Hans Fangohr",
    author_email="jupyteroommf@gmail.com",
    packages=setuptools.find_packages(),
    install_requires=["discretisedfield"],
    classifiers=["Development Status :: 3 - Alpha",
                 "License :: OSI Approved :: BSD License",
                 "Topic :: Scientific/Engineering :: Physics",
                 "Intended Audience :: Science/Research",
                 "Programming Language :: Python :: 3 :: Only"]
)
