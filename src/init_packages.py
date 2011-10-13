##
#	\namespace	__init__
#
#	\remarks	[REMARKS]
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		12/04/08
#

import os
import sys

def PySoftimage_initialize_OnEvent( ctxt ):
	# Import the PySoftimage package
	import PySoftimage


def XSILoadPlugin( reg ):
	from win32com.client import constants
	
	reg.Author 	= "blur"
	reg.Name 	= "Blur Site-Package Init"
	reg.Email 	= ""
	reg.URL 		= ""
	reg.Major 	= 1
	reg.Minor	= 0
	
	# Register Workgroup site-packages
	path = os.path.abspath( os.path.split( reg.fileName )[0] + '../../../data/site-packages' ).lower()
	if ( not path in sys.path ):
		sys.path.append( path )
	
	# try to import the package now
	try:
		import PySoftimage
	
	# otherwise, register it on startup
	except:
		reg.RegisterEvent( 'PySoftimage_initialize', constants.siOnStartup )
	
#/*--------------------------------------
#	XSIUnloadPlugin
#--------------------------------------*/
def XSIUnloadPlugin( reg ):
	path = os.path.abspath( os.path.split( reg.fileName )[0] + '../../../data/site-packages' ).lower()
	
	# Un-register Workgroup site-packages
	if ( path in sys.path ):
		sys.path.remove( path )
	
	popKeys = []
	for key, module in sys.modules.items():
		if ( module and hasattr( module, '__file__' ) ):
			if ( path in os.path.normpath( module.__file__ ) ):
				if ( not key in popKeys ):
					popKeys.append( key )
	
	# Remove modules from existence
	for key in popKeys:
		sys.modules.pop( key )
		
	