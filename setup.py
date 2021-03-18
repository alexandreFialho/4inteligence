import setuptools

from api import __version__ as VERSION

setuptools.setup(
    name='fast-api-sample-crud',
    version=VERSION,
    description='WebApi sample',
    author='Alexandre Fialho de Araujo',
    author_email='alexandrefialhobr@gmail.com',
    url='',
    packages=setuptools.find_packages(),
    package_dir={"app": "app"}
)
