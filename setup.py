from setuptools import setup


setup(
    name='AIOTumblr-core',
    version='0.1',
    description='Tumblr API client on top of aiohttp and oauthlib',
    author='Lena',
    author_email='arlena@hubsec.eu',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.7'
    ],
    packages=['aiotumblr_core'],
    install_requires=['aiohttp', 'oauthlib', 'python-forge'],
)
