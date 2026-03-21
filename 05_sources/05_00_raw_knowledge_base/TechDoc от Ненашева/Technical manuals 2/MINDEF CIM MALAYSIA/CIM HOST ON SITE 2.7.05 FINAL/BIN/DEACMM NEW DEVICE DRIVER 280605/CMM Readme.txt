Hi Bradders...
 
I've done some work on the CMM device driver, but have not been able to test it. I can't get any of the CIM software device drivers running on my XP machine and the floppy drive has failed on my 98 laptop.
 
So I've attached the EXE I've rebuilt and I suggest using the DEACMM.INI file I've included. 
I believe the problem is that the RS232 port is getting closed, then reopened between checking for a character to come in, so if the char comes whilst the port is closedwe'll miss it and so miss the 'idle' (if you remember it assumes idel when any character come into the device driver from the CMM). So the solution is not to close the port between checks, and not to flush the input buffer between checks. I've made all these selectable via the INI file so by default it acts the same as the old device driver, but adding the entries makes it behave differently (and hopefully better) 
 
Hope you can test with a couple of PCs setup back-to-back via an RS232 link, or alternatively ask Malaysia to test???
 
Let me know if all's well (or not) and in the mean time I'll see if I can get my laptop working.
 
Say hi to the gang from me...
 
Jim
 
PS - Had to rename the DEACMM.EXE to DEACMM.XEX 'cause my email program will not allow me to send EXEs - just rename it when you get it.
(Shit - had to rename .INI to .NIN too)
 
The INI file includes these additional entries...
[COMMS]
FlushInputBetweenChecks = 0 or 1
= 0 The RS232 input buffer is NOT flushed between polls
= 1 The RS232 input buffer IS flushed between polls (default)
FlushInputAfterChecking = 0 or 1
= 0   The RS232 input buffer is NOT flushed after a char is received
= 1   The RS232 input buffer IS flushed after a char is received (default)

KeepChannelOpen = 0 or 1
= 0 The RS232 port is closed in between polls (default)
= 1 The RS232 port is kept open in between polls

PollingCount = 2 to 10
How often the RS232 port is polled. This is s multiple of the "Sampling Interval" in the [TIMER] section So a Sampling Interval of 500 (1/2 second) and a PollingCount of 5 Means the RS232 port is polled every 2.5 seconds. (default = 5)

ReceiveTimeout = 500 to 5000
How long the receiver will wait for a char. This value should be less than the polling interval (see above - this good example shows a polling interval of 2.5 secs with a receive timeout of 2 secs) 
(default = 2000 msecs)




Hi Graham...
 
Here is the modified DEACMM files I've worked on. As I explained over the phone, I havn't made any major changes to how they work, just added plenty of INI file entries so that the way the RS232 port is accessed/flushed can be changed. The INI file entry names I've used should make sense.
 
Gazy...  how ya doing mate - bet it's nice to be doing a bit of ancient CIM stuff every now and again. I hear you made a small mod to the DEA device driver so now we're out of synch. Like I said, I've only really put INI file entries arond things to turn them on and off, but I also changed the names of stuff from CODETAG to DEACMM 'cause it was buggin me.
 
I'm away now 'till next tuesday so good luck and let me know how things go
 
Jim

James,
 
      Just a couple of points on the CMM device driver. We should have the HMK card (ASRS) and the Camera back next week, so i think a visit to Malaysia will be sooner rather than later. In passing today, i was trying to test your modified CMM device driver on 2 computers, it would not run because i did not have an IO card in the PC and as you know the device driver look for the IO Manager to be running first. Andy fixed the IOCARD1.DLL so that it would run in emulation mode if it could not find the DLL's or the card. The Device driver would still not run because it came up with an CODE TAG ERROR MESSAGE (Andy thinks the CMM device driver was modified to make the Code Tag device driver). Also i have just found out from Andy that he modified the CMM device driver for Malaysia, so your copy that you have modified might not be the latest copy we have here, therefore I attach the IOCARD.DLL and DEACMM1.CPP for your attention.
 
      Note ? is there a way just to be able to run a single device driver with out anything else running i.e. in testing the CMM device driver?
