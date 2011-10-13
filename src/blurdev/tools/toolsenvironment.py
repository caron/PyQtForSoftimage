##
#	\namespace	blurdev.tools.ToolsEnvironment
#
#	\remarks	Defines the ToolsEnvironment class for the tools package
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		06/11/10
#

from PyQt4.QtCore import QObject, pyqtSignal

USER_ENVIRONMENT_FILE 		= 'c:/blur/common/user_environments.xml'

class ToolsEnvironment( QObject ):
	# static members
	environments = []
	
	def __init__( self ):
		QObject.__init__( self )
		
		self._path				= ''
		self._development 		= False
		self._default			= False
		self._active			= False
		self._offline			= False
		self._custom			= False
		self._index				= None
		self._sourcefile		= ''
		self._emailOnError		= []
	
	def clearPathSymbols( self ):
		"""
			\remarks	removes the path symbols from the environment
		"""
		if ( self.isEmpty() ):
			return False
			
		path = self.normalizePath( self.path() )
		
		import sys
		oldpaths = sys.path
		newpaths = [ spath for spath in sys.path if not path in spath.lower() and spath != '.' ]
		sys.path = newpaths
		
		from blurdev import debug
		debug.debugObject( self.clearPathSymbols, '%s were removed from sys.path' % list( set( oldpaths ).difference( set( newpaths ) ) ), debug.DebugLevel.Mid )
		
		newmodules 	= {}
		
		import blurdev
		symbols		= blurdev.core.protectedModules()
		for key, value in sys.modules.items():
			if ( not key in symbols ):
				found = False
				try:
					found = path in value.__file__.lower()
				except:
					pass
				
				if ( found ):
					debug.debugObject( self.clearPathSymbols, 'removing %s from sys.modules' % key, debug.DebugLevel.Mid )
					sys.modules.pop( key )
		
		return True
	
	def emailOnError( self ):
		return self._emailOnError
	
	def index( self ):
		"""
			\remarks	returns the index of tools for this environment
			\return		<blurdev.tools.index.Index>
		"""
		if ( not self._index ):
			from toolsindex import ToolsIndex
			self._index 	= ToolsIndex( self )
			
		return self._index
				
	def isActive( self ):
		return self._active
	
	def isEmpty( self ):
		return self._path == ''
	
	def isCustom( self ):
		return self._custom
	
	def isDevelopment( self ):
		return self._development
	
	def isDefault( self ):
		return self._default
	
	def isOffline( self ):
		return self._offline
	
	def path( self ):
		return self._path
	
	def recordXml( self, xml ):
		envxml = xml.addNode( 'environment' )
		envxml.setAttribute( 'name', self.objectName() )
		envxml.setAttribute( 'loc', self.path() )
		envxml.setAttribute( 'default', self._default )
		envxml.setAttribute( 'development', self._development )
		envxml.setAttribute( 'offline', self._offline )
		
		if ( self._custom ):
			envxml.setAttribute( 'custom', True )
		
		if ( self._emailOnError ):
			envxml.setAttribute( ':'.join( self._emailOnError ) )
		
	def relativePath( self, path ):
		"""
			\remarks	returns the relative path from the inputed path to this environment
			\return		<str>
		"""
		if ( not self.isEmpty() ):
			import os.path
			return os.path.abspath( os.path.join( str( self.path() ), str( path ) ) )
		return ''
	
	def resetPaths( self ):
		self.clearPathSymbols()
		self.registerPath( self.path() )
		import blurdev
		blurdev.core.emitEnvironmentActivated()
		
	def setActive( self, silent = False ):
		"""
			\remarks	sets this environment as the active environment and switches the currently running modules from the
						system
		"""
		if ( not ( self.isActive() or self.isEmpty() ) ):
			# clear out the old environment
			old = self.activeEnvironment()
			old.clearPathSymbols()
			old._active = False
			
			# register this environment as active and update the path symbols
			self._active = True
			self.registerPath( self.path() )
			
			# emit the environment activateion change signal
			if ( not silent ):
				import blurdev
				blurdev.core.emitEnvironmentActivated()
				
			return True
		return False
	
	def setCustom( self, state = True ):
		self._custom = state
	
	def setDefault( self, state = True ):
		self._default = state
	
	def setDevelopment( self, state = True ):
		self._development = state
	
	def setOffline( self, state = False ):
		self._offline = state
	
	def setEmailOnError( self, emails ):
		self._emailOnError = [ entry for entry in emails if str( entry ) != '' ]
	
	def setPath( self, path ):
		self._path = path
	
	def setSourceFile( self, filename ):
		self._sourcefile = filename
	
	def sourceFile( self ):
		return self._sourcefile
	
	def stripRelativePath( self, path ):
		"""
			\remarks	removes this environments path from the inputed path
			\return		<str>
		"""
		return self.normalizePath( path ).replace( self.normalizePath( self.path() ), '' ).lstrip( '\\/' )
	
	@staticmethod
	def activeEnvironment():
		"""
			\remarks	looks up the active environment for the system
			\return		<ToolsEnvironment>
		"""
		for env in ToolsEnvironment.environments:
			if ( env.isActive() ):
				return env
		return ToolsEnvironment()
	
	@staticmethod
	def createNewEnvironment( name, path, default = False, development = False, offline = True, environmentFile = '' ):
		output = ToolsEnvironment()
		
		if ( not environmentFile ):
			environmentFile = USER_ENVIRONMENT_FILE
		
		output.setObjectName(	name )
		output.setPath( 		path )
		output.setDefault( 		default )
		output.setDevelopment( 	development )
		output.setOffline(		offline )
		output.setSourceFile(	environmentFile )
		output.setCustom(		True )
		
		ToolsEnvironment.environments.append( output )
		return output
	
	@staticmethod
	def defaultEnvironment():
		"""
			\remarks	looks up the default environment for the system
			\return		<ToolsEnvironment>
		"""
		for env in ToolsEnvironment.environments:
			if ( env.isDefault() ):
				return env
		return ToolsEnvironment()
	
	@staticmethod
	def findEnvironment( name ):
		"""
			\remarks	looks up the environment by the inputed name
			\return		<ToolsEnvironment>
		"""
		for env in ToolsEnvironment.environments:
			if ( str( env.objectName() ) == str( name ) ):
				return env
		return ToolsEnvironment()
	
	@staticmethod
	def findDevelopmentEnvironment():
		for env in ToolsEnvironment.environments:
			if( env.isDevelopment() ):
				return env
		return ToolsEnvironment.activeEnvironment()
	
	@staticmethod
	def fromXml( xml ):
		"""
			\remarks	generates a new tools environment based on the inputed xml information
			\param		xml		<blurdev.XML.XMLElement>
			\return		<ToolsEnvironment>
		"""
		output = ToolsEnvironment()
		
		output.setObjectName(	xml.attribute( 'name' ) )
		output.setPath( 		xml.attribute( 'loc' ) )
		output.setDefault( 		xml.attribute( 'default' ) == 'True' )
		output.setDevelopment( 	xml.attribute( 'development' ) == 'True' )
		output.setOffline(		xml.attribute( 'offline' ) == 'True' )
		output.setEmailOnError( xml.attribute( 'emailOnError' ).split( ';' ) )
		output.setCustom(		xml.attribute( 'custom' ) == 'True' )
		
		return output
	
	@staticmethod
	def normalizePath( path ):
		"""
			\remarks	returns a normalized path for this environment to use when registering paths to the sys path
			\param		path		<str> || <QString>
			\return		<str>
		"""
		import os.path
		return os.path.abspath( str( path ) ).lower()
	
	@staticmethod
	def loadConfig( filename, included = False ):
		"""
			\remarks	loads the environments from the inputed config file
			\param		filename		<str>
			\param		included		<bool> 	marks whether or not this is an included file
			\return		<bool> success
		"""
		from blurdev.XML import XMLDocument
		doc = XMLDocument()
		if ( doc.load( filename ) ):
			root = doc.root()
			
			for child in root.children():
				# include another config file
				if ( child.nodeName == 'include' ):
					ToolsEnvironment.loadConfig( child.attribute( 'loc' ), True )
				
				# load an environment
				elif ( child.nodeName == 'environment' ):
					env = ToolsEnvironment.fromXml( child )
					env.setSourceFile( filename )
					ToolsEnvironment.environments.append( env )
			
			# initialize the default environment
			if ( not included ):
				ToolsEnvironment.defaultEnvironment().setActive( silent = True )
				
			return True
		return False
	
	@staticmethod
	def recordConfig( filename = '' ):
		if ( not filename ):
			filename = USER_ENVIRONMENT_FILE
		
		if ( not filename ):
			return False
		
		from blurdev.XML import XMLDocument
		doc = XMLDocument()
		root = doc.addNode( 'tools_environments' )
		root.setAttribute( 'version', 1.0 )
		
		import os.path
		filename = os.path.normcase(filename)
		for env in ToolsEnvironment.environments:
			if ( os.path.normcase(env.sourceFile()) == filename ):
				env.recordXml( root )
		
		return doc.save( filename )
	
	@staticmethod
	def registerPath( path ):
		"""
			\remarks	registers the inputed path to the system
			\param		path		<str>
			\return		<bool> success
		"""
		import os.path
		if ( path and path != '.' ):
			import sys
			sys.path.insert( 0, ToolsEnvironment.normalizePath( path ) )
			return True
		return False
	
	@staticmethod
	def registerScriptPath( filename ):
		import os.path
		
		# push the local path to the front of the list
		path		= os.path.split( filename )[0]
		
		# if it is a package, then register the parent path, otherwise register the folder itself
		if ( os.path.exists( path + '/__init__.py' ) ):
			path	= os.path.abspath( path + '/..' )
		
		# if the path does not exist, then register it
		ToolsEnvironment.registerPath( path )