text = ".__ .__ .__ .__ ___ _______ | | | |__ _____ | | | | _____ \ \/ /\__ \ | | | | \\\__ \ | | | | \__ \ \ / / __ \| |_| Y \/ __ \| |_| |__/ __ \_ \_/ (____ /____/___| (____ /____/____(____ / \/ \/ \/ \\"
next = True
limit = len(text)
while next:
    printed = []
    temp = ''
    for t in range(len(text)):
        temp += text[t]
        if len(temp) >= limit or t >= (len(text)-1):
            printed.append(temp)
            temp = ''
    for p in printed:
        print(p)
    if limit == 1:
        break
    is_next = input("is want to next? : ")
    if is_next in ['y','Y','yes','ok','1']:
        num = input("skipped num : ")
        if(num not in ['no', 'n', 'N','0','nope','', ' ']):
            limit -= int(num)
        else:
            limit -= 1
    elif is_next in ['',' ']:
        limit -= 1
    else:
        break

print('nothing')