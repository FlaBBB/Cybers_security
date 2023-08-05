import requests

req = requests.get("http://challenge01.root-me.org/programmation/ch1/")
cookies = req.cookies.get_dict()
while True:
    u = int(req.content.decode().split("U<sub>0</sub> = ")[1].split("<br />")[0])
    num1 = int(req.content.decode().split("U<sub>n+1</sub> = [ ")[1].split(" + ")[0])
    num2 = int(req.content.decode().split("[ n * ")[1].split(" ]<br />")[0])
    num3 = int(req.content.decode().split("You must find U<sub>")[1].split("</sub><br /><br />")[0])
    print(f"Un-1 = [{num1} + Un] + [n * {num2}]")
    print(f"U0 = {u}")
    print(f"target = U{num3}")
    for i in range(num3):
        u = (num1+u)+(i*num2)
    
    print(f"Test: {u}")
    req = requests.get(f"http://challenge01.root-me.org/programmation/ch1/ep1_v.php?result={u}", cookies=cookies)
    if "flag" in req.content.decode():
        print(req.content.decode().rstrip())
        break
    else:
        print(f"[FAILED] {req.content.decode().rstrip().replace('<br />',' - ')}")
    req = requests.get("http://challenge01.root-me.org/programmation/ch1/", cookies=cookies)