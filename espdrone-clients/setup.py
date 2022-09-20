#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess
from subprocess import PIPE, Popen
from setuptools import setup, find_packages
from glob import glob
import json
import codecs
import sys
import os

if sys.argv[1] == 'build':
    from cx_Freeze import setup, Executable  # noqa

    cxfreeze_options = {
        'options': {
            'build_exe': {'includes': ['numpy.core._methods',
                                       'numpy.lib.format',
                                       'pyqtgraph.debug',
                                       'pyqtgraph.ThreadsafeTimer',
                                       ],
                          'packages': ['asyncio'],
                          'excludes': ['tkinter']}
        },
        'executables': [Executable("bin/edclient", icon='bitcraze.ico')],
    }
else:
    cxfreeze_options = {}
# except:
#     pass

if sys.version_info < (3, 5):
    raise "must use python 3.5 or greater"


# Recover version from Git.
# Returns None if git is not installed or if we are running outside of the git
# tree
def get_version():
    try:
        process = Popen(["git", "describe", "--tags"], stdout=PIPE)
        (output, err) = process.communicate()
        process.wait()
    except OSError:
        return None

    if process.returncode != 0:
        return None

    version = output.strip().decode("UTF-8")

    if subprocess.call(["git", "diff-index", "--quiet", "HEAD"]) != 0:
        version += "_modified"

    return version


def relative(lst, base=''):
    return list(map(lambda x: base + os.path.basename(x), lst))


VERSION = "1.0.0"

if not VERSION and not os.path.isfile('src/edclient/version.json'):
    sys.stderr.write("Git is required to install from source.\n" +
                     "Please clone the project with Git or use one of the\n" +
                     "release pachages (either from pip or a binary build).\n")
    raise Exception("Git required.")

if not VERSION:
    versionfile = open('src/edclient/version.json', 'r', encoding='utf8')
    VERSION = json.loads(versionfile.read())['version']
else:
    with codecs.open('src/edclient/version.json', 'w', encoding='utf8') as f:
        f.write(json.dumps({'version': VERSION}))

platform_requires = []
platform_dev_requires = []
if sys.platform == 'win32' or sys.platform == 'darwin':
    platform_requires = ['pysdl2']
if sys.platform == 'win32':
    platform_dev_requires = ['cx_freeze', 'jinja2']

package_data = {
    'edclient.ui':  relative(glob('src/edclient/ui/*.ui')),
    'edclient.ui.tabs': relative(glob('src/edclient/ui/tabs/*.ui')),
    'edclient.ui.widgets':  relative(glob('src/edclient/ui/widgets/*.ui')),
    'edclient.ui.toolboxes':  relative(glob('src/edclient/ui/toolboxes/*.ui')),  # noqa
    'edclient.ui.dialogs':  relative(glob('src/edclient/ui/dialogs/*.ui')),
    'edclient':  relative(glob('src/edclient/configs/*.json'), 'configs/') +  # noqa
                 relative(glob('src/edclient/configs/input/*.json'), 'configs/input/') +  # noqa
                 relative(glob('src/edclient/configs/log/*.json'), 'configs/log/') +  # noqa
                 relative(glob('src/edclient/resources/*'), 'resources/') +
                 relative(glob('src/edclient/*.png')),
    '': ['README.md']
}
data_files = [
    ('third_party', glob('src/edclient/third_party/*')),
]

# Initial parameters
setup(
    name='edclient',
    description='Bitcraze Cazyflie quadcopter client',
    version=VERSION,
    author='Bitcraze team',
    author_email='contact@bitcraze.se',
    url='http://www.bitcraze.io',

    classifiers=[
        'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',  # noqa
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='quadcopter espdrone',

    package_dir={'': 'src'},
    packages=find_packages('src'),

    entry_points={
        'console_scripts': [
            'edclient=edclient.gui:main',
            'cfheadless=edclient.headless:main',
            'cfloader=cfloader:main',
            'cfzmq=cfzmq:main'
        ],
    },

    install_requires=platform_requires + ['appdirs>=1.4.0',
                                          'pyzmq',
                                          'pyqtgraph>=0.10',
                                          'PyYAML',
                                          'quamash==0.6.1',
                                          'qtm>=2.0.2',
                                          'PyQt5==5.13.2'],


    package_data=package_data,

    data_files=data_files,

    # cx_freeze options
    **cxfreeze_options
)
