import setuptools

from api import __version__ as VERSION

setuptools.setup(
    name='4Inteligence_webapi',
    version=VERSION,
    description='WebApi for test pratic',
    author='Alexandre Fialho de Araujo',
    author_email='alexandrefialhobr@gmail.com',
    url='',
    packages=setuptools.find_packages(),
    package_dir={"app": "app"}
)
