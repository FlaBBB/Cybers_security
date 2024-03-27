This challenge should be run in a Windows 10 or 11 VM, with `Secure Boot` disabled.

You must enable `Test mode` in the VM (See what is `Test mode` here: https://learn.microsoft.com/en-us/windows-hardware/drivers/install/the-testsigning-boot-configuration-option)

To enable `Test mode`, run the following command in an administrator command prompt.
```
bcdedit.exe -set TESTSIGNING ON
```
After that, reboot your VM.

The binary must also be run in an administrator command prompt.