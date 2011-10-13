##
#	\namespace	python.blurdev.gui.widgets.previewscene
#
#	\remarks	Defines the QGraphicsScene that will be used for the PreviewWidget system
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		01/21/11
#

from PyQt4.QtCore	import pyqtSignal, QSize
from PyQt4.QtGui 	import QGraphicsScene, QColor
from blurdev.enum 	import enum
from previewlayers	import *

InteractionMode = enum( 'Navigate', 'Pencil', 'Brush', 'Selection' )

class PreviewScene( QGraphicsScene ):
	activeLayerChanged		= pyqtSignal()
	canvasSizeChanged		= pyqtSignal(QSize)
	interactionModeChanged 	= pyqtSignal(int)
	layersChanged			= pyqtSignal()
	layerRemoved			= pyqtSignal('Py_Object')

	def __init__( self, view ):
		# initialize the super class
		QGraphicsScene.__init__( self, view )
		
		# create custom properties
		self._previewWidget 	= view
		self._interactionMode	= None
		self._canvasSize		= None
		self._activeLayer		= None
		self._layers			= []
		
		self._foregroundColor	= QColor('black')
		self._backgroundColor	= QColor('white')
		self._pencilWidth		= 1
		self._brushWidth		= 5
		
		# initialize the system
		self.setBackgroundBrush( QColor( 60, 60, 60 ) )
		self.setInteractionMode( InteractionMode.Navigate )
		self.setCanvasSize( QSize( 1024, 740 ) )
		self.reset()
	
	def activeLayer( self ):
		"""
			\remarks	return the current active layer for this scene
			\return		<blurdev.gui.widgets.previewwidget.AbstractPreviewLayer>
		"""
		return self._activeLayer
	
	def addLayer( self, layer ):
		"""
			\remarks	adds a layer to the scene with the inputed name if there is not already a layer of that name
			\param		layer	<blurdev.gui.widgets.previewwidget.AbstractPreviewLayer>
			\return		<bool> success
		"""
		if ( not layer in self._layers ):
			self._layers.append( layer )
			self.setActiveLayer( layer )
			return True
		return False
	
	def backgroundColor( self ):
		return self._backgroundColor
	
	def brushWidth( self ):
		return self._brushWidth
	
	def createTextLayer( self, name = 'Text Layer', text = 'Enter Text' ):
		layer = self.createLayer( name, layerType = LayerType.Text )
		layer.setText( text )
		return layer
	
	def createLayer( self, name = 'Canvas Layer', layerType = LayerType.Canvas ):
		layer = AbstractPreviewLayer.createLayer( self, layerType, name )
		self._layers.append( layer )
		self.setActiveLayer( layer )
		self.layersChanged.emit()
		return layer
	
	def createMediaLayer( self, name = 'Media Layer', filename = '', autoResizeCanvas = False ):
		if ( not filename ):
			from PyQt4.QtGui import QFileDialog
			from blurdev import media
			filename = QFileDialog.getOpenFileName( self._previewWidget, 'Select Media File', '', media.fileTypes() )
		
		if ( not filename ):
			return None
		
		layer = self.createLayer( name, LayerType.Media )
		layer.setFilename( str(filename), autoResizeCanvas = autoResizeCanvas )
		return layer
	
	def canvasSize( self ):
		"""
			\remarks	return the current canvas size for the preview widget
			\return		<QSize>
		"""
		return self._canvasSize
	
	def clear( self ):
		"""
			\remarks	clears out all the data currently on this scene
		"""
		self.blockSignals(True)
		for layer in self._layers:
			layer.remove()
		self.blockSignals(False)
		
		self._layers = []
		self._activeLayer = None
		
		self.layersChanged.emit()
		
		# clear the scene
		QGraphicsScene.clear( self )
	
	def emitActiveLayerChanged( self ):
		if ( not self.signalsBlocked() ):
			self.activeLayerChanged.emit()
	
	def emitCanvasSizeChanged( self, size ):
		"""
			\remarks	emit the canvasSizeChanged signal for this scene provided the signals are not currently blocked
			\param		size	<QSize>
		"""
		if ( not self.signalsBlocked() ):
			self.canvasSizeChanged.emit( size )
	
	def emitLayerRemoved( self, layer ):
		if ( layer in self._layers ):
			self._layers.remove( layer )
			
		if ( not self.signalsBlocked() ):
			self.layersChanged.emit()
			self.layerRemoved.emit(layer)
	
	def emitInteractionModeChanged( self, mode ):
		"""
			\remarks	emit the interactionModeChanged signal for this scene provided the signals are not currently blocked
			\param		mode	<int>
		"""
		if ( not self.signalsBlocked() ):
			self.interactionModeChanged.emit( mode )
	
	def foregroundColor( self ):
		return self._foregroundColor
	
	def flattenedPixmap( self ):
		from PyQt4.QtGui import QPixmap, QPainter
		
		# create an output image
		output = QPixmap( self.canvasSize() )
		
		# create a painter
		painter = QPainter()
		painter.begin( output )
		
		# merge the layers down
		for layer in self.layers():
			painter.drawPixmap( 0, 0, layer.pixmap() )
		
		painter.end()
		return output
	
	def isInteractionMode( self, mode ):
		return (self._interactionMode & mode ) != 0
	
	def layerAt( self, index ):
		if ( 0 <= index and index < len(self._layers) ):
			return self._layers[index]
		return None
	
	def layerCount( self ):
		return len(self._layers)
	
	def layers( self ):
		"""
			\remarks	return a list of the current layers for this scene
			\return		<list> [ <blurdev.gui.widgets.previewwidget.AbstractPreviewLayer> layer, .. ]
		"""
		return self._layers
	
	def interactionMode( self ):
		return self._interactionMode
	
	def mousePressEvent( self, event ):
		layer = self.activeLayer()
		if ( layer ):
			layer.startEditing( event )
	
	def mouseMoveEvent( self, event ):
		layer = self.activeLayer()
		if ( layer ):
			layer.edit( event )
	
	def mouseReleaseEvent( self, event ):
		layer = self.activeLayer()
		if ( layer ):
			layer.stopEditing( event )
	
	def pen( self ):
		from PyQt4.QtCore	import Qt
		from PyQt4.QtGui 	import QRadialGradient, QPen, QBrush
		
		pen = QPen()
		pen.setColor( self.foregroundColor() )
		
		if ( self.interactionMode() == InteractionMode.Brush ):
			pen.setWidth( self.brushWidth() )
			pen.setCapStyle( Qt.RoundCap )
			pen.setJoinStyle( Qt.RoundJoin )
		else:
			pen.setWidth( self.pencilWidth() )
			pen.setCapStyle( Qt.SquareCap )
			pen.setJoinStyle( Qt.MiterJoin )
		
		return pen
	
	def previewWidget( self ):
		return self._previewWidget
	
	def renameLayer( self, oldname, newname ):
		"""
			\remarks	renames the layer at the oldname to the new name
			\param		oldname		<str>
			\param		newname		<str>
			\return		<bool> success
		"""
		layer 	= self._layers.get( str(oldname) )
		newname = str(newname)
		if ( layer and not newname in self._layers ):
			layer._name = newname
			self._layers.pop(oldname)
			self._layers[newname] = layer
			return True
		return False
	
	def reset( self ):
		# clear the current scene
		self.clear()
		
	def pencilWidth( self ):
		return self._pencilWidth
	
	def setActiveLayer( self, layer ):
		"""
			\remarks	set the active layer for the scene to the inputed layer
			\param		layer	<blurdev.gui.widgets.previewwidget.AbstractPreviewLayer>
			\return		<bool> changed
		"""
		if ( self._activeLayer == layer ):	
			return False
		elif ( self._activeLayer ):
			self._activeLayer.activate( False )
		
		self._activeLayer = layer
		
		if ( layer ):
			layer.activate( True )
		
		self.emitActiveLayerChanged()
		return True
	
	def setBackgroundColor( self, color ):
		self._backgroundColor = color
	
	def setBrushMode( self ):
		return self.setInteractionMode( InteractionMode.Brush )
	
	def setBrushWidth( self, width ):
		self._brushWidth = width
	
	def setCanvasSize( self, size ):
		"""
			\remarks	change the current canvas size for the items on the widget
			\param		size	<QSize>
			\return		<bool> changed
		"""
		if ( size == self._canvasSize ):
			return False
			
		self._canvasSize = size
		self.setSceneRect( 0, 0, size.width(), size.height() )
		
		from PyQt4.QtCore import Qt
		self._previewWidget.fitInView( 0, 0, size.width(), size.height(), Qt.KeepAspectRatio )
		self.emitCanvasSizeChanged(size)
		
		return True
		
	def setForegroundColor( self, color ):
		self._foregroundColor = color
	
	def setInteractionMode( self, mode ):
		"""
			\remarks	change the current interaction mode for the preview widget
			\param		mode	<blurdev.gui.widgets.previewwidget.InteractionMode>
			\return		<bool> changed
		"""
		if ( mode == self._interactionMode ):
			return False
		
		self._interactionMode = mode
		if ( mode == InteractionMode.Navigate ):
			self._previewWidget.setDragMode( self._previewWidget.ScrollHandDrag )
			
		elif ( mode == InteractionMode.Selection ):
			self._previewWidget.setDragMode( self._previewWidget.RubberBandDrag )
		
		else:
			self._previewWidget.setDragMode( self._previewWidget.NoDrag )
		
		self.emitInteractionModeChanged( mode )
		return True	
	
	def setNavigateMode( self ):
		return self.setInteractionMode( InteractionMode.Navigate )
	
	def setPencilMode( self ):
		return self.setInteractionMode( InteractionMode.Pencil )

	def setSelectionMode( self ):
		return self.setInteractionMode( InteractionMode.Selection )
	
	def wheelEvent( self, event ):
		"""
			\remarks	reimplements QGraphicsScene.wheelEvent to zoom in & out during wheel events
			\param		event	<QWheelEvent>
		"""
		if ( event.delta() < 0 ):
			self._previewWidget.scale( 0.9, 0.9 )
		else:
			self._previewWidget.scale( 1.1, 1.1 )