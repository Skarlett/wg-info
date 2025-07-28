#!/usr/bin/env python3
import sys
from __init__ import get_peers


def main():
    peerNames = { f"{v['name']}": k for k, v in get_peers.items() }

    if len(sys.argv) == 1:
        print(f"{sys.argv[0]} <pubkey/name>")

    for x in sys.argv[1:]:
        if x in peers:
            print(f"{x}   ||   {peers[x]['name']}")
        else:
            if x in peerNames:
            print(f"{x} {peerNames[x]}")
            else:
            print(f"{x} -> ??")
