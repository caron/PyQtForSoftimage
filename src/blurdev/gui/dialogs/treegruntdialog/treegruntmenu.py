##
#	\namespace	Treegrunt.treegruntmenu
#
#	\remarks	Defines the treegrunt item menu
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		06/16/10
#

from PyQt4.QtGui import QMenu

class TreegruntMenu( QMenu ):
	def __init__( self, parent, item ):
		QMenu.__init__( self, parent )
		
		# set custom properties
		from items import ToolItem
		self._item = item
		
		if ( parent.currentMode() == 'Favorites' ):
			self.addAction( 'Create Group...' ).triggered.connect( self.createGroup )
		
		if ( isinstance( item, ToolItem ) ):
			self.addAction( 'View User Guide...' ).triggered.connect( self.showUserGuide )
			#self.addAction( 'View SDK Guide...' ).triggered.connect( parent.showSdk )
			self.addSeparator()
			self.addAction( 'Create Macro...' ).triggered.connect( self.createMacro )
			self.addAction( 'Explore...' ).triggered.connect( self.explore )
		
		if ( parent.currentMode() == 'Favorites' and item ):
			self.addSeparator()
			self.addAction( 'Remove Item' ).triggered.connect( self.removeItem )
		
		# create the environments menu
		self.addSeparator()
		menu = self.addMenu( 'Environments...' )
		from blurdev.tools import ToolsEnvironment
		envs = list(ToolsEnvironment.environments)
		envs.sort( lambda x,y: cmp( x.isCustom(), y.isCustom() ) )
		
		first = True
		for env in envs:
			if ( env.isCustom() and first ):
				menu.addSeparator()
				first = False
			
			text = str(env.objectName())
			if ( env.isCustom() ):
				text = '(c) %s' % text
				
			action = menu.addAction( text )
			action.setCheckable( True )
			action.setChecked( env.isActive() )
		
		menu.addSeparator()
		menu.addAction( 'Rebuild Index...' ).triggered.connect( parent.rebuildIndex )
		menu.addAction( 'Reset Paths' ).triggered.connect( parent.resetPaths )
			
		menu.triggered.connect( self.switchEnvironment )
		
		# create the types menu
		menu = self.addMenu( 'Tool Types...' )
		from blurdev.tools import ToolType
		for label in ToolType.labels():
			if ( label != 'All Tools' ):
				action = menu.addAction( label )
				action.setCheckable( True )
				action.setChecked( parent.toolTypeEnabled( ToolType.valueByLabel( label ) ) )
			
		menu.triggered.connect( self.toggleToolType )
		
		self.addSeparator()
		
		self.addAction( parent.uiLoggerACT )
		self.addAction( parent.uiIdeACT )
		act = self.addAction( 'Show Dev. Toolbar' )
		act.setCheckable(True)
		act.setChecked( parent.showDevbar() )
		act.triggered.connect( parent.setShowDevbar )
	
	def currentItem( self ):
		return self._item
	
	def createGroup( self ):
		# create a group
		from PyQt4.QtGui import QInputDialog
		name, accepted = QInputDialog.getText( self, 'Create New Group', '' )
		if ( accepted ):
			from items import FavoriteGroupItem, ToolItem
			
			item = self.currentItem()
			if ( isinstance( item, ToolItem ) ):
				item = item.parent()
				
			if ( isinstance( item, FavoriteGroupItem ) ):
				newgroup = item.favoriteGroup().createGroup( name )
				item = FavoriteGroupItem( newgroup )
				item.addChild( item )
			else:
				from blurdev.tools.toolsfavoritegroup import ToolsFavoriteGroup
				newgroup = ToolsFavoriteGroup( self.parent().environment().index(), name )
				self.parent().uiToolTREE.addTopLevelItem( FavoriteGroupItem( newgroup ) )
	
	def createMacro( self ):
		import blurdev
		blurdev.core.createToolMacro( self.currentItem().tool() )
	
	def explore( self ):
		import os
		os.startfile( self.currentItem().tool().path() )
	
	def removeItem( self ):
		from PyQt4.QtGui import QMessageBox
		from items import FavoriteGroupItem, ToolItem
		
		item = self.currentItem()
		
		# remove a tool
		if ( isinstance( item, ToolItem ) ):
			if ( QMessageBox.question( self, 'Remove Tool', 'Are you sure you want to remove "%s" from your favorites?' % item.text(0), QMessageBox.Ok | QMessageBox.Cancel ) == QMessageBox.Ok ):
				# update the tool
				tool = item.tool()
				tool.setFavoriteGroup( None )
				tool.setFavorite( False )
				
				# update the item
				if ( item.parent() ):
					item.parent().takeChild( item.parent().indexOfChild( item ) )
				else:
					item.treeWidget().takeTopLevelItem( item.treeWidget().indexOfTopLevelItem( item ) )
		
		# remove a group
		elif ( isinstance( item, FavoriteGroupItem ) ):
			result = QMessageBox.question( self, 'Remove Group', 'Do you want to remove all the linked tools from your favorites as well?', QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel )
			if ( result == QMessageBox.Cancel ):
				return
				
			item.favoriteGroup().remove( unlinkTools = result == QMessageBox.Yes )
			
			# update the item
			if ( item.parent() ):
				item.parent().takeChild( item.parent().indexOfChild( item ) )
			else:
				item.treeWidget().takeTopLevelItem( item.treeWidget().indexOfTopLevelItem( item ) )
			
			self.parent().refresh()
	
	def showUserGuide( self ):
		import os
		os.startfile( 'http://redmine.blur.com/projects/pipeline/wiki/%s' % self.currentItem().tool().displayName().replace( ' ', '_' ) )
	
	def switchEnvironment( self, action ):
		self.parent().switchEnvironment( str(action.text()).replace('(c) ', '') )
	
	def toggleToolType( self, action ):
		from blurdev.tools import ToolType
		self.parent().setToolTypeEnabled( ToolType.valueByLabel( str( action.text() ) ), action.isChecked() )
		self.parent().refresh()