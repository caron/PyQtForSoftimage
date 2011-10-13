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

	# define instance methods
#!	def customParam( self ):
#!		"""
#!			\remarks	returns the value for my parameter
#!			\return		<variant>
#!		"""
#!		return self._customParam

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