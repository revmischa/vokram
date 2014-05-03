import os
from distutils.core import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='vokram',
    version='1.0.0',
    description='A toy Markov chain implementation.',
    long_description=read('README.rst'),
    url='https://github.com/mccutchen/vokram',
    license='MIT',
    author='Will McCutchen',
    author_email='will@mccutch.org',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=['vokram'],
    scripts=['bin/vokram'],
)
