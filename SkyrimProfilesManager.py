# Author: Jan Tulak (jan@tulak.me]
# Version: v0.1
# License: GNU GPLv3
# Requires Python 2.7

import os,shutil, sys

USERNAME="Jan"
SKYRIM_PATH="E:\\Steam\\steamapps\\common\\skyrim\\"
SKYRIM_BINARY="skse_loader.exe"

SAVES_ROOT="c:\\Users\\"+USERNAME+"\\Documents\\my games\\skyrim"

MODS_FILE="C:\\Users\\"+USERNAME+"\\Appdata\\Local\\Skyrim\\plugins.txt"

NAMEFILE="name.txt"
SAVES=SAVES_ROOT+"\\saves"
NAMEFILE_SAVED=SAVES+"\\"+NAMEFILE
MODS_SAVED=SAVES+"\\plugins.txt"







#///////////////////////////////////////

def getSavedProfiles():
	items=os.listdir(SAVES_ROOT)
	profiles=[]
	for name in items:
		if os.path.isdir(os.path.join(SAVES_ROOT,name)):
			# if it is dir, try to load name
			try:
				with open (os.path.join(SAVES_ROOT,name,NAMEFILE), "r") as myfile:
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

def saveProfile(targetName):
	# save plugin list
	try:
		shutil.move(MODS_SAVED,MODS_SAVED+".bak") # previous version
	except:
		pass
	shutil.copy2(MODS_FILE, MODS_SAVED) # save new one
	
	# rename profile
	shutil.move(SAVES, os.path.join(SAVES_ROOT,targetName))
	

def loadProfile(name):
	# rename profile
	shutil.move(os.path.join(SAVES_ROOT,name),SAVES)
	
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
		
		if os.path.exists(os.path.join(SAVES_ROOT,i)):
			i=""
			print "This name already exists."
			print ""
			continue
	
	namefile = open(os.path.join(NAMEFILE_SAVED), 'w+')
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
	print "'s' to run Skyrim"
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
			if prompt in ["s", "x","n","h"]:
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
			if active == "":
				print "You have to select a profile first!"
				continue
			print "Running Skyrim."
			os.system(os.path.join(SKYRIM_PATH,SKYRIM_BINARY))
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

# run main() again and again while it returns True
while main():
	pass
