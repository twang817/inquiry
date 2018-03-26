import os

from setuptools import setup, find_packages


install_requires = [
    'prompt-toolkit',
]

base_dir = os.path.dirname(__file__)

setup(
    name='inquiry',
    use_scm_version=True,
    description='Faithful clone of Inquirer.js',
    long_description=open(os.path.join(base_dir, 'README.md')).read(),
    author='Tommy Wang',
    author_email='twang@august8.net',
    url='https://github.com/twang817/inquiry',

    packages=find_packages('src'),
    package_dir={'': 'src'},

    setup_requires=['setuptools_scm'],
    install_requires=install_requires,
)
