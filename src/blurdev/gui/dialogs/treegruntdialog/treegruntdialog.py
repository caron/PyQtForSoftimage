##
#	\namespace	Treegrunt.treegruntdialog
#
#	\remarks	The Treegrunt utility is the source tool for acdessing all other tools
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		08/07/09
#

from blurdev.gui import Dialog

class TreegruntDialog( Dialog ):
	_instance = None
	
	def __init__( self, parent = None ):
		Dialog.__init__( self, parent )
		
		import blurdev.gui
		blurdev.gui.loadUi( __file__, self )
		
		# create the header file
#		try:
#			from PyQt4.QtWebKit import QWebView as HeaderClass
#		except:
		from PyQt4.QtGui import QTextBrowser as HeaderClass
		
		self.uiHeaderTXT = HeaderClass(self)
		self.uiMainSPLT.addWidget(self.uiHeaderTXT)
		
		# create custom properties
		self._currentMode 	= 'Category'
		self._toolTypes		= 0
		self._showDevbar	= False
		
		# initialize the splitter
		self.uiMainSPLT.widget(0).layout().setContentsMargins( 0, 0, 0, 0 )
		self.uiMainSPLT.widget(1).setVisible( False )
		self.uiMainSPLT.setStretchFactor( 0, 0 )
		self.uiMainSPLT.setStretchFactor( 1, 1 )
		
		self.layout().setContentsMargins( 0, 0, 0, 0 )
		
		# set the icons
		from PyQt4.QtGui import QIcon, QPixmap
		import os.path
		imgpath = os.path.split( __file__ )[0] + '/img/'
		
		self.uiCategoryBTN.setIcon( 	QIcon( imgpath + 'folder.png' ) )
		self.uiCategoryBTN.setText( '' )
		self.uiFavoritesBTN.setIcon( 	QIcon( imgpath + 'favorites.png' ) )
		self.uiFavoritesBTN.setText( '' )
		self.uiIndexBTN.setIcon( 		QIcon( imgpath + 'alphabetical.png' ) )
		self.uiIndexBTN.setText( '' )
		self.uiSearchBTN.setIcon( 		QIcon( imgpath + 'search.png' ) )
		self.uiSearchBTN.setText( '' )
		self.uiAdvancedBTN.setIcon(		QIcon( imgpath + 'advanced.png' ) )
		self.uiAdvancedBTN.setText( '' )
		self.uiRebuildIndexBTN.setIcon( QIcon( imgpath + 'rebuild.png' ) )
		self.uiResetPathsBTN.setIcon(	QIcon( imgpath + 'reset.png' ) )
		
		self.setWindowIcon( QIcon( imgpath + 'icon.png' ) )
		
		# create the delegates
		from PyQt4.QtCore 	import Qt
		from delegates 		import GridDelegate, PixmapCheckDelegate
		
		delegate = GridDelegate( self.uiToolTREE )
		favdelegate = PixmapCheckDelegate( self.uiToolTREE, imgpath + 'favorites.png', imgpath + 'favorites_inactive.png' )
		
		# initalize the tools tree
		self.uiToolTREE.setItemDelegate( delegate )
		self.uiToolTREE.setItemDelegateForColumn( 0, favdelegate )
		self.uiToolTREE.header().setStretchLastSection( False )
		self.uiToolTREE.installEventFilter( self )
		
		# create the tool drag & drop mime data
		import blurdev
		blurdev.bindMethod( self.uiToolTREE, 'mimeData', self.mimeData )
		
		# initialize the type filters
		from blurdev.tools import ToolType
		labels = ToolType.labels()
		self.uiToolTREE.setColumnCount( len( labels ) )
		self.uiToolTREE.setHeaderLabels( [ 'Category' ] + [ '' for i in range( len( labels ) - 1 ) ] )
		for i in range( len( labels ) - 1 ):
			self.uiToolTREE.headerItem().setToolTip( 1 + i, labels[i] )
			self.uiToolTREE.headerItem().setIcon( 1 + i, QIcon( imgpath + labels[i] + '.png' ) )
			self.uiToolTREE.headerItem().setText( 1 + i, '' )
		
		# create default actions
		from PyQt4.QtGui import QKeySequence, QAction
		self.uiLoggerACT = QAction( 'Show Logger', self )
		self.uiLoggerACT.setShortcut( QKeySequence( 'F2' ) )
		self.uiLoggerACT.triggered.connect( blurdev.core.showLogger )
		self.addAction( self.uiLoggerACT )
		
		self.uiIdeACT = QAction( 'Show IDE', self )
		self.uiIdeACT.setShortcut( QKeySequence( 'Shift+F2' ) )
		self.uiIdeACT.triggered.connect( blurdev.core.showIdeEditor )
		self.addAction( self.uiIdeACT )
		
		# initialize the devbar
		from blurdev import debug
		from blurdev.tools import ToolsEnvironment
		self.uiDebugModeDDL.addItems( [ 'Disabled' ] + debug.DebugLevel.keys() )
		self.uiEnvironmentDDL.addItems( [ env.objectName() for env in ToolsEnvironment.environments ] )
		self.refreshDebugLevel()
		
		# create the connections
		self._connect()
		
		# intiiazlie the look
		self.adjustSize()
		self.setToolTypes( blurdev.core.toolTypes() )
		
		# restore the preferences
		self.restorePrefs()
		
		self.refresh()
		self.updateTitle()
	
	def _connect( self ):
		"""	create signal/slot mappings """
		import blurdev
		
		self.uiCategoryBTN.clicked.connect( 	self.setCategoryMode )
		self.uiIndexBTN.clicked.connect( 		self.setIndexMode )
		self.uiFavoritesBTN.clicked.connect(	self.setFavoritesMode )
		self.uiAdvancedBTN.toggled.connect(		self.toggleAdvanced )
		
		self.uiSearchBTN.clicked.connect(		self.search )
		self.uiSearchTXT.returnPressed.connect(	self.search )
		
		blurdev.core.environmentActivated.connect(	self.refresh )
		blurdev.core.debugLevelChanged.connect( 	self.refreshDebugLevel )
		
		self.uiToolTREE.itemExpanded.connect(	self.itemExpanded )
		self.uiToolTREE.itemCollapsed.connect(	self.itemCollapsed )
		self.uiToolTREE.customContextMenuRequested.connect(	self.showMenu )
		self.uiToolTREE.itemDoubleClicked.connect(			self.launchTool )
		self.uiToolTREE.itemChanged.connect(				self.updateTool )
		self.uiToolTREE.itemSelectionChanged.connect(		self.refreshHelp )
		
		self.uiResetPathsBTN.clicked.connect( self.resetPaths )
		self.uiRebuildIndexBTN.clicked.connect( self.rebuildIndex )
		self.uiEnvironmentDDL.currentIndexChanged.connect( self.updateCurrentEnvironment )
		self.uiDebugModeDDL.currentIndexChanged.connect( self.updateDebugLevel )
		
		# bind the drop event
		import types
		self.uiToolTREE.__dict__[ 'dropEvent' ] = types.MethodType( self.handleDropEvent.im_func, self.uiToolTREE, self.uiToolTREE.__class__ )
	
	def closeEvent( self, event ):
		self.recordPrefs()
		import blurdev
		if blurdev.core.objectName() == 'treegrunt':
			blurdev.core.logger().recordPrefs()
		Dialog.closeEvent( self, event )
	
	def currentMode( self ):
		return self._currentMode
	
	def eventFilter( self, object, event ):
		"""
			\remarks	[overloaded] resizes the tree's columns based on the resize event
			\param		object	<QObject>
			\param		event	<QEvent>
		"""
		from PyQt4.QtCore import QEvent
		
		result = Dialog.eventFilter( self, object, event )
		if ( event.type() == QEvent.Resize ):
			self.updateColumns()
		
		return result
	
	def launchTool( self, item, column ):
		from items import ToolItem
		if ( isinstance( item, ToolItem ) ):
			item.tool().exec_()
	
	def loadCategories( self ):
		# load the tool types
		from items import CategoryItem
		
		toolTypes 	= self.toolTypes()
		index 		= self.environment().index()
		for category in index.baseCategories():
			if ( category.toolType() & toolTypes ):
				self.uiToolTREE.addTopLevelItem( CategoryItem( category, toolTypes ) )
		
	def loadIndex( self ):
		from items import TreegruntItem, ToolItem
		
		toolTypes 	= self.toolTypes()
		index 		= self.environment().index()
		
		letters		= '#abcdefghijklmnopqrstuvwxyz'
		toolmap		= {}
		for c in letters:
			toolmap[ c ] = []
		
		tools = index.tools()
		tools.sort( lambda x,y: cmp( x.objectName(), y.objectName()  ) )
		for tool in tools:
			if ( tool.toolType() & toolTypes ):
				key = str( tool.displayName() )[0].lower()
				if ( key in toolmap ):
					toolmap[ key ].append( tool )
				else:
					toolmap[ '#' ].append( tool )
		
		for c in letters:
			item = TreegruntItem( c )
			for tool in toolmap[ c ]:
				item.addChild( ToolItem( tool ) )
			self.uiToolTREE.addTopLevelItem( item )
	
	def loadFavorites( self ):
		self.uiToolTREE.setDragDropMode( self.uiToolTREE.DragDrop )
		
		index = self.environment().index()
		
		# load the favorite groups
		grps 	= index.favoriteGroups()
		tools	= index.favoriteTools()
		
		grps.sort( lambda x,y: cmp( x.objectName(), y.objectName() ) )
		tools.sort( lambda x,y: cmp( x.displayName(), y.displayName() ) )
		
		from items import FavoriteGroupItem, ToolItem
		for grp in grps:
			item = FavoriteGroupItem( grp )
			self.uiToolTREE.addTopLevelItem( item )
		
		# load the favorite tools
		for tool in tools:
			item = ToolItem( tool )
			self.uiToolTREE.addTopLevelItem( item )
	
	def loadSearch( self ):
		self.uiToolTREE.blockSignals( True )
		self.uiToolTREE.setUpdatesEnabled( False )
		self.uiToolTREE.clear()
		
		toolTypes 	= self.toolTypes()
		results 	= [ tool for tool in self.environment().index().search( self.uiSearchTXT.text() ) if ( tool.toolType() & toolTypes ) ]
		
		self.uiToolTREE.setRootIsDecorated( False )
		self.uiToolTREE.headerItem().setText( 0, 'Search (%i tools found)' % len( results ) )
		
		results.sort( lambda x,y: cmp( x.objectName(), y.objectName() ) )
		from items import ToolItem
		for tool in results:
			self.uiToolTREE.addTopLevelItem( ToolItem( tool ) )
		
		self.uiToolTREE.blockSignals( False )
		self.uiToolTREE.setUpdatesEnabled( True )
		
	def environment( self ):
		from blurdev.tools import ToolsEnvironment
		return ToolsEnvironment.activeEnvironment()
	
	def handleDropEvent( tree, event ):
		drag = tree.currentItem()
		drop = tree.itemAt( event.pos() )
				
		from items import FavoriteGroupItem, ToolItem
		
		# cannot drop a group to a tool, so attempt to drop onto its parent
		if ( isinstance( drop, ToolItem ) ):
			drop = drop.parent()
			
		# make sure that we are not trying to drag and drop onto ourselves, or that the parent is already selected
		if ( drag and drop and (drag == drop or drag.parent() == drop) ):
			return
		
		# drag a group item
		if ( isinstance( drag, FavoriteGroupItem ) ):
			# drag one group onto another
			if ( isinstance( drop, FavoriteGroupItem ) ):
				drag.favoriteGroup().setParent( drop.favoriteGroup().parent() )
				if ( drag.parent() ):
					drag.parent().takeChild( drag.parent().indexOfChild( drag ) )
				else:
					tree.takeTopLevelItem( tree.indexOfTopLevelItem( drag ) )
				drop.addChild( drag )
			
			# drag a group onto the root
			else:
				drag.favoriteGroup().setParent( tree.window().environment().index() )
				if ( drag.parent() ):
					drag.parent().takeChild( drag.parent().indexOfChild( drag ) )
				else:
					tree.takeTopLevelItem( tree.indexOfTopLevelItem( drag ) )
				tree.addTopLevelItem( drag )
		
		# drag a tool item
		elif ( isinstance( drag, ToolItem ) ):
			# drag a tool onto a group
			if ( isinstance( drop, FavoriteGroupItem ) ):
				drag.tool().setFavoriteGroup( drop.favoriteGroup() )
				if ( drag.parent() ):
					drag.parent().takeChild( drag.parent().indexOfChild( drag ) )
				else:
					tree.takeTopLevelItem( tree.indexOfTopLevelItem( drag ) )
				drop.addChild( drag )
			else:
				drag.tool().setFavoriteGroup( None )
				if ( drag.parent() ):
					drag.parent().takeChild( drag.parent().indexOfChild( drag ) )
				else:
					tree.takeTopLevelItem( tree.indexOfTopLevelItem( drag ) )
				tree.addTopLevelItem( drag )
	
	def itemExpanded( self, item ):
		from PyQt4.QtCore import Qt
		from PyQt4.QtGui import QApplication
		
		if ( QApplication.instance().keyboardModifiers() == Qt.ControlModifier ):
			item.expandAll( True )
		else:
			item.updateIcon()
		
	def itemCollapsed( self, item ):
		from PyQt4.QtCore import Qt
		from PyQt4.QtGui import QApplication
		
		if ( QApplication.instance().keyboardModifiers() == Qt.ControlModifier ):
			item.expandAll( False )
		else:
			item.updateIcon()
	
	def mimeData( tree, treeItems ):
		from items import ToolItem
		from PyQt4.QtCore import QMimeData
		if ( treeItems and isinstance( treeItems[0], ToolItem ) ):
			data = QMimeData()
			data.setText( 'Tool::%s' % treeItems[0].tool().objectName() )
			return data
		return None
	
	def rebuildIndex( self ):
		from PyQt4.QtGui import QMessageBox
		if ( QMessageBox.question( self, 'Rebuild Index', 'This will take a few seconds to serach your %s environment for tools.  Continue?' % self.environment().objectName(), QMessageBox.Yes | QMessageBox.No ) == QMessageBox.Yes ):
			self.environment().index().rebuild()
			self.refresh()
	
	def resetPaths( self ):
		import blurdev
		blurdev.activeEnvironment().resetPaths()
	
	def refreshDebugLevel( self ):
		from blurdev import debug
		index = self.uiDebugModeDDL.findText(debug.DebugLevel.keyByValue(debug.debugLevel()))
		if ( index < 0 ):
			index = 0
			
		self.uiDebugModeDDL.blockSignals(True)
		self.uiDebugModeDDL.setCurrentIndex( index )
		self.uiDebugModeDDL.blockSignals(False)
	
	def refresh( self ):
		mode = self.currentMode()
		
		# make sure the favorites are loaded
		env = self.environment()
		env.index().loadFavorites()
		
		self.uiEnvironmentDDL.blockSignals(True)
		self.uiEnvironmentDDL.setCurrentIndex(self.uiEnvironmentDDL.findText(env.objectName()))
		self.uiEnvironmentDDL.blockSignals(False)
		
		self.updateTitle()
		
		self.uiToolTREE.blockSignals( True )
		self.uiToolTREE.setUpdatesEnabled( False )
		self.uiToolTREE.clear()
		self.uiToolTREE.headerItem().setText( 0, mode )
		self.uiToolTREE.setRootIsDecorated( True )
		self.uiToolTREE.setDragDropMode( self.uiToolTREE.DragOnly )
		
		from blurdev.tools.toolheader import ToolHeader
		self.uiHeaderTXT.setHtml( ToolHeader.blankHeader() )
		
		if ( mode == 'Category' ):
			self.loadCategories()
		elif ( mode == 'Index' ):
			self.loadIndex()
		elif ( mode == 'Favorites' ):
			self.loadFavorites()
		else:
			self.loadSearch()
		
		self.uiToolTREE.blockSignals( False )
		self.uiToolTREE.setUpdatesEnabled( True )
	
	def refreshHelp( self ):
		if ( self.uiHeaderTXT.isVisible() ):
			item = self.uiToolTREE.currentItem()
			from items import ToolItem
			from blurdev.tools.toolheader import ToolHeader
			
			if ( item and isinstance( item, ToolItem ) ):
				self.uiHeaderTXT.setHtml( item.tool().header().html() )
			else:
				self.uiHeaderTXT.setHtml( ToolHeader.blankHeader() )
	
	def recordPrefs( self ):
		import blurdev
		from blurdev import prefs
		pref = prefs.find( 'treegrunt/interface' )
		
		pref.recordProperty( 'advanced', self.uiAdvancedBTN.isChecked() )
		pref.recordProperty( 'search', self.uiSearchTXT.text() )
		pref.recordProperty( 'mode', self.currentMode() )
		pref.recordProperty( 'geom', self.geometry() )
		pref.recordProperty( 'sizes', self.uiMainSPLT.sizes() )
		pref.recordProperty( 'showDevelopment', self._showDevbar )
		
		pref.save()
		
		# record the favorites
		self.environment().index().saveFavorites()
	
	def restorePrefs( self ):
		import blurdev
		from blurdev import prefs
		pref = prefs.find( 'treegrunt/interface' )
		
		self.uiAdvancedBTN.setChecked( pref.restoreProperty( 'advanced', False ) )
		self.uiSearchTXT.setText( pref.restoreProperty( 'search', '' ) )
		self.setCurrentMode( pref.restoreProperty( 'mode', self.currentMode() ) )
		self.setShowDevbar( pref.restoreProperty( 'showDevelopment', False ) )
		
		if ( self.currentMode() == 'Search' ):
			self.loadSearch()
		
		# update ui items
		geom = pref.restoreProperty( 'geom' )
		if ( geom ):
			self.setGeometry( pref.restoreProperty( 'geom' ) )
			
		sizes = pref.restoreProperty( 'sizes' )
		if ( sizes ):
			self.uiMainSPLT.setSizes( sizes )
	
	def search( self ):
		self.setCurrentMode( 'Search' )
		self.loadSearch()
	
	def setCategoryMode( self ):
		self.setCurrentMode( 'Category' )
	
	def setCurrentMode( self, mode ):
		self.uiCategoryBTN.setChecked( 		mode == 'Category' )
		self.uiIndexBTN.setChecked( 		mode == 'Index' )
		self.uiFavoritesBTN.setChecked( 	mode == 'Favorites' )
		
		if ( not self._currentMode == mode ):
			self._currentMode = mode
			self.refresh()
	
	def setFavoritesMode( self ):
		self.setCurrentMode( 'Favorites' )
	
	def setIndexMode( self ):
		self.setCurrentMode( 'Index' )
	
	def updateColumns( self ):
		# Update the icon columns to stretch through the tree
		w 	= self.uiToolTREE.width()
		cw 	= 4
		
		# encorporate the scroll bar visibility
		if ( self.uiToolTREE.verticalScrollBar().isVisible() ):
			cw += self.uiToolTREE.verticalScrollBar().width()
		
		# calculate the total number of items
		for i in range( 1, self.uiToolTREE.columnCount() ):
			self.uiToolTREE.setColumnWidth( i, 25 )
			if ( not self.uiToolTREE.header().isSectionHidden( i ) ):
				cw += 25
		
		self.uiToolTREE.setColumnWidth( 0, w - cw )
	
	def updateTitle( self ):
		import blurdev, blurdev.version
		self.setWindowTitle( 'Treegrunt - %s Environment - %s' % (blurdev.activeEnvironment().objectName(),blurdev.version.toString()) )
	
	def updateTool( self, item ):
		from PyQt4.QtGui import QMessageBox
		
		from items import ToolItem
		if ( isinstance( item, ToolItem ) ):
			from PyQt4.QtCore import Qt
			item.tool().setFavorite( item.checkState(0) == Qt.Checked )
	
	def setShowDevbar( self, state = True ):
		self._showDevbar = state
		self.uiDevelopmentFRAME.setVisible(state)
	
	def showDevbar( self ):
		return self._showDevbar
	
	def show( self ):
		Dialog.show( self )
		
		# make sure we mark this as not delete on close
		from PyQt4.QtCore import Qt
		self.setAttribute( Qt.WA_DeleteOnClose, False )
		
		# refresh the information
		self.uiSearchTXT.setFocus()
		self.uiSearchTXT.selectAll()
	
	def showMenu( self, point ):
		from treegruntmenu 	import TreegruntMenu
		from PyQt4.QtGui 	import QCursor
		
		item = self.uiToolTREE.itemAt( point )
		TreegruntMenu( self, item ).popup( QCursor.pos() )
	
	def showSdk( self ):
		import os.path
		from items import ToolItem
		item = self.uiToolTREE.currentItem()
		
		# look up the documentation for the selected tool
		if ( item and isinstance( item, ToolItem ) ):
			if ( os.path.splitext( item.tool().sourcefile() )[1].startswith( '.py' ) ):
				loc 	= os.path.split( item.tool().sourcefile() )[0]
				name 	= item.tool().objectName()
			else:
				from PyQt4.QtGui import QMessageBox
				QMessageBox.critical( self, 'Cannot Create SDK', 'The SDK viewer can only work on Python files.' )
				return
		else:
			return
		
		from blurdev.gui.windows.sdkwindow.document import Document
		Document.cache.clear()
		
		import blurdev
		browser = blurdev.core.sdkBrowser(self)
		browser.loadXml( '<sdk version="1.0"><module loc="%s" name="%s"/></sdk>' % (loc, name) )
		browser.show()
	
	def shutdown( self ):
		# close out of the ide system
		from PyQt4.QtCore import Qt
		
		# allow the global instance to be cleared
		if ( self == TreegruntDialog._instance ):
			TreegruntDialog._instance = None
			self.setAttribute( Qt.WA_DeleteOnClose, True )
			
		self.close()
	
	def setToolTypes( self, toolTypes ):
		self._toolTypes = toolTypes
		
		# update the visible types in the tree
		from blurdev.tools import ToolType
		for i in range( 1, self.uiToolTREE.columnCount() ):
			value = ToolType.valueByLabel( self.uiToolTREE.headerItem().toolTip( i ) )
			self.uiToolTREE.header().setSectionHidden( i, (toolTypes & value) == 0 )
		
		self.updateColumns()
	
	def setToolTypeEnabled( self, ttype, state = True ):
		if ( state ):
			self.setToolTypes( self.toolTypes() | ttype )
		else:
			self.setToolTypes( self.toolTypes() ^ ttype )
	
	def switchEnvironment( self, text ):
		from blurdev.tools import ToolsEnvironment
		
		# update the environment from the ui
		curr 	= ToolsEnvironment.activeEnvironment()
		envname = str(text)
		if ( envname != curr.objectName() ):
			# save the current settings
			curr.index().saveFavorites()
			
			# switch to the new environment
			env = ToolsEnvironment.findEnvironment( envname )
			env.setActive()
	
	def toggleAdvanced( self, state ):
		self.setUpdatesEnabled( False )
		
		# retain the width of the tree as it is
		width = self.uiMainSPLT.widget(0).width()
		
		self.uiMainSPLT.widget(1).setVisible( state )
		
		if ( not state ):
			self.resize( width, self.height() )
		else:
			self.resize( width + 600, self.height() )
			self.uiMainSPLT.setSizes( [ width, self.width() - width ] )
			
		self.setUpdatesEnabled( True )
	
	def toolTypes( self ):
		return self._toolTypes
	
	def toolTypeEnabled( self, ttype ):
		return ( ttype & self.toolTypes() ) != 0
	
	def updateCurrentEnvironment( self ):
		self.switchEnvironment( self.uiEnvironmentDDL.currentText() )
	
	def updateDebugLevel( self ):
		from blurdev import debug
		debug.setDebugLevel( debug.DebugLevel.value(str(self.uiDebugModeDDL.currentText())) )
	
	@staticmethod
	def instance( parent ):
		# create the instance for the logger
		if ( not TreegruntDialog._instance ):
			# determine default parenting
			import blurdev
			parent = None
			if ( not blurdev.core.isMfcApp() ):
				parent = blurdev.core.rootWindow()
			
			# create the logger instance
			inst = TreegruntDialog(parent)
			
			# protect the memory
			from PyQt4.QtCore import Qt
			inst.setAttribute( Qt.WA_DeleteOnClose, False )
			
			# cache the instance
			TreegruntDialog._instance = inst
			
		return TreegruntDialog._instance
