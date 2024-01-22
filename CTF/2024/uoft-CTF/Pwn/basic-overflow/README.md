# basic-overflow

**Category** : Pwn
**Points** : 224

This challenge is simple.

It just gets input, stores it to a buffer.

It calls `gets` to read input, stores the read bytes to a buffer, then exits.

What is `gets`, you ask? Well, it's time you read the manual, no?

`man 3 gets`

Cryptic message from author: There are times when you tell them something, but they don't reply. In those cases, you must try again. Don't just shoot one shot; sometimes, they're just not ready yet.

Author: drec

nc 34.123.15.202 5000

## Files : 
 - [basic-overflow](./basic-overflow)


