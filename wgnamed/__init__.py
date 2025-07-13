#!/usr/bin/env python3
import os
import json

punctuation = '!"#$%&\'()*+,/:;<=>?@[\\]^`{|}~'

def is_base64(s):
    try:
        return base64.b64encode(base64.b64decode(s)) == s
    except Exception:
        return False

def normal_json_item(v):
  k, v = v

  return not is_base64(k) \
    and "name" in v \
    and all(not c in punctuation for c in v["name"])

def santitize_input(update):
  reconstruction = dict()
  for k, v in filter(normal_json_item, update.items() or []):
    reconstruction[k] = v
  return reconstruction


def read_names(nameString):
  '''
    [PATH:..];PATH
    path:///file.json => { "<Base64-Public-Key>": { "name": "machine-name" } }
    https://domain/place
  '''
  seen = set()
  peers = dict()

  for resource in nameString.strip(";").split(";"):
    if resource.startswith("path://"):
      resource = resource[7:]

      if not os.path.exists(resource):
        continue

      try:
        with open(resource, "r") as fd:
          peers.update(
            santitize_input(json.load(fd))
          )
      except Exception as e:
        print(f"{resource}: {e}")

    elif resource.startswith("https://") or resource.startswith("http://"):
      try:
        import requests
        peers.update(
          santitize_input(requests.get(resource).json())
        )
      except Exception as e:
        print(f"{resource}:{e}")
    else:
      print(f"unrecgonized resource: {resource}")

  return peers

def get_peers():
  return read_names(os.environ.get("WG_NAME", "path:///etc/wireguard/name.json"))
