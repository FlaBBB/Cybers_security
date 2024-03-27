import os

print('Welcome to my best collections archive')
res = input('What is the secret: ')
secret_val = "k0D3NuKlIr2024"
if secret_val == res:
    print('How can you still find my collections!!!!')
    os.system('cat flag.txt')
    print()
else:
    print('Try harder xD!')