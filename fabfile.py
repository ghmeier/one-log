from __future__ import absolute_import

import os
import sys

from fabric.api import local, task
from fabric.colors import green, red
from fabric.context_managers import settings

ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))


@task
def clean():
    """Remove all .pyc files."""
    print green('Clean up .pyc files')
    local("find . -name '*.py[co]' -exec rm -f '{}' ';'")


@task
def lint():
    """Check for lints"""
    print green('Checking for lints')
    local("flake8 `find . -name '*.py' -not -path '*env/*'` --ignore=E501,E702,E712 "
          "--exclude='./docs/*,./scripts/*,./client/*,./verifier/thrift/*,./alembic/versions/*'")


@task
def bootstrap():
    """Bootstrap the environment."""
    local("mkdir -p logs")
    print green("\nInstalling requirements")
    local("pip install -r requirements.txt")


@task
def test(args='', environment='test'):
    """Run tests."""
    clean()
    lint()
    print green('Running all tests')

    cmd = ('py.test --cov=onelog/onelog.py --tb=native onelog/tests/main.py')

    with settings(warn_only=True, quiet=True):
        success = local(cmd).succeeded

    if success:
        print(green("Tests finished running with success."))
    else:
        print(red("Test finished running with errors."))
        sys.exit(1)
