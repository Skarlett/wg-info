#!/usr/bin/env python3
import os
import sys
import re
import json
import base64
import subprocess
import threading
import argparse
import sys

from . import read_names, is_base64, normal_json_item, punctuation

OUTPUT = 'pipe'
REDFMT = ''
BLUEFMT = ''
REDBLDFMT = ''
GREENFMT = ''
GREENBLDFMT = ''
YELLOWFMT = ''
YELLOWBLDFMT = ''
BLDFMT = ''
ENDFMT = ''

punctuation = '!"#$%&\'()*+,/:;<=>?@[\\]^`{|}~'

ENCODING = os.environ.get("WG_ENCODING", "b64")
PROGRAM = os.environ.get("PROGRAM", "wg")

def setGlobals():
  global OUTPUT, REDFMT, BLUEFMT, REDBLDFMT, \
    GREENBLDFMT, YELLOWFMT, YELLOWBLDFMT, BLDFMT, ENDFMT, \
    ENCODING

  OUTPUT = os.environ.get("WG_OUTPUT", "pipe")
  if sys.stdout.isatty():
    OUTPUT = "tty";

  if not OUTPUT in ["tty", "pipe", "html"]:
    OUTPUT="tty"

  if not ENCODING in ["b32", "b64"]:
    print(f"bad value for WG_ENCODING ({ENCODING})")
    ENCODING="b64"

  if OUTPUT == "html":
    REDFMT = '<span style="color: red;">'
    BLUEFMT = '<span style="color: cyan;">'
    REDBLDFMT = '<span style="color: red; font-weight: bold;">'
    GREENFMT = '<span style="color: green;">'
    GREENBLDFMT = '<span style="color: green; font-weight: bold;">'
    YELLOWFMT = '<span style="color: orange;">'
    YELLOWBLDFMT = '<span style="color: orange; font-weight: bold;">'
    BLDFMT = '<span style="font-weight: bold;">'
    ENDFMT = '</span>'

  elif OUTPUT == "tty":
    REDFMT = '\033[0;31m'
    BLUEFMT = '\033[0;36m'
    REDBLDFMT = '\033[1;31m'
    GREENFMT = '\033[0;32m'
    GREENBLDFMT = '\033[1;32m'
    YELLOWFMT = '\033[0;33m'
    YELLOWBLDFMT = '\033[1;33m'
    BLDFMT = '\033[1m'
    ENDFMT = '\033[0m'

  else:
    ENCODING="b64"
    OUTPUT="tty"
    
  return 0

def show_pubkey(value, encoding=ENCODING):
  if encoding == "b32":
    return base64.b32encode(
      base64.b64decode(value)
    ).decode("utf8").lower()
  return value

def show_info(peers, interface="all"):
  peer_section = False
  try:
    call = subprocess.check_output([PROGRAM, 'show', interface]);
  except Exception as e:
    return

  for i, line in enumerate(call.decode('utf-8').split("\n")[:-1]):
    line = line.strip()

    if line.startswith('peer:'):
      peer_section = True
      peer_pubkey = line.split(':', 1)[1].strip()

      colorfmt = YELLOWFMT
      colorbldfmt = YELLOWBLDFMT

      if peer_pubkey in peers:
          print(colorbldfmt + 'peer' + ENDFMT + ': ' + colorfmt +
              peers[peer_pubkey]['name'] + ' ('+show_pubkey(peer_pubkey)+')' + ENDFMT)
      else:
        print(colorbldfmt + 'peer' + ENDFMT + ': ' + colorfmt + show_pubkey(peer_pubkey) + ENDFMT)

    elif line.startswith('interface:'):
      peer_section = False
      interface = line.split(':', 1)[1].strip()
      print(GREENBLDFMT + 'interface' + ENDFMT + ': ' + GREENFMT + interface + ENDFMT)

    elif line:
      key = line.split(':')[0].strip()
      value = line.split(':', 1)[1].strip()
      indent = '  ' if peer_section else '  '

      accent = re.sub(
        r"(?P<tag>seconds|minutes|hours|days|weeks|months|MiB|B|KiB|GiB|TiB|\/)",
        BLUEFMT + r"\g<tag>" + ENDFMT,
        value
      )

      if not key == "public key": # dont turn pubkeys blue
        print(indent + BLDFMT + key + ENDFMT + ': ' + accent)
      else:
        print(indent + BLDFMT + key + ENDFMT + ': ' + show_pubkey(value))

    else:
      print(line)
      # if sys.argv[-1] == "dump":
      #   if i == 0:

      #   print(" peers[peer_pubkey]['name']", end="")

def main():
  setGlobals()
  peers = read_names(
    os.environ.get("WG_NAME", "path:///etc/wireguard/name.json")
  )

  if OUTPUT == 'html':
    print('<pre>')

  if len(sys.argv) > 1:
    show_info(peers, sys.argv[1])
  else:
    show_info(peers, "all")

  if OUTPUT == 'html':
    print('</pre>')

if __name__ == '__main__':
  main()
