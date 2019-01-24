from setuptools import setup
import importlib


cmdclass = None

try:
    import jinja2  # Available when installed in dev mode
except ImportError:
    pass
else:
    cmdclass = {
        'generate_docs': getattr(importlib.import_module('aiotumblr.utils.docgen'), 'DocGenCommand')
    }


setup(
    name='AIOTumblr',
    version='0.1',
    description='Tumblr API client on top of aiohttp and oauthlib',
    author='Lena',
    author_email='arlena@hubsec.eu',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.7'
    ],
    packages=['aiotumblr'],
    install_requires=['aiohttp', 'oauthlib', 'python-forge'],
    cmdclass=cmdclass
)
