#!/usr/bin/env python
import argparse
import random
from aos.system.sdk.python.pa.loader import Loader
APP = 'lifx'

parser = argparse.ArgumentParser()
parser.add_argument('-f', '-feature', help='feature', required=True)
args = parser.parse_args()

if args.f == 'show':
  Loader.show(APP)
else:
  Loader.hide(APP)
