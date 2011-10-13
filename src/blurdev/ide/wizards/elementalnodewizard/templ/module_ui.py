##
#	\namespace	[package].[module]
#
#	\remarks	[desc::commented]
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		11/09/10
#

import blurdev
from elemental import ElementalNode

class [class]( ElementalNode ):
	# define plugin information
	pluginUiFile		= blurdev.relativePath( __file__, 'ui/[module].ui' )
	pluginIconFile		= blurdev.relativePath( __file__, '[module].png' )

	def initialize( self ):
		"""
			\remarks	[virtual]	this method is called during the creation of this node plugin type and should create/register
									the default ports and values for this Node type.  You should also use this method to create your
									signal/slot connections between ports
		"""
		# create the ports from the ui file defined as pluginUiFile
		self.createPortsFromUi()
		
		# create additional ports (usually hidden from UI for the scene)
#!		from elemental import PortDirection

		# create connections
#!		self.port( 'load' ).triggered.connect( self.load )		
		pass
	
	
	def initializeInstance( self ):
		"""			
			\remarks	[virtual]	this method is designed to initialize the values of the ports for a new instance.  This method
									differs from the initialize method, as it does not define the ports, but rather sets their value
									for the first time.  This method will not be called during loading or pasting, only when a user creates
									a fresh instance of this class.
									
									You can define the default information in the initialize method as well, however this is useful to break
									up some of the process if you have to pull the default information from somewhere that you don't want to 
									access unnecessarily
		"""
		# define the default port values
#!		self.port( 'renderWidth' ).setValue( 10 )
		pass
	
#--------------------------------------------------------------------------------------------
		
def registerPlugins( system ):
	"""
		\remarks	this method will be run by the elemental plugin registration system, and will pass in the current
					ElementalSystem instance that the plugins should be registered to.  This method must exist or your
					plugins will not be registered
					
		\param		<elemental.elementalsystem.ElementalSystem>
	"""
	# register all the nodes for this package
	system.registerPlugin( '[group]::[name]', [class] )
