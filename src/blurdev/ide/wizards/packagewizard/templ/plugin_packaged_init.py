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
		filenames = glob.glob( os.path.split( __file__ )[0] + '/*/__init__.py' )
		for filename in filenames:
			modname = os.path.normpath( filename ).split( os.path.sep )[-2]
			
			# do not import the init module
			if ( modname != '__init__' ):
				package = '%s.%s' % ( __name__, modname )
				try:
					__import__( package )
				except:
					print 'Error importing %s plugin: %s' % ( __name__, modname )

def findPlugin( pluginName, fail = None ):
	init()
	return _plugins.get( str(pluginName), fail )

def pluginNames():
	init()
	return _plugins.keys()

def plugins():
	init()
	return _plugins.values()

def registerPlugin( pluginName, plugin ):
	_plugins[ str(pluginName) ] = plugin