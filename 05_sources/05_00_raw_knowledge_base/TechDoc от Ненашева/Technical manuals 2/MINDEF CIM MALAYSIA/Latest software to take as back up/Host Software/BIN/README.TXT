
***********************************************************

	Changes to the Device Drivers...

***********************************************************

25/05/99 - JHB - ASRS Changes to the device driver to support the new
                 PICK and PLACE commands

25/05/99 - JHB - Added an option in the INI files to disable the
                 Close button on the System Menu
[MAIN]
No Close = 1

25/05/99 - JHB - Device drivers now remember their position and size
                 when they close
[MAIN WINDOW]
X=
Y=
W=
H=

25/05/99 - JHB - Some Device drier now have an Edit menu option that launches
                 notepad. This can be overridden in the INI file
[FILES]
Editor=C:\windows\notepad.exe

25/05/99 - JHB - CODETAG no longer case sensitive when doing a verify

27/05/99 - JHB - CODETAG has an option to prompt the user whether they want
                 to ignore verify errors, selectable in the INI file
[MAIN]
Report Errors = 1

05/11/99 - AG -  CONVEYOR removed bitmap from centre of window.

05/11/99 - AG -  CONVEYOR if circular (ie store on conveyor, no ASRS) then go
                 idle after adding pallet to the queue. Before if there where
                 pallets already in the queue the part process of the Dispatcher
                 would never go idle.

08/11/99 - AG -  CONVEYOR changed above so that it uses ASRS deley setting before
                 it goes idle, previously it went idle striaght away.

19/04/00 - JHB - CONVEYOR changed so that the polling timer can be supressed when
                 a pallet is being passed on from a station. The plunger will wait
                 for a number of timer ticks before popping back out.
                 It allows pallets with two guide pins to let the 2nd pin pass
                 the sensor 'unseen'. Number of ticks is in CONVEYOR.INI...
[TIMER]
PinReleaseDelay = 4

17/05/00 - JHB - Fixed bug in above mod (19/04/00)

17/05/00 - JHB - Fixed About Dialog not working and gave it a version of v1.11

17/05/00 - JHB - New implementation of Light Barrier Safety Rules
                 Uses an entry in the devies INI file
[SAFETY BIT]
MANUAL=1
                 Allows the Device Driver to be used in manual mode regardless
                 of the state of the Setup/Auto keywsitch.
                 Manual=1 the light barrier is only checked when a
                 DDE DoCommand is recieved.
                 Manual=0 the light barrier is only checked when a
                 DDE DoCommand is recieved.

18/05/00 - JHB - Modification to the Machine Tools RS232 comms.
                 Communications type can now be specified in the machines INI file
                 (it used to be a compiler directive)
[COMMS]
Send Type =      1 = Old Fanuc
                 2 = PNC3
                 3 = Denford
                 4 = Fanuc

18/05/00 - JHB - Removed security (Dongle) checking from VISNU14 Vision System DD
                 The dongle stuff had been commented out in a previous version and
                 replaced with FLASH stuff that didn't work (don't know why?).

18/05/00 - JHB - Compiled New Device Driver Products
                 Version numbers are defined in the DDs resource file, and
                 can be viewed by RightClick->Properties->Version

ASRSU18.EXE      v1.9
CONVEYOR.EXE     v1.11
ROBOT.EXE        v2.1
LATHEU.EXE       v5.92
MILLERU.EXE      v5.92
CODETAG.EXE      v1.8
AGV.EXE          v1.5
ROBOTU67.EXE     v6.8
VISNU14.EXE      v1.5
DEACMM.EXE       v1.8

14/06/00 - JHB - Vision Device Driver now allows you to invert the busy input signal...

[IO PORT DATA]
inverted inputs = 1

14/06/00 - JHB - CodeTag Device driver was blowing up when receiving commands
                 from the Host. This has now been fixed.
                 (IOPort manager wasn't being initialised and so SafetyCheck
                  was causing the fault)
