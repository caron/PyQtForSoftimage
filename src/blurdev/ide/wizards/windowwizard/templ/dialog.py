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
#!		from PyQt4.QtGui import QHBoxLayout, QVBoxLayout, QPushButton, QTextEdit
#!		edit = QTextEdit(self)
#!		
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
#!	def edit( param = '' ):
#!		import blurdev
#!		dlg = [class]( blurdev.core.activeWindow() )
#!		dlg.setCustomParam( value )
#!		if ( dlg.exec_() ):
#!			return True
#!		return False
