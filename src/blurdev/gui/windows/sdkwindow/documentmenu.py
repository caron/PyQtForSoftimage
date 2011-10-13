##
#	\namespace	blurdev.gui.windows.sdkwindow.document
#
#	\remarks	Class for generating documentation about python modules or packages
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		07/08/10
#

from PyQt4.QtGui import QMenu

class DocumentMenu( QMenu ):
	def __init__( self, parent, document ):
		QMenu.__init__( self, parent )
		
		self._document = document
	
		self.addAction( 'Open in IDE' ).triggered.connect( 			self.openInIDE )
		self.addAction( 'Copy File Location' ).triggered.connect( 	self.copyFileLocation )
		self.addAction( 'Explore...' ).triggered.connect( 			self.explore )
		self.addSeparator()
		self.addAction( 'Close Tab' ).triggered.connect(				self.closeTab )
		self.addAction( 'Close All Other Tabs' ).triggered.connect(	self.closeOtherTabs )
	
	def openInIDE( self ):
		import blurdev
		blurdev.core.openScript( self._document.filename() )
	
	def copyFileLocation( self ):
		from PyQt4.QtGui import QApplication
		QApplication.clipboard().setText( self._document.filename() )
	
	def explore( self ):
		import os
		path, basename = os.path.split( self._document.filename() )
		if ( os.path.exists( path ) ):
			os.startfile(path)
	
	def closeTab( self ):
		self.parent().closeBrowser()
	
	def closeOtherTabs( self ):
		self.parent().closeOtherBrowsers()