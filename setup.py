from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

INSTALL_REQUIRES = [
    "aiohttp",
    "twine"
]

setup(
    name='aiocryptocurrency',
    version='0.1.2',
    author='Sander',
    author_email='sander@sanderf.nl',
    python_requires='>=3.6',
    packages=['aiocryptocurrency'],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=INSTALL_REQUIRES,
    url='https://github.com/sanderfoobar/aiocryptocurrency',
    description='Abstraction library for managing funds for various cryptocurrencies via their RPCs',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: BSD License",
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    keywords='cryptocurrency'
)
