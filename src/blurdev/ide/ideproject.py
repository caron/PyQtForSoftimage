##
#	\namespace	blurdev.ide.ideproject
#
#	\remarks	Stores information about a project
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		08/19/10
#

from PyQt4.QtGui import QTreeWidgetItem

class IdeProjectItem( QTreeWidgetItem ):
	def __init__( self ):
		QTreeWidgetItem.__init__( self )
		
		# create custom properties
		self._filePath		= ''
		self._group			= True
		self._fileSystem	= False
		self._exclude		= [ '.svn' ]
		self._fileTypes		= '*.py;;*.pyw;;*.xml;;*.ui;;*.nsi;;*.bat;;*.schema;;*.txt;;*.blurproj'.split( ';;' )
		self._loaded		= False
		
		# set the default icon
		from PyQt4.QtGui import QIcon
		import blurdev
		self.setIcon( 0, QIcon(blurdev.resourcePath( 'img/folder.png')) )
		self.setChildIndicatorPolicy( QTreeWidgetItem.ShowIndicator )
	
	def exclude( self ):
		return self._exclude
	
	def filePath( self ):
		return self._filePath
		
	def fileInfo( self ):
		from PyQt4.QtCore 	import QFileInfo
		if ( self.isFileSystem() ):
			return QFileInfo(self.filePath())
		return QFileInfo()
	
	def fileTypes( self ):
		return self._fileTypes
	
	def isGroup( self ):
		return self._group
		
	def isFile( self ):
		from PyQt4.QtCore import QFileInfo
		return QFileInfo( self.filePath() ).isFile()
	
	def isFileSystem( self ):
		return self._fileSystem
	
	def load( self ):
		if ( self._loaded ):
			return True
		
		self._loaded = True
			
		# don't need to load custom groups
		if ( self.isGroup() ):
			return False
		
		# don't need to load files
		elif ( self.isFile() ):
			return False
		
		# only show the indicator when there are children
		self.setChildIndicatorPolicy( QTreeWidgetItem.DontShowIndicatorWhenChildless )
		
		exclude 	= self.exclude()
		fileTypes 	= self.fileTypes()
		
		folders		= []
		files		= []
		
		import os
		from PyQt4.QtCore	import QFileInfo, QDir
		
		path = str(self.filePath())
		for d in os.listdir( str(self.filePath()) ):
			# ignore directories in the exclude group
			if ( d in exclude ):
				continue
				
			fpath = os.path.join( path, d )
			finfo = QFileInfo( fpath )
			if ( finfo.isFile() ):
				ext = '*' + os.path.splitext( fpath )[1]
				if ( ext in fileTypes ):
					files.append( fpath )
			else:
				folders.append( fpath )
		
		# sort the data alphabetically
		folders.sort()
		files.sort()
		
		# load the icon provider
		from PyQt4.QtGui 	import QFileIconProvider
		iconprovider = QFileIconProvider()
		
		# add the folders
		for folder in folders:
			self.addChild( IdeProjectItem.createFolderItem( folder, iconprovider, fileTypes, exclude ) )
			
		# add the files
		for file in files:
			self.addChild( IdeProjectItem.createFileItem( file, iconprovider ) )
			
	def loadXml( self, xml ):
		self.setText( 0, 	xml.attribute( 'name' ) )
		self.setGroup( 		xml.attribute( 'group' ) != 'False' )
		self.setFilePath( 	xml.attribute( 'filePath' ) )
		
		exclude = xml.attribute( 'exclude' )
		if ( exclude ):
			self.setExclude( exclude.split( ';;' ) )
		
		ftypes = xml.attribute( 'fileTypes' )
		if ( ftypes ):
			self.setFileTypes( ftypes.split( ';;' ) )
		
		# load children
		for child in xml.children():
			self.addChild( IdeProjectItem.fromXml( child, self ) )
			
	def project( self ):
		output = self
		while ( output and not isinstance( output, IdeProject ) ):
			output = output.parent()
		return output
	
	def refresh( self ):
		# refreshing only happens on non-groups
		if ( not self.isGroup() ):
			# remove the children
			self.takeChildren()
			
			self._loaded = False
			
			# load the items
			self.load()
	
	def setGroup( self, state ):
		self._group = state
	
	def setExclude( self, exclude ):
		self._exclude = exclude
	
	def setFilePath( self, filePath ):
		self._filePath = filePath
	
	def setFileSystem( self, state ):
		self._fileSystem = state
		if ( state ):
			self._group = False
	
	def setFileTypes( self, ftypes ):
		self._fileTypes = ftypes
	
	def toXml( self, parent ):
		if ( self.isFileSystem() ):
			return
			
		xml = parent.addNode( 'folder' )
		xml.setAttribute( 'name', self.text(0) )
		xml.setAttribute( 'group', self.isGroup() )
		xml.setAttribute( 'filePath', self.filePath() )
		xml.setAttribute( 'exclude', ';;'.join( self.exclude() ) )
		xml.setAttribute( 'fileTypes', ';;'.join( self.fileTypes() ) )
		
		for c in range( self.childCount() ):
			self.child(c).toXml( xml )
	
	@staticmethod
	def createFolderItem( folder, iconprovider = None, fileTypes = [], exclude = [] ):
		from PyQt4.QtCore import QFileInfo, QDir
		
		if ( not iconprovider ):
			from PyQt4.QtGui import QFileIconProvider
			iconprovider = QFileIconProvider()
		
		item = IdeProjectItem()
		item.setText( 0, QDir( folder ).dirName() )
		item.setIcon( 0, iconprovider.icon( QFileInfo(folder) ) )
		item.setFilePath( folder )
		item.setChildIndicatorPolicy( QTreeWidgetItem.ShowIndicator )
		item.setFileSystem( True )
		item.setExclude( exclude )
		item.setFileTypes( fileTypes )
		
		return item
	
	@staticmethod
	def createFileItem( filename, iconprovider = None ):
		from PyQt4.QtCore import QFileInfo
		import os.path
		
		if ( not iconprovider ):
			from PyQt4.QtGui import QFileIconProvider
			iconprovider = QFileIconProvider()
		
		# create the item and initialize its properties
		item = IdeProjectItem()
		item.setText( 0, os.path.basename( filename ) )
		item.setFilePath( filename )
		item.setGroup(False)
		item.setFileSystem(True)
		item.setIcon( 0, iconprovider.icon( QFileInfo(filename) ) )
		item.setChildIndicatorPolicy( QTreeWidgetItem.DontShowIndicatorWhenChildless )
		
		return item
	
	@staticmethod
	def fromXml( xml, parent ):
		out = IdeProjectItem()
		out.loadXml( xml )
		return out
	
class IdeProject( IdeProjectItem ):
	__version__ = 1.0
	
	DefaultPath = 'c:/blur/dev'
	Favorites = []
	
	def __init__( self ):
		IdeProjectItem.__init__( self )
		
		from PyQt4.QtGui import QIcon
		import blurdev
		self.setIcon( 0, QIcon( blurdev.resourcePath( 'img/project.png' ) ) )
		self._filename = ''
	
	def filename( self ):
		return self._filename
	
	def save( self ):
		return self.saveAs( self.filename() )
	
	def saveAs( self, filename = '' ):
		if ( not filename ):
			from PyQt4.QtGui import QFileDialog
			filename = QFileDialog.getSaveFileName( self.window(), 'Save File as...' )
		
		if ( filename ):
			filename = str(filename)
			
			from blurdev.XML import XMLDocument
			doc = XMLDocument()
			
			root = doc.addNode( 'blurproj' )
			root.setAttribute( 'version', self.__version__ )
			
			self.toXml( root )
			
			doc.save(filename)
			return True
		return False
		
	def setFilename( self, filename ):
		self._filename = filename
	
	@staticmethod
	def fromTool( tool ):
		# see if the tool has a project file
		import os.path
		projectfile = tool.projectFile()
		if ( os.path.exists( projectfile ) ):
			return IdeProject.fromXml( projectfile )
		
		# otherwise, generate a project on the fly
		proj = IdeProject()
		proj.setText( 0, tool.objectName() )
		
		import blurdev
		
		# determine the language for the source file
		sourcefile 	= tool.sourcefile()
		ext 		= os.path.splitext(sourcefile)[1]
		
		# external files are python (usually)
		if ( ext == '.lnk' ):
			ext = '.py'
			
		import lexers
		lang 		= lexers.languageForExt( ext )
		lexerMap	= lexers.lexerMap( lang )
		
		fileTypes = [ '*.xml','*.ui','*.txt','*.ini' ]
		if ( lexerMap ):
			fileTypes += [ '*' + ftype for ftype in lexerMap.fileTypes ]
		
		# support legacy libraries & structures
		if ( tool.isLegacy() ):
			# create the library path
			libs = IdeProjectItem()
			libs.setText( 0, 'Libraries' )
			libs.setFilePath( blurdev.activeEnvironment().relativePath( 'maxscript/treegrunt/lib' ) )
			libs.setFileTypes( fileTypes )
			libs.setGroup(False)
			proj.addChild( libs )
			
			# create the resource folder
			resc = IdeProjectItem()
			resc.setText( 0, 'Resources' )
			resc.setFilePath( tool.path() )
			resc.setFileTypes( fileTypes )
			resc.setGroup(False)
			proj.addChild( resc )
			
			# create the main file
			proj.addChild( IdeProjectItem.createFileItem( sourcefile ) )
			
		else:
			if ( lang ):
				# create the library path
				libs = IdeProjectItem()
				libs.setText( 0, 'Libraries' )
				libs.setFilePath( blurdev.activeEnvironment().relativePath( 'code/%s/lib' % lang ) )
				libs.setGroup(False)
				libs.setFileTypes( fileTypes )
				proj.addChild( libs )
			
			# create the main package
			packg = IdeProjectItem()
			packg.setText( 0, tool.displayName() )
			packg.setFileTypes( fileTypes )
			packg.setFilePath( tool.path() )
			packg.setGroup(False)
			proj.addChild( packg )
		
		return proj
	
	@staticmethod
	def fromXml( filename ):
		from blurdev.XML import XMLDocument
		import os.path
		
		doc 		= XMLDocument()
		output 		= None
		filename 	= str( filename )
		
		if ( doc.load(filename) ):
			root = doc.root()
			if ( root.nodeName == 'blurproj' ):
				output = IdeProject()
				output.setFilename( filename )
				output.setText( 0, os.path.basename( filename ).split('.')[0] )
				
				# load old style
				folders = root.findChild('folders')
				if ( folders ):
					for folder in folders.children():
						output.addChild( IdeProjectItem.fromXml( folder, output ) )
					
				# load new style
				folder = root.findChild('folder')
				if ( folder ):
					output.loadXml( folder )
					
		return output