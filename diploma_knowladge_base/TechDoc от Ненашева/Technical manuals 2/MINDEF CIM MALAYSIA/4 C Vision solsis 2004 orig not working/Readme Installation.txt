Denford Firewire C-Vision/Objects.

Hardware installation.

The Firewire card may be installed in any slot in the PC, observing the normal precautions (anti-static and complete power-down). The camera should be connected later.

Software.

On restarting the PC Windows XP should automatically find the Firewire card and install the driver.

Camera driver software. 

The Firewire camera may be connected while the PC is powered up. The camera is powered and controlled by the same cable. Windows XP will recognise a camera and install a generic camera driver. This is the WRONG driver.The correct one is on the installation CD.
Right click on "My Computer" and select "Manage" from the menu, and then choose "Device Manager" from the navigation panel. Open the entry for the camera, and right click and then choose "Update Driver". Do NOT allow Windows to search for a driver, instead choose the option to install from a list or specific location, and then navigate to the \drivers\1394camera directory on the Installation CD. Then go ahead and install the driver (1394cmdr.sys).

Camera Set-up.

The camera is mounted in the furthermost position away from the light box. The camera height is adjusted so that the top of the highest chess piece is slightly below the top edge of the illuminated area in the camera view. The lens focus was set to <0.2M and the aperture to 4.
In the Capture>Brightness/Contrast menu item of C-Vision both Brightness and Auto-exposure should be set to NOT automatic. Values of just over 400 and 380 were used.
The other part of the set-up that is influenced by the brightness and auto exposure is the threshold value for the edge detection (the region of interest - ROI - is also set at the same time as the threshold value). These controls are found in the Train Class>Set-up menu item. The ROI is chosen first to cover the bright area of the light box and the objects. Then the threshold slider is adjusted (slowly) to provide good edges for the object without a lot of clutter (in red). A threshold value of 96 was found to work well with the lighting.

Training.

This is carried out in the normal manner.