from setuptools import setup
import opa_git_sync

setup(
    name='opa-git-sync',
    version=opa_git_sync.__version__,
    url='https://github.com/tsandall/opa-git-sync',
    packages=[
        'opa_git_sync',
    ],
    scripts=[
        'scripts/opa-git-sync',
    ],
)
