import os
import sys
import json
import shutil
import string
import getpass
import subprocess


class mkcd:
    """Context manager for creating a new directory and
    cd to it."""

    def __init__(self, dir):
        self.dir = os.path.expanduser(dir)

    def __enter__(self):
        if not os.path.exists(self.dir):
            os.mkdir(self.dir)
        self.pwd = os.getcwd()
        os.chdir(self.dir)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.pwd)
        shutil.rmtree(self.dir)


class CodeFetchError(Exception):
    pass


class CodeBuildError(Exception):
    pass


def load_inst(inst_file='./inst.json'):
    """Loads given instructions file."""
    with open(inst_file, 'r') as f:
        return json.loads(f.read())


def get_login():
    """Get user's login and password."""
    login = {'username': None, 'password': None}
    uprint('Enter username for Git/SVN:')
    login['username'] = raw_input()
    pwd_prompt = 'Enter password for Git/SVN (no echo): '
    login['password'] = getpass.getpass(pwd_prompt)
    return login


def process(cmd, out):
    """Executes the given shell command. Puts the output to the
    given stream."""
    with open(out, 'w+') as outf:
        subprocess.check_call(cmd,
                             shell=True, 
                             stdout=outf,
                             stderr=outf)

def fetch_code(cmd, login):
    """Fetches the code using given cmd."""
    out = 'fetch.log'
    tpl = string.Template(cmd)
    cmd = tpl.safe_substitute(cmd, **login)
    try:
        process(cmd, out)
    except subprocess.CalledProcessError as e:
        raise CodeFetchException('ERROR! Fetch Failed [See %s].' % out)


def build_code(cmd):
    """Builds the code using given cmd."""
    out = 'build.log'
    try:
        process(cmd, out)
    except subprocess.CalledProcessError as e:
        raise CodeFetchException('ERROR! Build failed [See %s].' % out)

def uprint(s):
    """Print sans newline."""
    print(s),
    sys.stdout.flush()
