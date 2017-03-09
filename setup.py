from setuptools import setup
import opagitsync

setup(
    name='opa-git-sync',
    version=opagitsync.__version__,
    url='https://github.com/tsandall/opa-git-sync',
    packages=[
        'opagitsync',
    ],
    scripts=[
        'scripts/opa-git-sync',
    ],
)
