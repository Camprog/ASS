from setuptools import setup

with open("README", 'r') as f:
    long_description = f.read()

setup(
    name='ScrapJasssGithub',
    version='1.0',
    description='A useful module',
    license="GNU GPLv3",
    long_description=long_description,
    author='Kevin Chapuis',
    author_email='kevin.chapuis@gmail.com',
    url="http://github.com/chapuisk/scrapjasss",
    packages=['ScrapJasssGithub'],
    install_requires=['itertools', 'beautifulsoup4', 'requests'], #external packages as dependencies
    scripts=[
        'sample/.'
    ]
)