##
#	\namespace	python.blurdev.gui.widgets.previewwidgetlayerswidget
#
#	\remarks	Manages layers for the PreviewWidget
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		01/24/11
#

from PyQt4.QtCore 	import Qt, QSize
from PyQt4.QtGui 	import QWidget, QTreeWidgetItem, QItemDelegate

class LayerDelegate( QItemDelegate ):
	def __init__( self, parent, size = 12):
		QItemDelegate.__init__( self, parent )
		
		import blurdev
		from PyQt4.QtGui import QPixmap
		self._checkedMap 	= QPixmap( blurdev.resourcePath( 'img/preview/visible.png' ) ).scaled( size, size )
		self._uncheckedMap 	= QPixmap()
		self._editor		= None
	
	def clearEditor( self ):
		"""
			\remarks	clears the reference to this editor
		"""
		try:
			self._editor.close()
			self._editor.deleteLater()
		except:
			pass
		
		self._editor = None
		
	def createEditor( self, parent, option, index ):
		"""
			\remarks	overloaded from QItemDelegate, creates a new editor for the inputed widget
			\param		parent	<QWidget>
			\param		option	<QStyleOptionViewItem>
			\param		index	<QModelIndex>
			\return		<QWidget> editor
		"""
		from PyQt4.QtCore 	import Qt
		from PyQt4.QtGui 	import QLineEdit
		
		# clear out the old editor
		self.clearEditor()
		self._editor = QLineEdit( parent )
		self._editor.setFocus()
		self._editor.setFocusPolicy( Qt.StrongFocus )
		
		return self._editor
	
	def checkedMap( self ):
		""" returns the checked pixmap for this delegate """
		return self._checkedMap
	
	def drawCheck( self, painter, option, rect, state ):
		""" overloaded QItemDelegate.drawCheck method to handle the drawing of the checkbox to paint the pixmaps """
		if ( rect.isValid() ):
			from PyQt4.QtCore import Qt
			if ( state == Qt.Checked ):
				painter.drawPixmap( rect.x(), rect.y(), self.checkedMap() )
			else:
				painter.drawPixmap( rect.x(), rect.y(), self.uncheckedMap() )
		
	def editor( self ):
		"""
			\remarks	returns the current editor for this delegate
			\return		<QWidget> || None
		"""
		return self._editor
	
	def uncheckedMap( self ):
		""" returns the unchecked pixmap for this delegate """
		return self._uncheckedMap
		

class LayerItem( QTreeWidgetItem ):
	def __init__( self, layer ):
		QTreeWidgetItem.__init__( self, [ '', layer.name() ] )
		self._layer = layer
		
		checked = Qt.Unchecked
		if ( layer.isVisible() ):
			checked = Qt.Checked
		
		from PyQt4.QtGui import QIcon
		import blurdev
		from previewlayers import LayerType
		if ( layer.layerType() == LayerType.Text ):
			self.setIcon( 1, QIcon( blurdev.resourcePath( 'img/preview/type.png' ) ) )
		elif ( layer.layerType() == LayerType.Media ):
			self.setIcon( 1, QIcon( blurdev.resourcePath( 'img/preview/media.png' ) ) )
		else:
			self.setIcon( 1, QIcon( blurdev.resourcePath( 'img/preview/layers.png' ) ) )
		
		self.setCheckState( 0, checked )
		self.setSizeHint( 0, QSize( 18, 18 ) )
		
	def layer( self ):
		return self._layer

class LayersWidget( QWidget ):
	def __init__( self, parent, scene ):
		# initialize the super class
		QWidget.__init__( self, parent )
		
		# load the ui
		import blurdev
		blurdev.gui.loadUi( __file__, self )
		
		from PyQt4.QtCore import Qt
		self.setWindowFlags( Qt.Tool )
		
		# create custom properties
		self._scene 	= scene
		self._editCache = None
		scene.layersChanged.connect( self.refresh )
		
		# initialize ui
		columns = [ 'Visible', 'Name' ]
		self.uiLayerTREE.setColumnCount( len(columns) )
		
		# load icons
		from PyQt4.QtGui import QIcon
		self.uiNewCanvasLayerBTN.setIcon( 	QIcon( blurdev.resourcePath( 'img/preview/add.png' ) ) )
		self.uiNewTextLayerBTN.setIcon( 	QIcon( blurdev.resourcePath( 'img/preview/type.png' ) ) )
		self.uiNewMediaLayerBTN.setIcon( 	QIcon( blurdev.resourcePath( 'img/preview/media.png' ) ) )
		self.uiRemoveBTN.setIcon( 			QIcon( blurdev.resourcePath( 'img/preview/delete.png' ) ) )
		
		# create the layer delegate
		self.uiLayerTREE.setItemDelegate( LayerDelegate( self.uiLayerTREE ) )
		
		# create the drag/drop helpers
		
		# create connections
		self.uiNewCanvasLayerBTN.clicked.connect( 	self.createLayer )
		self.uiNewTextLayerBTN.clicked.connect(		self.createTextLayer )
		self.uiNewMediaLayerBTN.clicked.connect(	self.createMediaLayer )
		self.uiRemoveBTN.clicked.connect( self.removeLayer )
		self.uiLayerTREE.itemDoubleClicked.connect( self.renameLayer )
		self.uiLayerTREE.itemSelectionChanged.connect( self.activateLayer )
		self.uiLayerTREE.itemChanged.connect( self.updateLayer )
	
	def acceptLayerRename( self ):
		if ( self._editCache ):
			item, column = self._editCache
			item.layer().setName( str(self.uiLayerTREE.itemDelegate().editor().text()) )
			self.uiLayerTREE.closePersistentEditor( item, column )
		self._editCache = None
	
	def activateLayer( self ):
		item = self.uiLayerTREE.currentItem()
		if ( item ):
			self._scene.setActiveLayer( item.layer() )
	
	def createLayer( self ):
		self._scene.createLayer()
		self.refresh()
	
	def createTextLayer( self ):
		self._scene.createTextLayer()
		self.refresh()
	
	def createMediaLayer( self ):
		self._scene.createMediaLayer()
		self.refresh()
	
	def eventFilter( self, object, event ):
		# handle a key press event
		if ( event.type() == event.KeyPress ):
			# handle a return (accept) event
			if ( event.key() in (Qt.Key_Return,Qt.Key_Enter) ):
				self.acceptLayerRename()
			
			# handle an escape (cancel) event
			elif ( event.key() == Qt.Key_Escape ):
				self.rejectLayerRename()
		
		# accept the changes when the editor is finished
		elif ( event.type() == event.Leave ):
			self.acceptLayerRename()
		
		return False
	
	def rejectLayerRename( self ):
		if ( self._editCache ):
			item, column = self._editCache
			self.uiLayerTREE.closePersistentEditor( item, column )
			
			item.setText( 1, item.layer().name() )
			
		self._editCache = None
	
	def removeLayer( self ):
		item = self.uiLayerTREE.currentItem()
		if ( item ):
			item.layer().remove()
			self.refresh()
	
	def renameLayer( self, item, column ):
		if ( column == 1 ):
			delegate = self.uiLayerTREE.itemDelegate()
			self.uiLayerTREE.openPersistentEditor( item, column )
			
			editor = delegate.editor()
			editor.setText( item.text(column) )
			editor.setSelection( 0, len(item.text(column)) )
			editor.installEventFilter( self )
			
			self._editCache = (item,column)
		else:
			self._editCache = None
		
	def refresh( self ):
		self.uiLayerTREE.blockSignals(True)
		self.uiLayerTREE.setUpdatesEnabled(False)
		
		self.uiLayerTREE.clear()
		
		layers = list( self._scene.layers() )
		layers.reverse()
		for layer in layers:
			item = LayerItem( layer )
			self.uiLayerTREE.addTopLevelItem( item )
			if ( layer.isActive() ):
				self.uiLayerTREE.setCurrentItem( item, 1 )
		
		for i in range( self.uiLayerTREE.columnCount() ):
			self.uiLayerTREE.resizeColumnToContents( i )
		
		self.uiLayerTREE.setUpdatesEnabled(True)
		self.uiLayerTREE.blockSignals(False)
	
	def show( self ):
		QWidget.show( self )
		self.refresh()
		
	def updateLayer( self, item ):
		from PyQt4.QtCore import Qt
		layer = item.layer()
		layer.setVisible( item.checkState(0) == Qt.Checked )