##
#	\namespace	blurdev.gui.windows.sdkwindow.documentbrowser
#
#	\remarks	Creates a browser widget class for viewing documentation information
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		07/08/10
#

from PyQt4.QtCore 	import pyqtSignal
from PyQt4.QtGui 	import QTextBrowser

class DocumentBrowser( QTextBrowser ):
	pageChanged = pyqtSignal()
	
	def __init__( self, parent, document ):
		QTextBrowser.__init__( self, parent )
		
		self._currentDocument	= None
		self._historyStack 		= []
		self._historyIndex		= 0
		
		from PyQt4.QtCore import Qt
		self.setContextMenuPolicy( Qt.CustomContextMenu )
		self.customContextMenuRequested.connect( self.showMenu )
	
	def historyIndex( self ):
		return self._historyIndex
	
	def canGoForward( self ):
		return self._historyIndex < len(self._historyStack) - 1
	
	def canGoBack( self ):
		return self._historyIndex > 0
	
	def currentDocument( self ):
		return self._currentDocument
	
	def goBackward( self ):
		self.setHistoryIndex( self.historyIndex() - 1 )
	
	def goHome( self ):
		self.setHistoryIndex( 0 )
	
	def goForward( self ):
		self.setHistoryIndex( self.historyIndex() + 1 )
	
	def goToUrl( self, url, checkForNewTab = True ):
		from PyQt4.QtCore	import Qt
		from PyQt4.QtGui 	import QApplication
		
		# go the url in a new tab
		if ( checkForNewTab and QApplication.instance().keyboardModifiers() == Qt.ControlModifier ):
			browser = self.window().addBrowser( False )
			browser.goToUrl( url, False )
			return False
			
		from blurdev.gui.windows.sdkwindow.document import Document
		try:
			docname, anchor	= str( url.toString() ).split( '#' )
		except:
			docname		= str( url.toString() )
			anchor		= None
		
		document 	= Document.find( docname )
		
		if ( not document.isNull() ):
			self.setCurrentDocument( document )
			
			template = self.window().htmlTemplate()
			
			# set the source code html
			if ( anchor and anchor.startswith( 'source' ) ):
				# record the history
				self.setHtml( template % document.sourceHtml() )
				self.scrollToAnchor( anchor )
			
			# set the list all html
			elif ( anchor and anchor == 'allmembers' ):
				# record the history
				self.setHtml( template % document.allMembersHtml() )
			
			# set the html data
			else:
				self.setHtml( template % document.html() )
				if ( anchor ):
					self.scrollToAnchor( anchor )
		
			self.pageChanged.emit()
	
	def recordHistory( self, url ):
		self._historyStack = self._historyStack[:self._historyIndex+1]
		self._historyIndex = len( self._historyStack )
		self._historyStack.append(url)
	
	def runCode( self ):
		from PyQt4.QtGui import QApplication
		self.copy()
		f = open( 'c:/temp/example.py', 'w' )
		f.write( unicode(QApplication.instance().clipboard().text()) )
		f.close()
		
		import blurdev
		blurdev.core.runScript( 'c:/temp/example.py' )
		
	def setCurrentDocument( self, document ):
		if ( document != self._currentDocument ):
			self._currentDocument = document
			self.pageChanged.emit()
	
	def setHistoryIndex( self, index ):
		if ( 0 <= index and index < len( self._historyStack ) ):
			self._historyIndex = index
			self.goToUrl( self._historyStack[index] )
			return True
		return False
	
	def setSource( self, url ):
		"""
			\remarks	[overloaded]	handles the link clicking for this browser to navigate
						to a Document - all links are links to documents
			\param		url		<QUrl>
		"""
		self.recordHistory(url)
		self.goToUrl( url )
	
	def showMenu( self ):
		from PyQt4.QtGui import QMenu, QCursor
		
		menu = QMenu( self )
		menu.addAction( 'Copy' ).triggered.connect( self.copy )
		menu.addAction( 'Run Selected' ).triggered.connect( self.runCode )
		menu.addSeparator()
		menu.addAction( 'Select All' ).triggered.connect( self.selectAll )
		
		menu.exec_(QCursor.pos())