##
#	\namespace	blurdev.gui.dialogs.configdialog.configset
#
#	\remarks	Defines the ConfigSet class that will manage config widgets
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		04/20/10
#

from PyQt4.QtCore import QObject

class ConfigSetItem( QObject ):
	def __init__( self, configSet ):
		QObject.__init__( self, configSet )
		
		self._configClass 	= None
		self._groupName		= 'Default'
		self._icon			= ''
	
	def configClass( self ):
		return self._configClass
	
	def groupName( self ):
		return self._groupName
		
	def icon( self ):
		return self._icon
		
	def setConfigClass( self, configClass ):
		self._configClass = configClass
	
	def setGroupName( self, grpName ):
		self._groupName = grpName
	
	def setIcon( self, icon ):
		self._icon = icon
	
#---------------------------------------------------------------

class ConfigSet( QObject ):
	def __init__( self, parent = None ):
		QObject.__init__( self, parent )
	
	def configGroups( self ):
		output = []
		
		for child in self.findChildren( ConfigSetItem ):
			grpName = str(child.groupName())
			if ( not grpName in output ):
				output.append( grpName )

		output.sort()		
		
		return output
	
	def configGroupItems( self, groupName ):
		output = [ child for child in self.findChildren( ConfigSetItem ) if ( child.groupName() == groupName ) ]
		output.sort( lambda x,y: cmp( x.objectName(), y.objectName() ) )
		return output
	
	def edit( self, parent = None ):
		from blurdev.gui.dialogs.configdialog import ConfigDialog
		return ConfigDialog.edit( self, parent )
		
	def find( self, configName ):
		for child in self.findChildren( ConfigSetItem ):
			if ( child.objectName() == configName ):
				return child.configClass()
		return None
	
	def loadFrom( self, filename, package ):
		# load the config plugins
		import os.path, glob, sys
		
		filenames = glob.glob( os.path.split( filename )[0] + '/*.py' )
		for f in filenames:
			modname = os.path.basename( f ).split( '.' ) [0]
			if ( modname != '__init__' ):
				configmodule = '%s.%s' % (package,modname)
				try:
					__import__( configmodule )
				except:
					print 'could not import %s' % configmodule
					continue
				
				mod = sys.modules.get( configmodule )
				if ( mod ):
					mod.registerConfig( self )
	
	def registerConfig( self, configName, configClass, group = 'Default', icon = '' ):
		item = ConfigSetItem( self )
		item.setObjectName( configName )
		item.setGroupName( group )
		item.setConfigClass( configClass )
		item.setIcon( icon )
		
		# load the last settings
		configClass.reset()
		
		return item

