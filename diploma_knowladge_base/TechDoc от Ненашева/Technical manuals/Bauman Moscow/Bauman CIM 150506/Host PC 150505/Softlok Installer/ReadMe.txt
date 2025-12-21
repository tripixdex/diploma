Driver installation utilities

sl2inst.exe is a Windows utility to copy the appropriate driver for the OS
and add the registry entries.

drvinst.exe is a Windows command line version of sl2inst that can be called by
your own installation program if required. The C source code (drvinst.c) can be
found in the Source directory of this disk.

'drvinst install' will install the driver and registry entries

'drvinst uninstall' will remove the driver and registry entries

If you move these installation programs to another location please remember
that both sl2inst.exe and drvinst.exe expect to find the two driver files
windrvr.vxd and windrvr.sys in the same directory.

Softlok International Ltd
Tel:   44 (1204) 436000
Fax:   44 (1204) 436025
Email: tech@softlok.com
Url:   http://www.softlok.com



