##
#	\namespace	python.blurdev.gui.windows.loggerwindow.workboxwidget
#
#	\remarks	A area to save and run code past the existing session
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		03/17/11
#

from PyQt4.QtGui import QTextEdit
from PyQt4.QtCore	import QEvent, Qt
from blurdev.ide.documenteditor	import DocumentEditor
from PyQt4.QtGui import QApplication

import blurdev
class WorkboxWidget( DocumentEditor ):
	def __init__( self, parent, console = None ):
		# initialize the super class
		DocumentEditor.__init__( self, parent )
		
		self._console = console
		# define the user interface data
#! 		finish initializing the class
		
		# create custom properties
#! 		self._customProperty = ''
		
		# create connections
#! 		self.uiNameTXT.textChanged.connect( self.setCustomProperty )

	def console( self ):
		return self._console
	
	def execAll( self ):
		"""
			\remarks	reimplement the DocumentEditor.exec_ method to run this code without saving
		"""
		import __main__
		exec unicode(self.text()).replace('\r','\n') in __main__.__dict__, __main__.__dict__
	
	def execSelected( self ):
		text = unicode(self.selectedText()).replace('\r','\n')
		if ( not text ):
			line, index = self.getCursorPosition()
			text = unicode(self.text(line)).replace('\r','\n')
		
		import __main__	
		exec text in __main__.__dict__, __main__.__dict__
	
	def keyPressEvent( self, event ):
		if ( event.key() == Qt.Key_Enter ):
			self.execSelected()
		else:
			DocumentEditor.keyPressEvent( self, event )
	
	def setConsole( self, console ):
		self._console = console