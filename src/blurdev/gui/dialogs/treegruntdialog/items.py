##
#	\namespace	Treegrunt.items
#
#	\remarks	Defines all the treewidgetitems that will be used by the treegrunt
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		06/16/10
#

from PyQt4.QtGui import QTreeWidgetItem

#-------------------------------------------------------------------------------------------------------------

class TreegruntItem( QTreeWidgetItem ):
	def __init__( self, name ):
		QTreeWidgetItem.__init__( self, [ name ] )
		
		# Set the sizing hint
		from PyQt4.QtCore import QSize
		self.setSizeHint( 0, QSize( 150, 20 ) )
		
		# Set the icon
		from PyQt4.QtGui import QIcon
		import os.path
		self.setIcon( 0, QIcon( os.path.split( __file__ )[0] + '/img/folder.png' ) )
		
	def expandAll( self, state = True ):
		self.setExpanded( state )
		self.updateIcon() 
		
		# expand all children recursively
		for c in range( self.childCount() ):
			self.child(c).expandAll( state )
	
	def findItem( self, name ):
		for c in range( self.childCount() ):
			item = self.child(c)
			if ( item.text(0) == name ):
				return item
		return None
	
	def isTool( self ):
		return False
	
	def updateIcon( self ):
		# Update the icon
		from PyQt4.QtGui import QIcon
		import os.path
		
		if ( self.isExpanded() ):
			self.setIcon( 0, QIcon( os.path.split( __file__ )[0] + '/img/folder_open.png' ) )
		else:
			self.setIcon( 0, QIcon( os.path.split( __file__ )[0] + '/img/folder.png' ) )

#-------------------------------------------------------------------------------------------------------------

class CategoryItem( TreegruntItem ):
	def __init__( self, category, toolTypes = 0 ):
		TreegruntItem.__init__( self, category.displayName() )
		
		self._category		= category
		
		# load subcategories
		categories = category.subcategories()
		categories.sort( lambda x,y: cmp( x.objectName(), y.objectName() ) )
		for subcategory in categories:
			if ( subcategory.toolType() & toolTypes ):
				self.addChild( CategoryItem( subcategory, toolTypes ) )
		
		# load the tools
		tools = category.tools()
		tools.sort( lambda x,y: cmp( x.objectName(), y.objectName() ) )
		for tool in tools:
			if ( tool.toolType() & toolTypes ):
				self.addChild( ToolItem( tool ) )
	
	def category( self ):
		return self._category

#-------------------------------------------------------------------------------------------------------------

class FavoriteGroupItem( TreegruntItem ):
	def __init__( self, favoriteGroup ):
		TreegruntItem.__init__( self, favoriteGroup.objectName() )
		
		self._favoriteGroup = favoriteGroup
		
		# load subgroups
		groups = favoriteGroup.childGroups()
		groups.sort( lambda x,y: cmp( x.objectName(), y.objectName() ) )
		for grp in groups:
			item = FavoriteGroupItem( grp )
			self.addChild( item )
		
		# load tools
		tools = favoriteGroup.linkedTools()
		tools.sort( lambda x,y: cmp( x.displayName(), y.displayName() ) )
		for tool in tools:
			item = ToolItem( tool )
			self.addChild( item )
	
	def favoriteGroup( self ):
		return self._favoriteGroup

#-------------------------------------------------------------------------------------------------------------

class ToolItem( TreegruntItem ):
	iconCache = {}
	
	def __init__( self, tool ):
		TreegruntItem.__init__( self, tool.displayName() )
		
		self._tool = tool
		
		# create the icon
		from PyQt4.QtGui import QIcon, QPixmap

		self.setIcon( 0, QIcon( tool.icon() ) )
		
		# update possible tool type options
		from PyQt4.QtCore 	import Qt
		from blurdev.tools 	import ToolType
		
		if ( tool.isFavorite() ):
			self.setCheckState( 0, Qt.Checked )
		else:
			self.setCheckState( 0, Qt.Unchecked )
		
		labels = ToolType.labels()
		for i in range( len( labels ) - 1 ):
			if ( ToolType.valueByLabel( labels[i] ) & tool.toolType() ):
				self.setCheckState( i + 1, Qt.Checked )
	
	def tool( self ):
		return self._tool
	
	def isTool( self ):
		return True
	
	def updateIcon( self ):
		pass