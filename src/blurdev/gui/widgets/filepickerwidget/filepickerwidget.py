##
#	\namespace	trax.gui.widgets.filepickerwidget.filepickerwidget
#
#	\remarks	Defines the FilePickerWidget class
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		10/06/10
#

from PyQt4.QtCore	import pyqtSignal, pyqtSlot, pyqtProperty
from PyQt4.QtGui 	import QWidget

class FilePickerWidget( QWidget ):
	filenamePicked 	= pyqtSignal( str )
	filenameChanged = pyqtSignal( str )
	filenameEdited	= pyqtSignal( str )
		
	def __init__( self, parent ):
		QWidget.__init__( self, parent )
		
		import blurdev.gui
		blurdev.gui.loadUi( __file__, self )
		
		self._caption = "Pick file..."
		self._filters = "All Files (*.*)"
		self._pickFolder = False
		self._openFile = False
		self._resolvePath = False
		self._resolved = False
			
		self.uiFilenameTXT.textChanged.connect( self.emitFilenameChanged )
		self.uiFilenameTXT.editingFinished.connect( self.emitFilenameEdited )
		self.uiFilenameTXT.editingFinished.connect( self.resolve )
		self.uiPickFileBTN.clicked.connect( self.pickPath )
		
		self.resolve()
	
	def caption( self ):
		return self._caption
	
	def emitFilenameChanged( self ):
		if ( not self.signalsBlocked() ):
			self.filenameChanged.emit( self.uiFilenameTXT.text() )
	
	def emitFilenameEdited( self ):
		if ( not self.signalsBlocked() ):
			self.filenameEdited.emit( self.uiFilenameTXT.text() )
	
	def filePath( self ):
		return self.uiFilenameTXT.text()
		
	def filters( self ):
		return self._filters
	
	def isResolved( self ):
		return self._resolved		
	
	def openFile( self ):
		return self._openFile
	
	def pickFolder( self ):
		return self._pickFolder
	
	def pickPath( self ):
		
		from PyQt4.QtGui import QFileDialog
		
		if self._pickFolder:
			filepath = QFileDialog.getExistingDirectory( self, self._caption, self.uiFilenameTXT.text() )
		elif self._openFile:
			filepath = QFileDialog.getOpenFileName( self, self._caption, self.uiFilenameTXT.text(), self._filters )
		else:
			filepath = QFileDialog.getSaveFileName( self, self._caption, self.uiFilenameTXT.text(), self._filters )

		if filepath:
			self.uiFilenameTXT.setText( filepath )
			if ( not self.signalsBlocked() ):
				self.filenamePicked.emit( filepath )
	
	def resolve( self ):
		
		if self.resolvePath():
			from PyQt4.QtGui import QPalette, QColor
			palette = self.uiFilenameTXT.palette()
			
			import os.path
			if os.path.exists( str( self.uiFilenameTXT.text() ) ):
				fg = QColor( "darkGreen" )
				bg = QColor( "green" )
				bg.setAlpha( 100 )
				self._resolved = True
			else:
				fg = QColor( "darkRed" )
				bg = QColor( "red" )
				bg.setAlpha( 100 )
				self._resolved = False
				
			palette.setColor( QPalette.Text, fg )
			palette.setColor( QPalette.Base, bg )
		else:
			palette = self.palette()
			self._resolved = False
			
		self.uiFilenameTXT.setPalette( palette )
			
	def resolvePath( self ):
		return self._resolvePath
	
	def setCaption( self, caption ):
		self._caption = caption
	
	@pyqtSlot( str )
	def setFilePath( self, filePath ):
		self.uiFilenameTXT.setText( filePath )
		self.resolve()
		
	def setFilters( self, filters ):
		self._filters = filters
	
	def setOpenFile( self, state ):
		self._openFile = state
	
	def setPickFolder( self, state ):
		self._pickFolder = state
	
	def setResolvePath( self, state ):
		self._resolvePath = state
		self.resolve()
	
	
	pyCaption		= pyqtProperty( "QString", caption, setCaption )
	pyFilters		= pyqtProperty( "QString", filters, setFilters )
	pyPickFolder	= pyqtProperty( "bool", pickFolder, setPickFolder )
	pyOpenFile		= pyqtProperty( "bool", openFile, setOpenFile )
	pyResolvePath	= pyqtProperty( "bool", resolvePath, setResolvePath )
	
	
	
	