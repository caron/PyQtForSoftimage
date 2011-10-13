##
#	\namespace	blurdev.tools.index
#
#	\remarks	Defines the indexing system for the tools package
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		06/11/10
#

from PyQt4.QtCore import QObject

class ToolsIndex( QObject ):
	def __init__( self, environment ):
		QObject.__init__( self, environment )
		
		self._loaded			= False
		self._favoritesLoaded	= False
		self._categoryCache		= {}
		self._toolCache			= {}
	
	def baseCategories( self ):
		"""
			\remarks	returns the categories that are parented to this index
			\return		<list> [ <ToolCategory>, .. ]
		"""
		self.load()
		
		from toolscategory import ToolsCategory
		output = [ cat for cat in self._categoryCache.values() if cat.parent() == self ]
		output.sort( lambda x,y: cmp( x.objectName(), y.objectName() ) )
		return output
	
	def clear( self ):
		"""
			\remarks	clears the current cache of information
		"""
		# save the favorites first
		self.saveFavorites()
		
		# reload the data
		self._favoritesLoaded 	= False
		self._loaded 			= False
		self._categoryCache.clear()
		self._toolCache.clear()
		
		# remove all the children
		from tool 				import Tool
		from toolsfavoritegroup import ToolsFavoriteGroup
		from toolscategory		import ToolsCategory
		
		for child in self.findChildren( ToolsFavoriteGroup ):
			child.setParent( None )
			child.deleteLater()
		
		for child in self.findChildren( Tool ):
			child.setParent( None )
			child.deleteLater()
		
		for child in self.findChildren( ToolsCategory ):
			child.setParent( None )
			child.deleteLater()
	
	def categories( self ):
		"""
			\remarks	returns the current categories for this index
			\return		<list> [ <blurdev.tools.ToolsCategory>, .. ]
		"""
		self.load()
		
		output = self._categoryCache.values()
		output.sort( lambda x, y: cmp( x.objectName(), y.objectName() ) )
		return output
	
	def cacheCategory( self, category ):
		"""
			\remarks	caches the category
		"""
		self._categoryCache[ str( category.objectName() ) ] = category
	
	def cacheTool( self, tool ):
		"""
			\remarks	caches the inputed tool by its name
		"""
		self._toolCache[ str( tool.objectName() ) ] = tool
	
	def environment( self ):
		"""
			\remarks	returns this index's environment
			\return		<ToolsEnvironment>
		"""
		return self.parent()
	
	def rebuild( self ):
		"""
			\remarks	rebuilds the index from the file system
		"""
		from blurdev.XML import XMLDocument
		
		doc 	= XMLDocument()
		root 	= doc.addNode( 'index' )
		
		# walk through the hierarchy
		categories 	= root.addNode( 'categories' )
		tools		= root.addNode( 'tools' )
		legacy		= root.addNode( 'legacy' )
		
		# go through all the different language tool folders
		import glob
		for path in glob.glob( self.environment().relativePath( 'code/*/tools/*/' ) ):
			self.rebuildPath( path, categories, tools )
		
		# go through the legacy folders
		for path in glob.glob( self.environment().relativePath( 'maxscript/treegrunt/main/*/' ) ):
			self.rebuildPath( path, categories, tools, True )
		
		# save the index file
		doc.save( self.filename() )
		
		# clear the old data & reload
		self.clear()
		self.load()
		self.loadFavorites()
	
	def rebuildPath( self, path, parent, tools, legacy = False, parentCategoryId = '' ):
		"""
			\remarks	rebuilds the tool information recursively for the inputed path and tools
			\param		path				<str>
			\param		parent				<blurdev.XML.XMLElement>
			\param		tools				<blurdev.XML.XMLElement>
			\param		legacy				<bool>
			\param		parentCategoryId	<str>
		"""
		import glob
		import os.path
		foldername = os.path.normpath( path ).split( os.path.sep )[-1].strip( '_' )
		
		if ( parentCategoryId ):
			categoryId = parentCategoryId + '::' + foldername
		else:
			categoryId = foldername
		
		# create a category
		categoryIndex = parent.findChildById( categoryId )
		if ( not categoryIndex ):
			categoryIndex = parent.addNode( 'category' )
			categoryIndex.setAttribute( 'name', categoryId )
		
		# add non-legacy tools
		processed = []
		if ( not legacy ):
			paths = glob.glob( path + '/*/__meta__.xml' )
			
			from blurdev.XML import XMLDocument
			for toolPath in paths:
				toolId 		= os.path.normpath( toolPath ).split( os.path.sep )[-2]
				toolIndex 	= tools.addNode( 'tool' )
				toolIndex.setAttribute( 'name', 	toolId )
				toolIndex.setAttribute( 'category', categoryId )
				toolIndex.setAttribute( 'loc', 		self.environment().stripRelativePath( toolPath ) )
				
				# store the tool information
				doc = XMLDocument()
				if ( doc.load( toolPath ) and doc.root() ):
					toolIndex.addChild( doc.root() )
				else:
					print 'Error loading tool: ', toolPath
				
				processed.append( toolPath )
				
		# add legacy tools
		else:
			# add maxscript legacy tools
			scripts = glob.glob( path + '/*.ms' )
			for script in scripts:
				toolId = os.path.splitext( os.path.basename( script ) )[0]
				toolIndex = tools.addNode( 'legacy_tool' )
				toolIndex.setAttribute( 'category', categoryId )
				toolIndex.setAttribute( 'name', 'LegacyStudiomax::%s' % toolId )
				toolIndex.setAttribute( 'src', script )
				toolIndex.setAttribute( 'type', 'LegacyStudiomax' )
				toolIndex.setAttribute( 'icon', 'icon24.bmp' )
			
			# add python legacy tools
			scripts = glob.glob( path + '/*.py*' )
			for script in scripts:
				if ( not os.path.splitext( script )[1] == '.pyc' ):
					if ( 'External_Tools' in script ):
						typ = 'LegacyExternal'
					else:
						typ = 'LegacySoftimage'
					
					toolId = os.path.splitext( os.path.basename( script ) )[0]
					toolIndex = tools.addNode( 'legacy_tool' )
					toolIndex.setAttribute( 'category', categoryId )
					toolIndex.setAttribute( 'name', '%s::%s' % (typ,toolId) )
					toolIndex.setAttribute( 'src', script )
					toolIndex.setAttribute( 'type', typ )
					
					if ( typ == 'LegacyExternal' ):
						toolIndex.setAttribute( 'icon', 'img/icon.png' )
					else:
						toolIndex.setAttribute( 'icon', 'icon24.bmp' )
			
			# add link support
			links = glob.glob( path + '/*.lnk' )
			for link in links:
				toolId = os.path.splitext( os.path.basename( link ) )[0]
				toolIndex = tools.addNode( 'legacy_tool' )
				toolIndex.setAttribute( 'category', categoryId )
				toolIndex.setAttribute( 'name', 'LegacyExternal::%s' % toolId )
				toolIndex.setAttribute( 'src', link )
				toolIndex.setAttribute( 'type', 'LegacyExternal' )
		
		# add subcategories
		subpaths = glob.glob( path + '/*/' )
		for path in subpaths:
			if ( not (os.path.split( path )[0].endswith( '_resource' ) or ( path + '__meta__.xml' in processed )) ):
				self.rebuildPath( path, categoryIndex, tools, legacy, categoryId )
	
	def favoriteGroups( self ):
		"""
			\remarks	returns the favorites items for this index
		"""
		self.loadFavorites()
		
		from toolsfavoritegroup import ToolsFavoriteGroup
		return [ child for child in self.findChildren( ToolsFavoriteGroup ) if child.parent() == self ]
	
	def favoriteTools( self ):
		"""
			\remarks	returns all the tools that are favorited and linked
			\return		<list> [ <blurdev.tools.Tool>, .. ]
		"""
		self.loadFavorites()
		
		return [ tool for tool in self._toolCache.values() if tool.isFavorite() and tool.favoriteGroup() == None ]
		
	def filename( self ):
		"""
			\remarks	returns the filename for this index
			\return		<str>
		"""
		return self.environment().relativePath( 'code/tools.xml' )
	
	def load( self ):
		"""
			\remarks	loads the current index from the system
		"""
		if ( not self._loaded ):
			self._loaded = True
			
			from blurdev.XML import XMLDocument
			doc = XMLDocument()
			
			filename = self.filename()
			if ( doc.load( filename ) ):
				from toolscategory 	import ToolsCategory
				from tool			import Tool
				
				root 	= doc.root()
				
				# load categories
				categories	= root.findChild( 'categories' )
				if ( categories ):
					for xml in categories.children():
						ToolsCategory.fromIndex( self, self, xml )
				
				# load tools
				tools = root.findChild( 'tools' )
				if ( tools ):
					for xml in tools.children():
						Tool.fromIndex( self, xml )
	
	def loadFavorites( self ):
		if ( not self._favoritesLoaded ):
			self._favoritesLoaded = True
			
			# load favorites
			import blurdev
			from toolsfavoritegroup import ToolsFavoriteGroup
			
			from blurdev import prefs
			pref = prefs.find( 'treegrunt/%s_favorites' % (self.environment().objectName()) )
			
			children = pref.root().children()
			for child in children:
				if ( child.nodeName == 'group' ):
					ToolsFavoriteGroup.fromXml( self, self, child )
				else:
					self.findTool( child.attribute( 'id' ) ).setFavorite( True )
	
	def findCategory( self, name ):
		"""
			\remarks	returns the tool based on the inputed name, returning the default option if no tool is found
			\return		<blurdev.tools.Tool>
		"""
		self.load()
		
		return self._categoryCache.get( str( name ) )
	
	def findTool( self, name ):
		"""
			\remarks	returns the tool based on the inputed name, returning the default option if no tool is found
			\return		<blurdev.tools.Tool>
		"""
		self.load()
		
		from tool import Tool
		return self._toolCache.get( str( name ), Tool() )
	
	def findToolsByCategory( self, name ):
		"""
			\remarks	looks up the tools based on the inputed category name
			\param		name		<str>
			\return		<list> [ <blurdev.tools.Tool>, .. ]
		"""
		self.load()
		
		output = [ tool for tool in self._toolCache.values() if tool.categoryName() == name ]
		output.sort( lambda x,y: cmp( str( x.objectName().lower() ), str( y.objectName().lower() ) ) )
		return output
	
	def findToolsByLetter( self, letter ):
		"""
			\remarks	looks up tools based on the inputed letter
			\param		letter		<str>
			\return		<list> [ <blurdev.tools.Tool>, .. ]
		"""
		self.load()
		
		import re
		if ( letter == '#' ):
			regex = re.compile( '\d' )
		else:
			regex = re.compile( '[%s%s]' % (str(letter.upper()),str(letter.lower())) )
		
		output = []
		for key, item in self._toolCache.items():
			if ( regex.match( key ) ):
				output.append( item )
		
		output.sort( lambda x, y: cmp( x.name().lower(), y.name().lower() ) )
		
		return output
	
	def saveFavorites( self ):
		# load favorites
		if ( self._favoritesLoaded ):
			import blurdev
			from toolsfavoritegroup import ToolsFavoriteGroup
			
			from blurdev import prefs
			pref = prefs.find( 'treegrunt/%s_favorites' % (self.environment().objectName()) )
			root = pref.root()
			root.clear()
			
			# record the groups
			for grp in self.favoriteGroups():
				grp.toXml( root )
			
			# record the tools
			for tool in self.favoriteTools():
				node = root.addNode( 'tool' )
				node.setAttribute( 'id', tool.objectName() )
			
			pref.save()
	
	def search( self, searchString ):
		"""
			\remarks	looks up tools by the inputed search string
			\param		searchString	<str> || <QString>
			\return		<list> [ <trax.api.data.Tool>, .. ]
		"""
		self.load()
		
		import re
		expr 	= re.compile( str( searchString ).replace( '*', '.*' ), re.IGNORECASE )
		
		output = []
		for tool in self._toolCache.values():
			if ( expr.search( tool.displayName() ) ):
				output.append( tool )
		
		output.sort( lambda x,y: cmp( str(x.objectName()).lower(),str(y.objectName()).lower() ) )
		return output
	
	def tools( self ):
		return self._toolCache.values()
	
	def toolNames( self ):
		return self._toolCache.keys()