##
#	\namespace	blurdev.gui.windows.sdkwindow.sdkwindow
#
#	\remarks	Defines the main window class for the Sdk browsing system
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		07/08/10
#

from blurdev.gui import Window

class SdkWindow( Window ):
	_instance = None
	
	def __init__( self, parent ):
		Window.__init__( self, parent )
		
		# create the custom properties
		self._filenames 		= []
		self._currentFilename	= ''
		self._loaded			= False
		
		# load the ui
		import blurdev.gui
		blurdev.gui.loadUi( __file__, self )
		
		# initialize the look
		self.uiMainSPLT.setSizes( [ 250, 600 ] )
		self.uiContentsTREE.setHeaderHidden( True )
		self.uiIndexTREE.setHeaderHidden( True )
		self.uiContentsTAB.clear()
		
		# create icons
		import os.path
		path = os.path.split( __file__ )[0]
		
		from PyQt4.QtGui import QIcon
		
		self.uiPreviousACT.setIcon( 	QIcon( path + '/img/back.png' ) )
		self.uiNextACT.setIcon( 		QIcon( path + '/img/forward.png' ) )
		self.uiHomeACT.setIcon(			QIcon( path + '/img/home.png' ) )
		self.uiFindNextACT.setIcon(		QIcon( path + '/img/find_next.png' ) )
		self.uiFindPreviousACT.setIcon(	QIcon( path + '/img/find_previous.png' ) )
		self.uiFindACT.setIcon(			QIcon( path + '/img/find.png' ) )
		self.uiSearchBTN.setIcon(		QIcon( path + '/img/search.png' ) )
		self.uiLoadACT.setIcon(			QIcon( path + '/img/load.png' ) )
		self.uiAddTabACT.setIcon( 		QIcon( path + '/img/addtab.png' ) )
		self.uiCloseTabACT.setIcon( 	QIcon( path + '/img/closetab.png' ) )
		self.uiExitACT.setIcon(			QIcon( path + '/img/quit.png' ) )
		
		# connect button actions
		self.uiBackBTN.setDefaultAction( self.uiPreviousACT )
		self.uiForwardBTN.setDefaultAction( self.uiNextACT )
		self.uiHomeBTN.setDefaultAction( self.uiHomeACT )
		
		self.uiFindNextBTN.setDefaultAction( self.uiFindNextACT )
		self.uiFindPreviousBTN.setDefaultAction( self.uiFindPreviousACT )
		
		self.uiHideFindBTN.setIcon(			QIcon( path + '/img/close.png' ) )
		
		# load the stylesheet
		f = open( path + '/stylesheet.css', 'r' )
		self._stylesheet = f.read()
		f.close()
		
		self.uiFindFRAME.hide()
		
		from PyQt4.QtGui import QIcon
		self.setWindowIcon( QIcon( path + '/img/sdk_class.png' ) )
		
		self._connect()
		
		self.restorePrefs()
		self.updateBrowserInfo()
	
	def _connect( self ):
		# connect file menu
		self.uiAddTabACT.triggered.connect( 		self.addBrowser )
		self.uiExitACT.triggered.connect(			self.close )
		self.uiLoadACT.triggered.connect(			self.loadFile )
		self.uiCloseTabACT.triggered.connect( 		self.closeBrowser )
		
		# connect the edit menu
		self.uiFindACT.triggered.connect(			self.showFind )
		self.uiFindNextACT.triggered.connect(		self.findNext )
		self.uiFindPreviousACT.triggered.connect(	self.findPrevious )
		
		# connect the go menu
		self.uiNextACT.triggered.connect(			self.goForward )
		self.uiPreviousACT.triggered.connect(		self.goBackward )
		self.uiHomeACT.triggered.connect(			self.goHome )
		self.uiNextTabACT.triggered.connect(		self.toNextBrowser )
		self.uiPreviousTabACT.triggered.connect(	self.toPreviousBrowser )
		
		# connect widgets
		self.uiContentsTREE.itemSelectionChanged.connect(		self.refreshContents )
		self.uiIndexTREE.itemSelectionChanged.connect(			self.refreshContents )
		self.uiSearchResultsTREE.itemSelectionChanged.connect(	self.refreshContents )
		
		self.uiContentsTAB.currentChanged.connect(				self.updateBrowserInfo )
		self.uiContentsTAB.customContextMenuRequested.connect( 	self.showDocumentMenu )
		
		self.uiFindTXT.textChanged.connect(					self.findText )
		self.uiFindTXT.returnPressed.connect(				self.findNext )
		
		self.uiIndexSearchTXT.textChanged.connect(			self.filterIndex )
		self.uiContentSearchTXT.textChanged.connect(		self.filterContents )
		
		self.uiSearchDDL.lineEdit().returnPressed.connect(	self.search )
		self.uiSearchBTN.clicked.connect(					self.search )
		
		self.uiHideFindBTN.clicked.connect(					self.uiFindFRAME.hide )
		self.uiCaseSensitiveCHK.clicked.connect(			self.findText )
		self.uiWholeWordsCHK.clicked.connect(				self.findText )
	
	def addBrowser( self, goToUrl = True ):
		doc = self.currentDocument()
		if ( not doc ):
			return None
			
		from blurdev.gui.windows.sdkwindow.documentbrowser import DocumentBrowser
		browser = DocumentBrowser( self, doc )
		browser.pageChanged.connect( self.updateBrowserInfo )
		
		if ( goToUrl ):
			from PyQt4.QtCore import QUrl
			browser.setSource( QUrl( doc.objectName() ) )
		
		self.uiContentsTAB.addTab( browser, doc.title() )
		self.uiContentsTAB.setCurrentIndex( self.uiContentsTAB.count() - 1 )
		self.updateBrowserInfo()
		return browser
	
	def compareSearchResults( self, a, b ):
		if ( a[0] == b[0] ):
			return cmp(a[1].title(),b[1].title())
		return cmp(b[0],a[0])
	
	def currentBrowser( self ):
		return self.uiContentsTAB.currentWidget()
	
	def currentDocument( self ):
		from blurdev.gui.windows.sdkwindow.documentitem import DocumentItem
		
		index = self.uiNavigateTAB.currentIndex()
		
		# pull from the contents tree
		if ( index == 0 ):
			item = self.uiContentsTREE.currentItem()
			if ( isinstance( item, DocumentItem ) ):
				return item.document()
				
		# pull from the index
		elif ( index == 1 ):
			item = self.uiIndexTREE.currentItem()
			if ( isinstance( item, DocumentItem ) ):
				return item.document()
		
		# pull from the search
		elif ( index == 2 ):
			item = self.uiSearchResultsTREE.currentItem()
			if ( isinstance( item, DocumentItem ) ):
				return item.document()
				
		from blurdev.gui.windows.sdkwindow.document import Document
		return Document()
	
	def currentFilename( self ):
		return self._currentFilename
	
	def closeEvent( self, event ):
		Window.closeEvent( self, event )
		self.recordPrefs()
	
	def closeBrowser( self ):
		browser = self.currentBrowser()
		if ( browser ):
			self.uiContentsTAB.removeTab(self.uiContentsTAB.currentIndex())
			browser.close()
			browser.deleteLater()
	
	def closeOtherBrowsers( self ):
		index 	= self.uiContentsTAB.currentIndex()
		for i in range( self.uiContentsTAB.count() - 1, -1, -1 ):
			if ( i == index ):
				continue
			
			widget = self.uiContentsTAB.widget(i)
			self.uiContentsTAB.removeTab(i)
			widget.close()
			widget.deleteLater()
		
	def goForward( self ):
		browser = self.currentBrowser()
		if ( browser ):
			browser.goForward()
	
	def goBackward( self ):
		browser = self.currentBrowser()
		if ( browser ):
			browser.goBackward()
	
	def goHome( self ):
		browser = self.currentBrowser()
		if ( browser ):
			browser.goHome()
	
	def htmlTemplate( self ):
		html = [ '<html><head><style>' ]
		html.append( self._stylesheet )
		html.append( '</style></head><body>%s</body></html>' )
		return '\n'.join( html )
	
	def isLoaded( self ):
		return self._loaded
	
	def findText( self ):
		browser = self.currentBrowser()
		if ( browser ):
			from PyQt4.QtGui import QTextCursor
			browser.moveCursor( QTextCursor.Start )
			self.findNext()
	
	def findNext( self ):
		browser = self.currentBrowser() 
		if ( browser ):
			from PyQt4.QtGui import QTextDocument
			
			text 	= self.uiFindTXT.text()
			flags 	= 0
			
			if ( self.uiCaseSensitiveCHK.isChecked() ):
				flags = QTextDocument.FindCaseSensitively
				
			if ( self.uiWholeWordsCHK.isChecked() ):
				if ( flags ):
					flags |= QTextDocument.FindWholeWords
				else:
					flags = QTextDocument.FindWholeWords
			
			if ( flags ):
				result = browser.find( text, flags )
			else:
				result = browser.find( text )
			
			from PyQt4.QtGui import QColor
			palette = self.uiFindTXT.palette()
			if ( text and not result ):
				clr = QColor( 'red' )
				clr.setAlpha( 100 )
				palette.setColor( palette.Base, clr )
			else:
				palette.setColor( palette.Base, self.palette().color( palette.Base ) )
			self.uiFindTXT.setPalette(palette)
	
	def findPrevious( self ):
		browser = self.currentBrowser()
		if ( browser ):
			from PyQt4.QtGui import QTextDocument
			
			text 	= self.uiFindTXT.text()
			flags 	= QTextDocument.FindBackward
			if ( self.uiCaseSensitiveCHK.isChecked() ):
				flags |= QTextDocument.FindCaseSensitively
				
			if ( self.uiWholeWordsCHK.isChecked() ):
				flags |= QTextDocument.FindWholeWords
			
			
			browser.find( text, flags )
	
	def filterContents( self ):
		text = str( self.uiContentSearchTXT.text() ).lower()
		for i in range( self.uiContentsTREE.topLevelItemCount() ):
			item = self.uiContentsTREE.topLevelItem(i)
			item.filterHidden( text )
	
	def filterIndex( self ):
		text = str( self.uiIndexSearchTXT.text() ).lower()
		for i in range( self.uiIndexTREE.topLevelItemCount() ):
			item = self.uiIndexTREE.topLevelItem(i)
			item.filterHidden( text )
	
	def loadRecent( self, action ):
		self.loadFile( action.data().toString() )
	
	def loadFile( self, filename = '' ):
		if ( not filename ):
			from PyQt4.QtGui import QFileDialog
			filename = QFileDialog.getOpenFileName( self, 'Select Sdk File', '', 'Sdk Files (*.sdk);;All Files (*.*)' )
		
		if ( filename ):
			from PyQt4.QtCore import Qt
			from PyQt4.QtGui import QApplication
			
			import os.path
			self.statusBar().showMessage( 'Loading %s...' % os.path.basename(str(filename)) )
			
			QApplication.setOverrideCursor( Qt.WaitCursor )
			
			from blurdev.gui.windows.sdkwindow.document import Document
			if ( Document.load( filename ) ):
				self._loaded = True
				if ( filename in self._filenames ):
					self._filenames.remove( filename )
					
				self._filenames.insert( 0, filename )
				self._filenames 		= self._filenames[:5]
				self._currentFilename 	= filename
				self.refresh()
				self.refreshFilenames()
			else:
				from PyQt4.QtGui import QMessageBox
				QMessageBox.critical( self, 'Error Loading File', 'Could not load %s as a valid SDK file.' % filename )
			
			QApplication.restoreOverrideCursor()
			self.statusBar().clearMessage()
	
	def loadXml( self, xml ):
		from blurdev.gui.windows.sdkwindow.document import Document
		if ( Document.parse( xml ) ):
			self._loaded = True
			self.refresh()
			self.refreshFilenames()
	
	def refresh( self ):
		self.uiIndexTREE.setUpdatesEnabled(False)
		self.uiIndexTREE.blockSignals(True)
		self.uiIndexTREE.clear()
		
		from blurdev.gui.windows.sdkwindow.document 		import Document
		from blurdev.gui.windows.sdkwindow.documentitem 	import DocumentItem
		
		documents = Document.cache.values()
		documents.sort( lambda x,y: cmp( x.title().lower(), y.title().lower() ) )
			
		# load the index
		for doc in documents:	
			self.uiIndexTREE.addTopLevelItem( DocumentItem( doc ) )
		
		self.uiIndexTREE.blockSignals(False)
		self.uiIndexTREE.setUpdatesEnabled(True)
		
		# load the contents
		self.uiContentsTREE.setUpdatesEnabled( False )
		self.uiContentsTREE.blockSignals(True)
		self.uiContentsTREE.clear()
		
		# load contents
		# load the contents
		from PyQt4.QtGui import QTreeWidgetItem
		moduleItem 	= DocumentItem( Document() )
		moduleItem.setText( 0, 'Modules & Packages' )
		classItem	= DocumentItem( Document() )
		classItem.setText( 0, 'Class Hierarchy' )
		
		hierarchy 	= Document.moduleHierarchy()
		classes		= Document.classHierarchy()
		
		for doc in hierarchy[ '__main__' ]:
			item = DocumentItem( doc )
			item.loadHierarchy( hierarchy )
			moduleItem.addChild( item )
		
		for doc in classes[ '__main__' ]:
			item = DocumentItem( doc )
			item.loadHierarchy( classes )
			classItem.addChild( item )
		
		self.uiContentsTREE.addTopLevelItem( moduleItem )
		self.uiContentsTREE.addTopLevelItem( classItem )
		
		self.uiContentsTREE.blockSignals(False)
		self.uiContentsTREE.setUpdatesEnabled(True)
	
	def refreshContents( self ):
		browser = self.currentBrowser()
		if ( not browser ):
			self.addBrowser()
		else:
			from PyQt4.QtCore import QUrl
			browser.setSource( QUrl( self.currentDocument().objectName() ) )
	
	def refreshFilenames( self ):
		from PyQt4.QtGui import QMenu
		
		filemenu 	= self.menuBar().findChild( QMenu, 'uiFileMENU' )
		oldmenu		= filemenu.findChild( QMenu, 'uiRecentFileMENU' )
		if ( oldmenu ):
			oldmenu.close()
			oldmenu.setParent( None )
			oldmenu.deleteLater()
		
		if ( self._filenames ):
			newmenu = QMenu( filemenu )
			newmenu.setObjectName( 'uiRecentFileMENU' )
			newmenu.setTitle( 'Recent Files' )
			
			import os.path
			for i in range( len( self._filenames ) ):
				action = newmenu.addAction( '%i. %s' % (i+1,os.path.basename(str(self._filenames[i]))) )
				action.setData( self._filenames[i] )
			
			filemenu.addMenu( newmenu )
			newmenu.triggered.connect( self.loadRecent )
	
	def recordPrefs( self ):
		from blurdev import prefs
		pref = prefs.find( 'sdkwindow' )
		
		pref.recordProperty( 'filenames', self._filenames )
		pref.recordProperty( 'geometry', self.geometry() )
		pref.recordProperty( 'currentFilename', self.currentFilename() )
		
		pref.save()
	
	def restorePrefs( self ):
		from blurdev import prefs
		pref = prefs.find( 'sdkwindow' )
		
		# restore the recent files
		self._filenames = pref.restoreProperty( 'filenames', [] )
		
		# restore the current filename
		filename = pref.restoreProperty( 'currentFilename' )
		if ( filename ):
			self.loadFile(filename)
		
		# restore the geometry
		geom = pref.restoreProperty( 'geometry' )
		if ( geom ):
			self.setGeometry(geom)
			
		self.refreshFilenames()
	
	def showDocumentMenu( self ):
		doc = self.currentDocument()
		if ( doc ):
			from PyQt4.QtGui import QCursor
			from documentmenu import DocumentMenu
			DocumentMenu(self,doc).exec_(QCursor.pos())
	
	def updateBrowserInfo( self ):
		browser = self.currentBrowser()
		if ( browser ):
			document = browser.currentDocument()
			if ( document ):
				self.uiContentsTAB.setTabText( self.uiContentsTAB.currentIndex(), document.title() )
				
			self.uiNextACT.setEnabled(browser.canGoForward())
			self.uiPreviousACT.setEnabled(browser.canGoBack())
			self.uiHomeACT.setEnabled(True)
		else:
			self.uiNextACT.setEnabled(False)
			self.uiPreviousACT.setEnabled(False)
			self.uiHomeACT.setEnabled(False)
	
	def search( self ):
		from blurdev.gui.windows.sdkwindow.document 		import Document
		from blurdev.gui.windows.sdkwindow.documentitem 	import DocumentItem
		
		from PyQt4.QtCore import Qt
		from PyQt4.QtGui import QApplication
		
		QApplication.setOverrideCursor( Qt.WaitCursor )
		
		self.uiSearchResultsTREE.blockSignals(True)
		self.uiSearchResultsTREE.setUpdatesEnabled(False)
		
		text = str(self.uiSearchDDL.currentText()).lower()
		
		self.uiSearchResultsTREE.clear()
		
		documents = Document.cache.values()
		results	= []
		for document in documents:
			result = document.search(text)
			if ( result ):
				results.append( (result,document) )
		
		results.sort( self.compareSearchResults )
		for result, document in results:
			self.uiSearchResultsTREE.addTopLevelItem( DocumentItem(document) )
			
		self.uiSearchResultsTREE.blockSignals(False)
		self.uiSearchResultsTREE.setUpdatesEnabled(True)
		
		QApplication.restoreOverrideCursor()
	
	def showFind( self ):
		self.uiFindFRAME.show()
		self.uiFindTXT.setFocus()
	
	def toNextBrowser( self ):
		index = self.uiContentsTAB.currentIndex() + 1
		if ( index == self.uiContentsTAB.count() ):
			index = 0
		self.uiContentsTAB.setCurrentIndex( index )
	
	def toPreviousBrowser( self ):
		index = self.uiContentsTAB.currentIndex() - 1
		if ( index < 0 ):
			index = self.uiContentsTAB.count() - 1
		self.uiContentsTAB.setCurrentIndex(index)
	
	def shutdown( self ):
		# close out of the ide system
		from PyQt4.QtCore import Qt
		
		# if this is the global instance, then allow it to be deleted on close
		if ( self == SdkWindow._instance ):
			self.setAttribute( Qt.WA_DeleteOnClose, True )
			SdkWindow._instance = None
		
		# clear out the system
		self.close()
	
	@staticmethod
	def instance( parent = None ):
		# create the instance for the logger
		if ( not SdkWindow._instance ):
			# determine default parenting
			import blurdev
			parent = None
			if ( not blurdev.core.isMfcApp() ):
				parent = blurdev.core.rootWindow()
			
			# create the logger instance
			inst = SdkWindow(parent)
			
			# protect the memory
			from PyQt4.QtCore import Qt
			inst.setAttribute( Qt.WA_DeleteOnClose, False )
			
			# cache the instance
			SdkWindow._instance = inst
			
		return SdkWindow._instance
	
	@staticmethod
	def showSdk( filename ):
		inst = SdkWindow.instance()
		inst.loadFile( filename )
		inst.show()
		
if ( __name__ == '__main__' ):
	import blurdev
	blurdev.launch( SdkWindow.instance, coreName = 'sdk' )