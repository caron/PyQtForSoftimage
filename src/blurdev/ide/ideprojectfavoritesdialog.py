##
#	\namespace	[FILENAME]
#
#	\remarks	[ADD REMARKS]
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		11/02/10
#

from blurdev.gui import Dialog

class IdeProjectFavoritesDialog( Dialog ):
	def __init__( self, parent ):
		Dialog.__init__( self, parent )
		
		import blurdev.gui
		blurdev.gui.loadUi( __file__, self )
		
		self.uiFavoriteTREE.customContextMenuRequested.connect( self.showMenu )
		
		self.refresh()
	
	def addFavorite( self ):
		from PyQt4.QtGui import QFileDialog
		from ideproject import IdeProject
		filename = str(QFileDialog.getOpenFileName( self, 'Blur IDE Project', IdeProject.DefaultPath, 'Blur IDE Projects (*.blurproj);;XML Files (*.xml);;All Files (*.*)' ))
		
		from ideproject import IdeProject
		if ( filename and not filename in IdeProject.Favorites ):
			IdeProject.Favorites.append( filename )
			self.refresh()
	
	def currentProject( self ):
		item = self.uiFavoriteTREE.currentItem()
		if ( not item ):
			return None
			
		from ideproject import IdeProject
		from PyQt4.QtCore import Qt
		return IdeProject.fromXml( item.data( 0, Qt.UserRole ).toString() )
	
	def refresh( self ):
		self.uiFavoriteTREE.blockSignals(True)
		self.uiFavoriteTREE.setUpdatesEnabled(False)
		self.uiFavoriteTREE.clear()
		
		from PyQt4.QtCore import Qt
		from PyQt4.QtGui import QTreeWidgetItem, QIcon
		
		import os.path
		from ideproject import IdeProject
		filenames = IdeProject.Favorites
		filenames.sort()
		
		import blurdev
		favicon = QIcon( blurdev.resourcePath( 'img/favorite.png' ) )
		
		for filename in filenames:
			name = os.path.basename( str(filename) ).split( '.' )[0]
			item = QTreeWidgetItem( [ name ] )
			item.setToolTip( 0, '<b>%s Project</b><hr><small>%s</small>' % (name,filename) )
			item.setData( 0, Qt.UserRole, filename )
			item.setIcon( 0, favicon )
			self.uiFavoriteTREE.addTopLevelItem(item)
		
		self.uiFavoriteTREE.setUpdatesEnabled(True)
		self.uiFavoriteTREE.blockSignals(False)
	
	def removeFavorite( self ):
		item = self.uiFavoriteTREE.currentItem()
		if ( not item ):
			return
			
		from ideproject import IdeProject
		from PyQt4.QtCore import Qt
		IdeProject.Favorites.remove(str(item.data(0,Qt.UserRole).toString()))
		self.refresh()
	
	def showMenu( self ):
		from PyQt4.QtGui import QMenu, QCursor
		
		menu = QMenu( self )
		menu.addAction( 'Add Favorite...' ).triggered.connect( self.addFavorite )
		menu.addSeparator()
		menu.addAction( 'Remove from Favorites' ).triggered.connect( self.removeFavorite )
		
		menu.popup( QCursor.pos() )
	
	@staticmethod
	def getProject():
		import blurdev
		dlg = IdeProjectFavoritesDialog(blurdev.core.activeWindow())
		if ( dlg.exec_() ):
			return dlg.currentProject()
		return None