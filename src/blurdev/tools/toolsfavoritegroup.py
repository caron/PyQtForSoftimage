##
#	\namespace	blurdev.tools.toolsfavoritegroup
#
#	\remarks	Creates the ToolsFavoriteGroup class for grouping favorited tools together
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		06/11/10
#

from PyQt4.QtCore import QObject

class ToolsFavoriteGroup( QObject ):
	def __init__( self, parent, name ):
		QObject.__init__( self, parent )
		self.setObjectName( name )
	
	def childGroups( self ):
		return [ grp for grp in self.findChildren( ToolsFavoriteGroup ) if grp.parent() == self ]
		
	def createGroup( self, name ):
		return ToolsFavoriteGroup( self, name )
		
	def linkedTools( self ):
		tools = self.index().tools()
		return [ tool for tool in tools if tool.favoriteGroup() == self and tool.isFavorite() ]
	
	def linkTool( self, tool ):
		tool.setFavoriteGroup( self )
	
	def index( self ):
		from toolsindex import ToolsIndex
		output = self.parent()
		while ( output and not isinstance( output, ToolsIndex ) ):
			output = output.parent()
		return output
	
	def remove( self, unlinkTools = False ):
		# unlink all the tools from this tree
		childgroups = [ self ] + list( self.findChildren( ToolsFavoriteGroup ) )
		for tool in self.index().tools():
			if ( tool.favoriteGroup() in childgroups ):
				tool.setFavoriteGroup( None )
				if ( unlinkTools ):
					tool.setFavorite( False )
		
		# remove the group
		self.setParent( None )
		self.deleteLater()
	
	def toXml( self, parent ):
		xml = parent.addNode( 'group' )
		xml.setAttribute( 'name', self.objectName() )
		
		# record the child groups
		for grp in self.childGroups():
			grp.toXml( xml )
		
		# record the tools
		for tool in self.linkedTools():
			child = xml.addNode( 'tool' )
			child.setAttribute( 'id', tool.objectName() )
		
	def unlinkTool( self, tool ):
		tool.setFavoriteGroup( None )
	
	@staticmethod
	def fromXml( index, parent, xml ):
		output = ToolsFavoriteGroup( parent, xml.attribute( 'name' ) )
		
		# load the children
		for child in xml.children():
			if ( child.nodeName == 'group' ):
				ToolsFavoriteGroup.fromXml( index, output, child )
			else:
				output.linkTool( index.findTool( child.attribute( 'id' ) ) )
		
		return output