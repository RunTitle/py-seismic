from setuptools import setup, find_packages

setup(
    name="Seismic",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'structlog>=15.3.0',
        'iso8601>=0.1.11',
        'future>=0.15.2'
    ],
    test_suite='seismic.tests',
    # metadata for upload to PyPI
    author="A.T. Fouty",
    author_email="afouty@runtitle.com",
    description="Structlog implementation library for python",
    license="PSF",
    keywords="Python logging structlog",
    url="https://github.com/RunTile/py-seismic/",   
)