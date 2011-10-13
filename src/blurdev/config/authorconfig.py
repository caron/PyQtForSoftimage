##
#	\namespace	blurdev.config.authorconfig
#
#	\remarks	Drives the Author config settings for the blurdev system
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		11/19/10
#

from blurdev.gui.dialogs.configdialog import ConfigWidget

class AuthorConfig( ConfigWidget ):
	# define static members to store/retrieve data
	prefName		= 'config/Default/Author'
	
	name			= 'Blur Studio'
	email			= 'beta@blur.com'
	company			= 'Blur Studio'
	initials		= 'BS'
	
	def __init__( self, parent ):
		ConfigWidget.__init__( self, parent )
		
		# load the ui
		import blurdev.gui
		blurdev.gui.loadUi( __file__, self )
		
		# refresh the ui
		self.refreshUi()
	
	def recordUi( self ):
		AuthorConfig.name		= self.uiNameTXT.text()
		AuthorConfig.email		= self.uiEmailTXT.text()
		AuthorConfig.company	= self.uiCompanyTXT.text()
		AuthorConfig.initials	= self.uiInitialsTXT.text()
	
	def refreshUi( self ):
		self.uiNameTXT.setText( 	AuthorConfig.name )
		self.uiEmailTXT.setText( 	AuthorConfig.email )
		self.uiCompanyTXT.setText( 	AuthorConfig.company )
		self.uiInitialsTXT.setText( AuthorConfig.initials )
	
	@staticmethod
	def commit():
		"""
			\remarks	saves the current config values to the system
						this method will be called by the config dialog's Save/Save & Exit buttons
			\return		<bool> 	should return True if the commit was successful
		"""
		from blurdev import prefs
		pref = prefs.find( AuthorConfig.prefName )
		
		# record settings to the pref file
		pref.recordProperty( 'name',		AuthorConfig.name )
		pref.recordProperty( 'email', 		AuthorConfig.email )
		pref.recordProperty( 'company',		AuthorConfig.company )
		pref.recordProperty( 'initials',	AuthorConfig.initials )
		
		pref.save()
		return True
	
	@staticmethod
	def reset():
		"""
			\remarks	resets the config values to their default
						this method will be called by the config dialog's Reset button
			\return		<bool> 	should return True if the reset was successful
		"""
		from blurdev import prefs
		pref = prefs.find( AuthorConfig.prefName )
		
		# restore settings from the pref file
		AuthorConfig.name		= pref.restoreProperty( 'name', AuthorConfig.name )
		AuthorConfig.email 		= pref.restoreProperty( 'email', AuthorConfig.email )
		AuthorConfig.company	= pref.restoreProperty( 'company', AuthorConfig.company )
		AuthorConfig.initials	= pref.restoreProperty( 'initials', AuthorConfig.initials )
		
		return True
	
def registerConfig( configSet ):
	"""
		\remarks	registers the classes in this module to the inputed configSet instance
		\param		configSet 	<blurdev.gui.dialogs.configdialog.ConfigSet>
	"""
	import blurdev
	configSet.registerConfig( 'Author', AuthorConfig, group = 'Default', icon = blurdev.relativePath( __file__, 'authorconfig.png' ) )