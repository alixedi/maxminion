import sys
import json
import string
import subprocess
import utils
import os

# Parse the CLI
if len(sys.argv) < 3:
    print 'Usage: minion.py <username> <password>'
    sys.exit(1)

args = {
    'username': sys.argv[1],
    'password': sys.argv[2]
}

# Read the config
cfgf = open('./apps.json')
cfg = json.loads(cfgf.read())

# make tmp directory
utils.mkdir('./tmp')

# Set up the output streams
FNULL = open(os.devnull, 'w')

with utils.cd('./tmp'):
    for app in cfg['APPS']:
        try:
            utils.uprint('Testing %s: ' % app)
            tpl = string.Template(cfg['APPS'][app]['Fetch'])
            fetch = tpl.safe_substitute(args)
            test = cfg['APPS'][app]['Test']
            subprocess.check_call(fetch, shell=True, stdout=FNULL, stderr=FNULL)
            subprocess.check_call(test, shell=True, stdout=FNULL)
            utils.uprint('OK')
        except:
            utils.uprint('ERROR')
            continue

# delete the tmp dir
utils.rmdir('./tmp')
