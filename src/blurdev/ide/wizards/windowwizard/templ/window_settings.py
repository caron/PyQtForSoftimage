##
#	\namespace	[package].[module]
#
#	\remarks	[desc::commented]
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		[date]
#

from blurdev.gui import Window

class [class]( Window ):
	def __init__( self, parent = None ):
		Window.__init__( self, parent )
		
		# define ui controls
#!		from PyQt4.QtGui import QVBoxLayout, QTextEdit
#!		edit = QTextEdit( self )
#!		layout = QVBoxLayout()
#!		layout.addWidget(edit)
#!		self.setLayout(layout)

		# define menu actions
#!		from PyQt4.QtGui import QKeySequence
#!		menu = self.menuBar().addMenu( 'File' )
#!		action = menu.addAction( 'Quit' )
#!		action.setShortcut( QKeySequence( 'Ctrl+Q' ) )

		# define custom properties
#!		self._customParam = ''

		# create connections
#!		edit.textChanged.connect( self.setCustomParam )
#!		action.triggered.connect( self.close )

		# restore settings
		self.restoreSettings()
	
	def closeEvent( self, event ):
		"""
			\remarks	[virtual]	overloaded from Window, we will record our settings from this session before closing down
			\param		event		<QEvent>
		"""
		self.recordSettings()
		
		Window.closeEvent( self, event )
			

	# define instance methods
#!	def customParam( self ):
#!		"""
#!			\remarks	returns the value for my parameter
#!			\return		<variant>
#!		"""
#!		return self._customParam

	def recordSettings( self ):
		"""
			\remarks	records settings to be used for another session
		"""
		from blurdev import prefs
		pref = prefs.find( '[class]' )
		
		# record the geometry
		pref.recordProperty( 'geom', self.geometry() )
		
		# record additional settings
#!		pref.recordProperty( 'index', self.uiSomeDDL.currentIndex() )
		
		# save the settings
		pref.save()
	
	def restoreSettings( self ):
		"""
			\remarks	restores settings that were saved by a previous session
		"""
		from blurdev import prefs
		pref = prefs.find( '[class]' )
		
		# reload the geometry
		from PyQt4.QtCore import QRect
		geom = pref.restoreProperty( 'geom', QRect() )
		if ( geom and not geom.isNull() ):
			self.setGeometry( geom )
		
		# restore additional settings
#!		self.uiSomeDDL.setCurrentIndex( pref.restoreProperty( 'index', 0 ) )

#!	def setCustomParam( self, value ):
#!		"""
#!			\remarks	sets the value for my parameter to the inputed value
#!			\param		value	<variant>
#!		"""
#!		self._customParam = value

	# define static methods
#!	@staticmethod
#!	def edit( text = '' ):
#!		import blurdev
#!		wnd = [class]( blurdev.core.activeWindow() )
#!		wnd.setCustomParam( text )
#!		wnd.show()