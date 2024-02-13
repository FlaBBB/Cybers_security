# pwn02

**Category** : PWNABLE
**Points** : 1000

**Chall name:**
* CoolPool

   
**Category:**
* Pwn

**Author:**
* linhlhq

**Description:**
#### Goal
- Spawn cmd with SYSTEM
- Read the flag in `C:\flag.txt` (readable only by SYSTEM)
#### Environment
- Windows 10 Pro 22h2
    - OS Build 19041.vb_release.191206-1406
- Load coolpool.sys (sha1: F8B1238982E60E64DA444F39368E45B81626C100)
- Account 
    - ctf/tetctf2024
    - admin/tetctf2024
- ntoskrnl.exe (sha1: 39D3060EF96BB18544C452EAD5ECF8DCB8C2D139)
#### Test
You can use follow command and use vnc for testing :
~~~
qemu-system-x86_64 -enable-kvm -m 4096 -smp cores=4 -hda windows.qcow2 -cpu host,+smep,+smap,+pcid -device e1000,netdev=user.0 -netdev user,id=user.0,hostfwd=tcp::9696-:9696 -monitor stdio
~~~

The VM just for your final test. You also can use your VM to test it. But you need makesure the build version is same as 19041.vb_release.191206-1406
#### Remote Service
- Our service will be hosted at `123.24.204.45:1337`, you need to use the team token to log in to the service.
- Each team will have 3 accesses to the VM:
    - Please make sure your exploit is work in local in the environment we provide first.
    - You can only use the VM in 10 minutes at a time.
    - If it's BSOD, we won't restart it.

#### Enviroment
We will run qemu with follow command:
~~~
qemu-system-x86_64 -hda windows.qcow2 -m 4096 -smp cores=4 -enable-kvm -cpu host,+smep,+smap,+pcid -nographic -monitor /dev/null -loadvm ctf_snapshot -device e1000,netdev=user.0 -netdev user,id=user.0,hostfwd=tcp::{port}-:{port}
~~~
- The snapshot just login `ctf` account and run `C:\ctf\start.cmd`.
- It will run `C:\ctf\cmd.exe` as Low integrity
- When you connect to the service and select `Access VM`, we will automatically connect to the VM to spawn cmd for you to use.
- You can use `curl` to download your binary in `%TEMP%\Low` or `c:\ctf\tmp`.
- Please running in ubuntu 22.04

**Material:**
* [Driver](https://drive.google.com/file/d/13JPhvk8CNUWStdzI3Qf1c5gvGcbFh4bc/view?usp=sharing)
* [VM](https://drive.google.com/file/d/1D_PhUvkDeGL2gYZlHa73qnIwGwXU21F1/view?usp=sharing)

Password for unzip: tetctf2024

nc 123.24.204.45 1337



