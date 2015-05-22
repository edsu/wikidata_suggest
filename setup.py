from setuptools import setup, Command

class PyTest(Command):
    """
    A command to convince setuptools to run pytests.
    """
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        import pytest
        pytest.main("test.py")

setup(
    name = 'wikidata_suggest',
    version = '0.0.5',
    url = 'http://github.com/edsu/wikidata_suggest',
    author = 'Ed Summers',
    author_email = 'ehs@pobox.com',
    py_modules = ['wikidata_suggest'],
    install_requires = ['requests', 'colorama'],
    tests_require=['pytest'],
    scripts = ['scripts/wd'],
    cmdclass = {'test': PyTest},
    description = 'Interactively look up Wikidata entities from the command line',
    license='MIT License'
)
