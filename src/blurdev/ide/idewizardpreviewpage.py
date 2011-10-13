##
#	\namespace	blurdev.ide.idewizardpreviewpage
#
#	\remarks	This dialog allows the user to create new python classes and packages based on plugin templates
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		08/19/10
#

from PyQt4.QtGui import QWizardPage, QTreeWidgetItem

class ComponentItem( QTreeWidgetItem ):
	def __init__( self, page, xml ):
		name = page.formatText( xml.attribute( 'name' ) )
		QTreeWidgetItem.__init__( self, [ name ] )
		
		from PyQt4.QtCore 	import Qt
		from PyQt4.QtGui 	import QIcon
		import blurdev
		self.setIcon( 0, QIcon( blurdev.resourcePath( 'img/%s.png' % xml.nodeName ) ) )
		self.setCheckState( 0, Qt.Checked )
		
		self._folder		= xml.nodeName == 'folder'
		self._name			= name
		self._copyFrom 		= page.formatText( xml.attribute( 'copyFrom' ) )
		self._templateFrom 	= page.formatText( xml.attribute( 'templateFrom' ) )
		
		for child in xml.children():
			self.addChild( ComponentItem( page, child ) )
	
	def create( self, path ):
		from PyQt4.QtCore import Qt
		if ( not self.checkState(0) == Qt.Checked ):
			return
		
		import os, shutil
		path 	= str(path)
		newpath = os.path.join( path, self._name )
		
		# create a folder
		if ( self._folder ):
			if ( not os.path.exists( newpath ) ):
				try:
					os.mkdir( newpath )
				except:
					print 'Could not create folder: ', newpath
					return
		
		# copy a file
		elif ( self._copyFrom ):
			try:
				shutil.copyfile( self._copyFrom, newpath )
			except:
				print 'Error copying file from: ', self._copyFrom, ' to: ', newpath
		
		# create from a template
		elif ( self._templateFrom ):
			templ = self.page().relativePath( 'templ/%s' % self._templateFrom )
			self.page().formatFile( templ, newpath )
			
		# create the children
		for c in range( self.childCount() ):
			self.child(c).create(newpath)
	
	def expandAll( self, state ):
		self.setExpanded( state )
		for c in range( self.childCount() ):
			self.child(c).expandAll(state)
	
	def page( self ):
		return self.treeWidget().parent()

class IdeWizardPreviewPage( QWizardPage ):
	def __init__( self, parent, moduleFile ):
		QWizardPage.__init__( self, parent )
		
		# load the ui
		import blurdev.gui
		blurdev.gui.loadUi( __file__, self )
		
		self._moduleFile 	= moduleFile
		self._options		= {}
		
		self.registerField( 'components', self )
	
	def formatFile( self, input, output ):
		from blurdev import template
		return template.formatFile( input, output, self._options )
		
	def formatText( self, text ):
		from blurdev import template
		return template.formatText( text, self._options )
	
	def initializePage( self ):
		from PyQt4.QtCore import QDir
		self.uiRootPATH.setFilePath( QDir.currentPath() )
		
		self.uiComponentsTREE.blockSignals(True)
		self.uiComponentsTREE.setUpdatesEnabled(False)
		
		# generate a dictionary of options based on the fields
		field = self.field( 'options' )
		foptions = self.field( 'options' ).toPyObject()
		if ( not type(foptions) == dict ):
			foptions = {}
			
		self._options = {}
		for opt,val in foptions.items():
			self._options[str(opt)] = str(val)
		
		from blurdev.XML import XMLDocument
		doc = XMLDocument()
		
		field = str(self.field('components').toString())
		if ( not field ):
			field = 'default'
		
		# clear and repopulate the tree
		import blurdev
		self.uiComponentsTREE.clear()
		if ( doc.load( blurdev.relativePath( self._moduleFile, 'components/%s.xml' % field ) ) ):
			root = doc.root()
			
			for child in root.children():
				item = ComponentItem( self, child )
				self.uiComponentsTREE.addTopLevelItem( item )
		
		self.uiComponentsTREE.setUpdatesEnabled(True)
		self.uiComponentsTREE.blockSignals(False)
	
	def relativePath( self, relpath ):
		import blurdev
		return blurdev.relativePath( self._moduleFile, relpath )
	
	def validatePage( self ):
		if ( not self.uiRootPATH.isResolved() ):
			from PyQt4.QtGui import QMessageBox
			QMessageBox.critical( None, 'Invalid Path', 'You have to provide a valid path to create this template in' )
			return False
		
		path = self.uiRootPATH.filePath()
		
		# figure out the package location for this path
		import blurdev
		if ( not 'package' in self._options ):
			self._options[ 'package' ] = blurdev.packageForPath( path )
		
		# record the installpath for future use
		self._options[ 'installpath' ] = path
		self.setField( 'options', self._options )
		
		# create the components
		for i in range( self.uiComponentsTREE.topLevelItemCount() ):
			self.uiComponentsTREE.topLevelItem(i).create( path )
		
		return True