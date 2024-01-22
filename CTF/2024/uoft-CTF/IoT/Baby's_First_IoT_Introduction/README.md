# Baby's First IoT Introduction

**Category** : IoT
**Points** : 10

The following collections of challenges utilize the instructions provided below. For each flag, there will be a challenge to submit it. The flag format will NOT be UofTCTF{...}. The root IP is 35.225.17.48.

* Part 1 - Here is an FCC ID, Q87-WRT54GV81, what is the frequency in MHz for Channel 6 for that device? Submit the answer to port 3895.
* Part 2 - What company makes the processor for this device? https://fccid.io/Q87-WRT54GV81/Internal-Photos/Internal-Photos-861588. Submit the answer to port 6318.
* Part 3 - Submit the command used in U-Boot to look at the system variables to port 1337 as a GET request ex. 35.225.17.48:1337/{command}. This output is needed for another challenge. **There is NO flag for this part**.
* Part 4 – Submit the full command you would use in U-Boot to set the proper environment variable to a /bin/sh process upon boot to get the flag on the webserver at port 7777. Do not include the ‘bootcmd’ command. It will be in the format of "something something=${something} something=something" Submit the answer on port 9123.
* Part 5 - At http://35.225.17.48:1234/firmware1.bin you will find the firmware. Extract the contents, find the hidden back door in the file that is the first process to run on Linux, connect to the backdoor, submit the password to get the flag. Submit the password to port 4545.
* Part 6 - At http://35.225.17.48:7777/firmware2.bin you will find another firmware, submit the number of lines in the ‘ethertypes’ file multiplied by 74598 for the flag on port 8888.

The flag for this introduction is {i_understand_the_mission}



