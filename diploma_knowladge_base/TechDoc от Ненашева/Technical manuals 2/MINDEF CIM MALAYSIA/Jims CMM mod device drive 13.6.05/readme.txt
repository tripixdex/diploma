Hi Bradders...
 
I've done some work on the CMM device driver, but have not been able to test it. I can't get any of the CIM software device drivers running on my XP machine and the floppy drive has failed on my 98 laptop.
 
So I've attached the EXE I've rebuilt and I suggest using the DEACMM.INI file I've included. 
I believe the problem is that the RS232 port is getting closed, then reopened between checking for a character to come in, so if the char comes whilst the port is closedwe'll miss it and so miss the 'idle' (if you remember it assumes idel when any character come into the device driver from the CMM). So the solution is not to close the port between checks, and not to flush the input buffer between checks. I've made all these selectable via the INI file so by default it acts the same as the old device driver, but adding the entries makes it behave differently (and hopefully better) 
 
Hope you can test with a couple of PCs setup back-to-back via an RS232 link, or alternatively ask Malaysia to test???
 
Let me know if all's well (or not) and in the mean time I'll see if I can get my laptop working.
