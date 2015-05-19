from setuptools import setup, Command

setup(
    name = 'wikidata_suggest',
    version = '0.0.2',
    url = 'http://github.com/edsu/wikidata_suggest',
    author = 'Ed Summers',
    author_email = 'ehs@pobox.com',
    py_modules = ['wikidata_suggest'],
    install_requires = ['requests', 'colorama'],
    scripts = ['scripts/wd'],
    description = 'Interactively look up Wikidata entities from the command line',
    license='MIT License'
)
