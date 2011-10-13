##
#	\namespace	blurdev.tools.toolscategory
#
#	\remarks	Creates the ToolsCategory class for grouping tools together
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		06/11/10
#

from PyQt4.QtCore import QObject

class ToolsCategory( QObject ):
	def __init__( self, parent ):
		QObject.__init__( self, parent )
		
		self._toolTypeLoaded 	= False
		self._toolType 			= 0
	
	def addTool( self, tool ):
		"""
			\remarks	adds the tool to the cache
		"""
		tool.setParent( self )
		self._toolType |= tool.toolType()
	
	def displayName( self ):
		name = str( self.objectName() ).split( '::' )[-1]
		return name.replace( '_', ' ' ).strip()
	
	def index( self ):
		"""
			\remarks	returns the index from which this category is instantiated
			\return		<blurdev.tools.ToolIndex>
		"""
		from toolsindex import ToolsIndex
		output = self.parent()
		while ( output and not isinstance( output, ToolsIndex ) ):
			output = output.parent()
		return output
	
	def subcategories( self ):
		"""
			\remarks	returns a list of the sub-categories for this category
			\return		<list> [ <ToolsCategory>, .. ]
		"""
		return [ child for child in self.children() if isinstance( child, ToolsCategory ) ]
	
	def tools( self, toolType = None ):
		"""
			\remarks	returns a list of the tools for this category
			\return		<list> [ <blurdev.tools.Tool>, .. ]
		"""
		from tool import Tool
		return [ child for child in self.children() if isinstance( child, Tool ) ]
		
	def toolType( self ):
		"""
			\remarks	returns the toolType for this category
		"""
		if ( not self._toolTypeLoaded ):
			self._toolTypeLoaded = True
			for cat in self.subcategories():
				self._toolType |= cat.toolType()
				
		return self._toolType
	
	@staticmethod
	def fromIndex( index, parent, xml ):
		output = ToolsCategory( parent )
		
		# load the information
		output.setObjectName( xml.attribute( 'name' ) )
		
		# cache the category
		index.cacheCategory( output )
		
		# load the child categories
		for child in xml.children():
			ToolsCategory.fromIndex( index, output, child )
		
		return output