[templ::py_header]

# define global variables
_loaded		= False
_plugins 	= {}

# define global functions
def init():
	global _loaded
	global _plugins
	if ( not _loaded ):
		_loaded = True
		
		import os.path, glob
		filenames = glob.glob( os.path.split( __file__ )[0] + '/*/register.xml' )
		for filename in filenames:
			self.registerPlugin( filename )
			
def findPlugin( pluginName, fail = None ):
	init()
	return _plugins.get( str(pluginName), fail )

def pluginNames():
	init()
	return _plugins.keys()

def plugins():
	init()
	return _plugins.values()

def registerPlugin( filename ):
	from blurdev.XML import XMLDocument
	doc = XMLDocument()
	if ( doc.load( filename ) ):
		# load the registration information
		root = doc.root()
		
#!		create registration information and then register something to the plugins dictionary
		
		return True
	return False