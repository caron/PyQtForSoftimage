##
#	\namespace	documentitem
#
#	\remarks	[REMARKS]
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		07/08/10
#

from PyQt4.QtGui import QTreeWidgetItem

class DocumentItem( QTreeWidgetItem ):
	def __init__( self, document ):
		QTreeWidgetItem.__init__( self, [ document.title() ] )
		
		self._document = document
		self.updateIcon()
	
	def document( self ):
		return self._document
	
	def loadHierarchy( self, hierarchy ):
		title = self.document().title()
		for doc in hierarchy.get( str( self.document().objectName() ), [] ):
			child = DocumentItem( doc )
			child.setText( 0, doc.title().split( '.' )[-1] )
			child.loadHierarchy( hierarchy )
			self.addChild( child )
		
		self.updateIcon()
	
	def filterHidden( self, text ):
		# look for visible children
		childvisible = False
		for c in range( self.childCount() ):
			self.child(c).filterHidden( text )
			if ( not self.child(c).isHidden() ):
				childvisible = True
		
		if ( text == '' ):
			self.setHidden( False )
			self.setExpanded( False )
		else:
			self.setHidden( not (childvisible or text in str( self.text(0) ).lower() ) )
			self.setExpanded( True )
		
		if ( self.document().isNull() ):
			self.updateIcon()
	
	def updateIcon( self ):
		from PyQt4.QtGui import QIcon
		import os.path
		
		path = os.path.split( __file__ )[0] + '/img/'
		if ( not self.document().isNull() ):
			import inspect
			if ( self.childCount() ):
				self.setIcon( 0, QIcon( path + 'sdk_package.png' ) )
			elif ( inspect.isclass( self.document().object() ) ):
				self.setIcon( 0, QIcon( path + 'sdk_class.png' ) )
			else:
				self.setIcon( 0, QIcon( path + 'sdk_file.png' ) )
		else:
			if ( self.isExpanded() ):
				self.setIcon( 0, QIcon( path + 'folder_open.png' ) )
			else:
				self.setIcon( 0, QIcon( path + 'folder.png' ) )
		
	