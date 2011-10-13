##
#	\namespace	blurdev.version
#
#	\remarks	version module to track the version information for the blurdev
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		04/16/09
#

_major		= 1		# User defined major version
_minor		= 00	# User defined minor version

#-------------------------------------------------------------------------------------------------------------

import glob
import re
import os.path
		
# Load build version from file
_currentBuild		= 0
filename 			= os.path.split( __file__ )[0] + '/build.txt'
if ( os.path.exists( filename ) ):
	f 				= open( filename, 'r' )
	_currentBuild	= int( f.read() )
	f.close()

#-------------------------------------------------------------------------------------------------------------

def major():
	return _major

def minor():
	return _minor

def currentBuild():
	return _currentBuild

def toString( version = None ):
	# return the current version information for this system
	if ( version == None ):
		vstr = versionString(major(),minor(),currentBuild())
		return vstr
	
	# return the version string for a float
	elif ( type( version ) == float ):
		maj 	= int( version )
		min 	= round((version % 1) * 100)
		build 	= 0
		return versionString(maj,min,build)

def versionString( major, minor, build ):
	return 'v%i.%02i.%i' % (major,minor,build)