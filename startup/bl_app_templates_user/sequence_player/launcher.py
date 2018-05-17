#!/usr/bin/env python

import sys
import subprocess
import os

current_dir = os.path.dirname(__file__)
current_dir = os.path.normpath(current_dir)

sys.path.append(current_dir)

from argconfig import getargs
args = getargs()

blender = 'blender'
command = [blender]

script_path = os.path.join(
    current_dir,
    'setapp.py')

command.extend(['--python', script_path, '--'])
command.extend(sys.argv[1:])  # pass the same arguments to Blender

# set ACES config.ocio with EXR files
if args.path:
    path = args.path
    if path.lower().endswith('.exr'):
        args.ocio = os.getenv('ACES')

if args.ocio:
    env = os.environ.copy()
    env['OCIO'] = args.ocio
    subprocess.call(command, env=env)
else:
    subprocess.call(command)
