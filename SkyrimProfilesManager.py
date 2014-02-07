# Author: Jan Tulak (jan@tulak.me]
# Version: v0.2
# License: GNU GPLv3
# Requires: Python 2.7
#           pywin32    

import os,shutil, sys, ConfigParser
from win32com.shell import shell, shellcon
import win32file


NAMEFILE="name.txt"
PLUGINS_FILE="plugins.txt"
INI_FILE="SkyrimProfilesManager.ini"
DEFAULT_LAUNCHER="SkyrimLauncher.exe"

#SKYRIM_PATH="E:\\Steam\\steamapps\\common\\skyrim\\"
#SKYRIM_BINARY="skse_loader.exe"

#USERNAME="Jan"
#SAVES_ROOT="c:\\Users\\"+USERNAME+"\\Documents\\my games\\skyrim"
#MODS_FILE="C:\\Users\\"+USERNAME+"\\Appdata\\Local\\Skyrim\\plugins.txt"


#SAVES=SAVES_ROOT+"\\saves"
#NAMEFILE_SAVED=SAVES+"\\"+NAMEFILE
#MODS_SAVED=SAVES+"\\plugins.txt"

SKYRIM_PATH=""
SKYRIM_BINARY=""
SAVES_ROOT=""
MODS_FILE=""
SAVES=""
NAMEFILE_SAVED=""
MODS_SAVED=""



#///////////////////////////////////////
def path(*pathes):
	return os.path.join(*pathes)

def init():
	# load user profile folder
	findProfilePathes()
	
	if os.path.exists(path(SAVES_ROOT,INI_FILE)):
		# Config file exists
		loadConfig()
		
	else:
		# Config file do not exists
		# try create a new one
		if findSkyrim():
			saveConfig(SKYRIM_PATH,SKYRIM_BINARY)
		else:
			# autodetecting of Skyrim failed, manual entry needed.
			saveConfig("",DEFAULT_LAUNCHER)
			print >> sys.stderr,\
				"Error: Skyrim wasn't find! Add correct path to",\
				path(SAVES_ROOT,INI_FILE)
			os.system('pause')
			exit (1)

def saveConfig(sPath, sLauncher):
	config = ConfigParser.RawConfigParser()
	config.add_section('Game')
	config.set('Game', 'sPath', sPath)
	config.set('Game', 'sLauncher', sLauncher)
	
	# Writing our configuration file to 'example.cfg'
	with open(path(SAVES_ROOT,INI_FILE), 'wb') as configfile:
		config.write(configfile)

def loadConfig():
	global SKYRIM_PATH
	global SKYRIM_BINARY
	
	config = ConfigParser.ConfigParser()
	config.read(path(SAVES_ROOT,INI_FILE))
	SKYRIM_PATH=config.get('Game', 'sPath')
	SKYRIM_BINARY=config.get('Game', 'sLauncher')
	if not os.path.exists(path(SKYRIM_PATH,SKYRIM_BINARY)):
		print >> sys.stderr,\
			"Error: Game path in ini file (",\
			path(SAVES_ROOT,INI_FILE),\
			") is invalid!\r\nFix it, or delete the file to autodetect correct path."
		os.system('pause')
		exit (1)
"""
Try to find default path for saves and so
"""
def findProfilePathes():
	global SAVES_ROOT
	global SAVES
	global NAMEFILE_SAVED
	global MODS_SAVED
	global MODS_FILE
	
	userDocuments=shell.SHGetFolderPath(0, shellcon.CSIDL_PERSONAL, None, 0)
	SAVES_ROOT=path(userDocuments,"my games","skyrim")
	SAVES=path(SAVES_ROOT,"saves")
	NAMEFILE_SAVED=path(SAVES,NAMEFILE)
	MODS_SAVED=path(SAVES,PLUGINS_FILE)
	
	appData=shell.SHGetFolderPath(0, shellcon.CSIDL_LOCAL_APPDATA, None, 0)
	MODS_FILE=path(appData,"Skyrim","plugins.txt")
	
""" 
Try to find Skyrim
"""	
def findSkyrim():
	global SKYRIM_PATH
	global SKYRIM_BINARY
	"TODO - better detection"
	
	"""
		Find steam
		- so at first, find drives
		- then look for program files or steam in root
	"""
	dl = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' 
	drives=[]
	for d in dl:
		if win32file.GetDriveType(d+":\\") == win32file.DRIVE_FIXED:
			drives.append(d+":\\")
	
	steam=None
	for d in drives:
		for p in [path("Program Files","Steam"), path("Program Files (x86)","Steam"),"Steam"]:
			if os.path.exists(path(d,p)):
				steam=path(d,p)
	
	if steam is None:
		return False
	
	"""
		Now find Skyrim and its launcher
	"""
	skyrim=path(steam,"steamapps","common","skyrim")
	if not os.path.exists(skyrim):
		return False
	
	SKYRIM_PATH=skyrim
	
	"Test for SKSE first, then use SkyrimLauncher.exe"
	SKYRIM_BINARY="skse_loader.exe"
	if not os.path.exists(path(SKYRIM_PATH,SKYRIM_BINARY)):
		SKYRIM_BINARY=DEFAULT_LAUNCHER
	
	return True
	

	
#///////////////////////////////////////

def getSavedProfiles():
	items=os.listdir(SAVES_ROOT)
	profiles=[]
	for name in items:
		if os.path.isdir(path(SAVES_ROOT,name)):
			# if it is dir, try to load name
			try:
				with open (path(SAVES_ROOT,name,NAMEFILE), "r") as myfile:
					profiles.append(myfile.read())
			except:
				pass
				
	return profiles
			

def getActiveProfile():
	if os.path.exists(SAVES):
		try:
			with open (NAMEFILE_SAVED, "r") as myfile:
				name=myfile.read()
		except:
			name = createProfile()
			if (name == False):
				return False
		return name
	else:
		return ""

def savePlugins():
		# save plugin list
	try:
		shutil.move(MODS_SAVED,MODS_SAVED+".bak") # previous version
	except:
		pass
	shutil.copy2(MODS_FILE, MODS_SAVED) # save new one	
		
def saveProfile(targetName):
	savePlugins()
	
	# rename profile
	shutil.move(SAVES, path(SAVES_ROOT,targetName))
	

def loadProfile(name):
	# rename profile
	shutil.move(path(SAVES_ROOT,name),SAVES)
	
	# restore plugins
	shutil.copy2(MODS_SAVED, MODS_FILE) 
	
	
def createProfile():
	i=""
	while (i==""):
		print "Enter name of the profile or 'cancel' to cancel: "
		i=raw_input()
		print ""
		
		if i=="cancel":
			return False
		
		if os.path.exists(path(SAVES_ROOT,i)):
			i=""
			print "This name already exists."
			print ""
			continue
	
	namefile = open(path(NAMEFILE_SAVED), 'w+')
	namefile.write(i)
	namefile.close()
	return i
	
	
#///////////////////////////////////////
def getProfilesFiltered(active):
	profiles=getSavedProfiles()
	return [ v for v in profiles if not v == active ]

def printProfiles(profiles):
	cnt=-1
	print "Available profiles:"
	for profile in profiles:
		cnt+=1
		print cnt," ",profile
	return cnt

def printActive(active):
	if active != "":
		print "Active profile: ",active;
	else:
		print "No active profile."
		print "You have to select one prior to starting the game."
	print ""
	
def printHelp():
	print ""
	print "Options:"
	print "Number to load a profile"
	print "'h' to print again this help"
	print "'r' to run Skyrim"
	print "'s' to save current plugins"
	print "'n' to create a new, empty profile"
	print "'x' to exit"
	print ""
	
# argument is number of available profiles
def getPrompt(maxNum):
	while True:
		print "Your option:"
		prompt=raw_input().lower()
		# known options
		try:
			if prompt in ["r", "s", "x","n","h"]:
				return prompt
			if (int(prompt) >=0 and int(prompt) <= maxNum):
				return int(prompt)
		except:
			pass
		print "Bad option, try it again. (Type 'h' for list of options)"
	
	
	
def main():
	active=getActiveProfile()
	profiles=getProfilesFiltered(active)

	if active == False:
		print "Canceled, will do nothing, exiting."
		exit()

	# list profiles	
	printActive(active)
	cnt=printProfiles(profiles)
	if cnt==-1:
		print "No additional profiles"
	
	printHelp()

	
	while True:
		prompt=getPrompt(cnt)
		
		if prompt == "x":
			print "Exiting..."
			return False
			
		elif prompt == "h":
			printHelp()
			continue
			
		elif prompt == "s":
			savePlugins()
			print "Plugins saved"
		elif prompt == "r":
			if active == "":
				print "You have to select a profile first!"
				continue
			print "Running Skyrim."
			os.chdir(SKYRIM_PATH)
			os.system(path(SKYRIM_PATH,SKYRIM_BINARY))
			return False
			
		elif prompt == "n":
			print "Create a profile"
			if active != "":
				# save current profile
				saveProfile(active)
			# create dir for new
			os.makedirs(SAVES)
			newProfile=getActiveProfile()
			if newProfile==False or newProfile == "":
				shutil.rmtree(SAVES)
			else:
				saveProfile(newProfile)
				print ""
				print "Profile ",newProfile," created. You can activate it now."
				print ""
			if active != "":
				loadProfile(active)
			profiles=getProfilesFiltered(active)
			printActive(active)
			cnt=printProfiles(profiles)
			
		else: # number - loading
			if active != "":
				saveProfile(active)
			active=profiles[prompt]
			loadProfile(active)
			print "Profile ",active," is now active."
			profiles=getProfilesFiltered(active)
			printActive(active)
			cnt=printProfiles(profiles)
			print ""
			
			

	return False


#///////////////////////////////////////

print "Skyrim Profile Manager by Zopper"
print ""

init()
# run main() again and again while it returns True
while main():
	pass
