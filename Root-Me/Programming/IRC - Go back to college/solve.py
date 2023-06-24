import socket
import sys
import math

server = "irc.hackerzvoice.net"
server_port = 6667
channel = "#root-me_challenge"
nickname = "w0lf"
botname = "Candy"
irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
def join_chan(channel):
    irc.send(f"JOIN {channel}\n".encode())
    ircmsg = ""
    while ircmsg.find("End of /NAMES list.") == -1:
        ircmsg = irc.recv(2048).decode("UTF-8")
        ircmsg = ircmsg.strip('\n\r')
        print(ircmsg)
    return True
        
def join_serv(server):
    irc.connect((server, server_port))
    irc.send(f"USER {nickname} {nickname} {nickname} :just {nickname}\n".encode()) 
    irc.send(f"NICK {nickname}\n".encode())               
    ircmsg = ""
    while ircmsg.find(f"MODE {nickname}") == -1:
        ircmsg = irc.recv(2048).decode("UTF-8")
        ircmsg = ircmsg.strip('\n\r')
        print(ircmsg)
    return True
        
def send_msg(message, target=channel):
    irc.send(f"PRIVMSG {target} :{message}\n".encode())
        
def main():
    if not join_serv(server):
        print("Error joining server")
        sys.exit(1)
    if not join_chan(channel):
        print("Error joining channel")
        sys.exit(1)
    send_msg("!ep1", botname)
    while True:
        ircmsg = irc.recv(2048).decode("UTF-8")
        print(ircmsg)
        if ircmsg.find("password") != -1 :
            print(f"flag: {ircmsg.split('password ')[1]}")
            break
        if ircmsg.find("Bad reponse!") != -1:
            send_msg("!ep1", botname)
            continue
        if ircmsg.find("Stop flooding!") != -1:
            exit(1)
        number = ircmsg.split(":")[2].strip('\n\r').split(' / ')
        result = round(math.sqrt(int(number[0])) * int(number[1]), 2)
        msg = f"!ep1 -rep {result}"
        print(msg)
        send_msg(msg, botname)
    
main()
