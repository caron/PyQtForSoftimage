##
#	\namespace	[package].[config::lower]
#
#	\remarks	The main View class for the [name] Trax View
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		[date]
#

from PyQt4.QtGui 			import QWidget

class [config]( QWidget ):
	# define class level config options
#!	includeMembers = True	
	
	def __init__( self, parent ):
		QWidget.__init__( self, parent )
		
		# create the ui controls
#!		from PyQt4.QtGui import QCheckbox, QVBoxLayout
#!		layout = QVBoxLayout()
#!		self._incMemeberCHK = QCheckbox(self)
#!		self._incMemeberCHK.setText( 'Include Members' )
#!		layout.addWidget( self._incMemeberCHK )
#!		layout.addStretch(1)
#!		self.setLayout( layout )

		# reset to the current settings
		self.reset()
	
	def commit( self ):
		"""
			\remarks	records the current ui settings to memory
		"""
#!		[config].includeMembers = self._incMemeberCHK.isChecked()

		[config].saveSettings()
	
	def reset( self ):
		"""
			\remarks	matches the ui settings to the current memory state
		"""
#!		self._incMemeberCHK.setChecked( [config].includeMembers )
		pass
	
	@staticmethod
	def saveSettings():
		from blurdev import prefs
		pref = prefs.find( 'views/[name::lower]' )
		
		# record the config properties
#!		pref.recordProperty( 'includeMembers', [config].includeMembers )

		# save the prefs
		pref.save()

	@staticmethod
	def loadSettings():
		from blurdev import prefs
		pref = prefs.find( 'views/[name::lower]' )
		
		# restore config properties
#!		[config].includeMembers = pref.restoreProperty( 'includeMembers' )

# initialize the config settings
[config].loadSettings()