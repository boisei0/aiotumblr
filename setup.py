from setuptools import setup, find_packages
import importlib


cmdclass = {}

try:
    import jinja2
except ImportError:
    pass
else:
    cmdclass = {
        'generate_docs': getattr(importlib.import_module('aiotumblr.utils.docgen'), 'DocGenCommand')
    }


setup(
    name='AIOTumblr',
    version='0.2',
    description='Tumblr API client on top of aiohttp and oauthlib',
    author='Lena',
    author_email='arlena@hubsec.eu',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.7'
    ],
    # packages=['aiotumblr'],
    packages=find_packages(),
    install_requires=['aiohttp', 'oauthlib', 'python-forge', 'aiotumblr_public>=0.1.1'],
    extras_requires={
        'docs': ['sphinx', 'jinja2'],
    },
    setup_requires=['jinja2'],
    python_requires='>=3.7',
    cmdclass=cmdclass,
)
