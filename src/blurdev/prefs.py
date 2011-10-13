##
#	\namespace	blurdev.prefs
#
#	\remarks	Module for handling user interface preferences
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		04/09/10
#

from blurdev.XML import XMLDocument

#-------------------------------------------------------------------------------------------------------------

class Preference( XMLDocument ):
	""" a preference document is a sub-class of the XMLDocument and is used for storing custom information
		about blurdev components, most often tools or views """
	
	RootPath = 'c:/blur/userprefs'	# this is the folder where all preference files will be saved per core
	
	def __init__( self ):
		XMLDocument.__init__( self )
		self._filename 	= ''
		self._name		= ''
	
	def load( self, filename = '' ):
		""" loads the preferences from the file, using the current stored filename """
		if ( not filename ):
			filename = self.filename()
		
		XMLDocument.load( self, filename )
	
	def name( self ):
		""" return the name attribute """
		return self._name
		
	def filename( self ):
		""" return this documents filename, deriving the default filename from its name and standard preference location  """
		if ( not self._filename ):
			#import blurdev, os.path
			key = self.name().lower().replace( ' ', '-' )
			self._filename = self.path() + '%s.pref' % key
		
		return self._filename
	
	def path( self, coreName = '' ):
		""" return the path to the application's prefrences folder """
		import blurdev, os.path
		
		# use the core
		if ( not coreName and blurdev.core ):
			coreName = blurdev.core.objectName() 
			
		return os.path.join( Preference.RootPath, 'app_%s/' % coreName )
	
	def recordProperty( self, key, value ):
		""" connects to the root recordProperty method """
		return self.root().recordProperty( key, value )
	
	def restoreProperty( self, key, default = None ):
		""" connects to the root restoreProperty method """
		return self.root().restoreProperty( key, default )
	
	def save( self, filename = '' ):
		""" save the preference file """
		if ( not filename ):
			filename = self.filename()
		
		import os
		path = os.path.split( filename )[0]
		
		# try to create the path
		if ( not os.path.exists( path ) ):
			import os
			os.makedirs( path )
			
		XMLDocument.save( self, filename )
	
	def setName( self, name ):
		""" sets the name of this Preference """
		self._name = name
	
	def setVersion( self, version ):
		""" sets the version number of this preferene """
		self.root().setAttribute( 'version', version )
	
	def version( self ):
		""" returns the current version of this preference """
		return float( self.root().attribute( 'version', 1.0 ) )

#-------------------------------------------------------------------------------------------------------------

# cache of all the preferences
_cache = {}

def clearCache():
	_cache.clear()

def find( name, reload = False, coreName = '' ):
	"""
		\remarks	Finds a preference for the with the inputed name
					If a pref already exists within the cache, then the cached pref is returned,
					otherwise, it is loaded from the blurdev preference location
		
		\param		name	<str>	the name of the preference to retrieve
		\param		reload	<bool>	reloads the cached item
		
		\return		<blurdev.prefs.Preference>
	"""
	import blurdev
	
	key = str( name ).replace( ' ', '-' ).lower()
	
	if ( reload or not key in _cache ):
		import os.path
		
		# create a new preference record
		pref = Preference()
		
		# look for a default preference file
		filename = pref.path( coreName ) + '%s.pref' % key
		if ( os.path.exists( filename ) ):
			pref.load( filename )
		else:
			# create default information
			root = pref.addNode( 'preferences' )
			root.setAttribute( 'name', name )
			root.setAttribute( 'version', 1.0 )
			root.setAttribute( 'ui', '' )
		
		pref.setName( key )
		_cache[key] = pref
	
	return _cache[key]