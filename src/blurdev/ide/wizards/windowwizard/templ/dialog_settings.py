##
#	\namespace	[package].[module]
#
#	\remarks	[desc::commented]
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		[date]
#

from blurdev.gui import Dialog

class [class]( Dialog ):
	def __init__( self, parent = None ):
		Dialog.__init__( self, parent )
		
		# define ui controls
#!		from PyQt4.QtGui import QHBoxLayout, QPushButton
#!		btn1 = QPushButton( self )
#!		btn1.setText( 'Ok' )
#!		btn2 = QPushButton( self )
#!		btn2.setText( 'Cancel' )
#!		layout = QVBoxLayout()
#!		layout.addWidget(btn1)
#!		layout.addWidget(btn2)
#!		self.setLayout(layout)

		# define custom properties
#!		self._customParam = 1

		# create connections
#!		btn1.clicked.connect( self.accept )		# dialogs have the accept/reject method to return true/false when running modally
#!		btn2.clicked.connect( self.reject )

		# restore settings
		self.restoreSettings()
	
	def closeEvent( self, event ):
		"""
			\remarks	[virtual]	overloaded from Dialog, we will record our settings from this session before closing down
			\param		event		<QEvent>
		"""
		self.recordSettings()
		
		Dialog.closeEvent( self, event )

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
#!	def edit( value ):
#!		import blurdev
#!		dlg = [class]( blurdev.core.activeWindow() )
#!		dlg.setCustomParam( value )
#!		if ( dlg.exec_() ):
#!			return True
#!		return False