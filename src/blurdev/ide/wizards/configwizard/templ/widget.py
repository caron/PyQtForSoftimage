[templ::py_header]

from blurdev.gui.dialogs.configdialog import ConfigWidget

class [class]( ConfigWidget ):
	# define static members to store/retrieve data
	prefName		= 'config/[group]/[name]'
	
#!	showSettings = True

	def __init__( self, parent ):
		ConfigWidget.__init__( self, parent )
		
		# load the ui
		import blurdev.gui
		blurdev.gui.loadUi( __file__, self )
		
		# refresh the ui
		self.refreshUi()
	
	def checkForSave( self ):
		"""
			\remarks	checks the widget to see if the data stored is invalid
			\return		<bool>	if the data is successfully saved or ready to otherwise close/update
		"""
		return True
	
	def recordUi( self ):
		"""
			\remarks	records the latest ui settings to the data
		"""
		pass
#!		[class].showSettings = self.uiShowSettingsCHK.isChecked()

	def refreshUi( self ):
		"""
			\remarks	refrshes the ui with the latest data settings
		"""
		pass
#!		self.uiShowSettingsCHK.setChecked( [class].showSettings )
	
	@staticmethod
	def reset():
		"""
			\remarks	resets the config values to their default
						this method will be called by the config dialog's Reset button
			\return		<bool> 	should return True if the reset was successful
		"""
		from blurdev import prefs
		pref = prefs.find( [class].prefName )
		
		# restore settings from the pref file
#!		[class].showSettings = pref.restoreProperty( 'showSettings' )
		
		return True
	
	@staticmethod
	def commit():
		"""
			\remarks	saves the current config values to the system
						this method will be called by the config dialog's Save/Save & Exit buttons
			\return		<bool> 	should return True if the commit was successful
		"""
		from blurdev import prefs
		pref = prefs.find( [class].prefName )
		
		# record settings to the pref file
#!		pref.recordProperty( [class].showSettings )
		
		pref.save()
		return True
	
def registerConfig( configSet ):
	"""
		\remarks	registers the classes in this module to the inputed configSet instance
		\param		configSet 	<blurdev.gui.dialogs.configdialog.ConfigSet>
	"""
	import blurdev
	configSet.registerConfig( '[name]', [class], group = '[group]', icon = blurdev.relativePath( __file__, '[class::lower].png' ) )