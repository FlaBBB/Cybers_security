# patched-shell

**Category** : Pwn
**Points** : 382

Okay, okay. So you were smart enough to do basic overflow huh...

Now try this challenge!
I patched the shell function so it calls system instead of execve...
so now your exploit shouldn't work! bwahahahahaha

Note: due to the copycat nature of this challenge, it suffers from the same bug that was in basic-overflow. see the cryptic message there for more information.

Author: drec


nc 34.134.173.142 5000

## Files : 
 - [patched-shell](./patched-shell)


