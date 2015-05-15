# -*- coding: utf-8 -*-
"""
    maxminion.minion
    ~~~~~~~~~~~~~~~~

    A stupid, yellow assistant for testing MaxCompiler.

    It doesn't talk nonsense though.

    :copyright: (c) 2015 Maxeler Technologies
    :license: No license at the moment.
"""

_doc_ = """
Maxeler Test Minion.

Usage:
  maxminion <instructions_file> <scratch_directory>
  maxminion -h | --help
  maxminion --version

Options:
  -h --help    Show this screen.
  --version    Show version.
"""

import os

from docopt import docopt
from utils import mkcd, load_inst, get_login
from utils import fetch_code, build_code, uprint
from utils import CodeFetchError, CodeBuildError


VERSION = '0.0.1'


def run_app_test(app_name, app, login):
    """Runs tests for given app."""
    uprint('Testing %s... ' % app_name)
    with mkcd(app_name):
        try:
            fetch_code(app['FETCH'], login)
            build_code(app['BUILD'])
            print('OK')
        except CodeFetchError as e:
            print(e)
        except CodeBuildError as e:
            print(e)


def run_tests(apps, scratch, login):
    """Kinda main. Runs the whole thing."""
    with mkcd(scratch):
        # TODO: multiprocessing?
        for app_name in apps:
            app = apps[app_name]
            run_app_test(app_name, app, login)


if __name__ == '__main__':
    args = docopt(_doc_, version=VERSION)
    print('$MAXCOMPILERDIR=' + os.environ['MAXCOMPILERDIR'])
    print('$MAXELEROSDIR=' + os.environ['MAXELEROSDIR'])
    ins = load_inst(args['<instructions_file>'])
    scratch = os.path.abspath(args['<scratch_directory>'])
    run_tests(ins['APPS'], scratch, get_login())

