import setuptools

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name='micromagneticmodel',
    version='0.11',
    description=('Python-based domain-specific language for '
                 'computational magnetism'),
    author='Marijan Beg, Martin Lang, and Hans Fangohr',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://ubermag.github.io',
    packages=setuptools.find_packages(),
    include_package_data=True,
    python_requires='>=3.8',
    install_requires=['discretisedfield==0.11'],
    classifiers=['Development Status :: 5 - Production/Stable',
                 'Intended Audience :: Education',
                 'Intended Audience :: Developers',
                 'Intended Audience :: Science/Research',
                 'License :: OSI Approved :: BSD License',
                 'Natural Language :: English',
                 'Operating System :: MacOS',
                 'Operating System :: Microsoft :: Windows',
                 'Operating System :: Unix',
                 'Programming Language :: Python :: 3 :: Only',
                 'Topic :: Scientific/Engineering :: Physics',
                 'Topic :: Scientific/Engineering :: Mathematics',
                 'Topic :: Scientific/Engineering :: Visualization']
)
