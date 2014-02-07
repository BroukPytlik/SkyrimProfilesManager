SkyrimProfileManager
====================

SPM is a small and simple script in Python, that allows users to organize Skyrim saves with related mods to profiles.

IMPORTANT !
---------------------------------------
This is a very first release, backup your savegame folder first! 
(C:\Users\username\Documents\my games\skyrim) 

How To Use
----------
Run the SkyrimProfileManager.exe file.
If it cannot find your Skyrim installation, add it manually
to a SkyrimProfileManager.ini file in your Skyrim profile folder
(usually it is Documents\my games\Skyrim).


For development
---------------
Requires:
  - python 2.7
  - pywin32
  - cxfreeze for compiling

Build with `cxfreeze SkyrimProfilesManager.py --target-dir dist`
  
Changelog:
----------
v0.2 - Added autodetection and ini config, 
	added "save plugins list" option to menu 
	and created .exe download
v0.1 - initial release
