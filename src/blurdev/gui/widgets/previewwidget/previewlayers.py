##
#	\namespace	python.blurdev.gui.widgets.previewwidget.previewlayer
#
#	\remarks	Defines the QGraphicsScene that will be used for the PreviewWidget system
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		01/21/11
#

from blurdev.enum import enum

LayerType = enum( 'Media', 'Canvas', 'Text' )

class AbstractPreviewLayer:
	layerClasses = {}
	
	def __init__( self, layerType, scene, name ):
		self._scene 		= scene
		self._name			= name
		self._visible		= True
		self._layerType		= layerType
	
	def activate( self, state ):
		return False
	
	def edit( self, event ):
		pass
	
	def isActive( self ):
		return self == self._scene.activeLayer()
	
	def isVisible( self ):	
		return self._visible
	
	def layerType( self ):
		return self._layerType
	
	def loadFrom( self, filename ):
		print 'loading from: ', filename
	
	def name( self ):
		return self._name
	
	def pixmap( self ):
		from PyQt4.QtGui import QPixmap
		return QPixmap()
	
	def remove( self ):
		return False
	
	def saveTo( self, filename ):
		print 'saving to: ', filename
	
	def scene( self ):
		return self._scene
	
	def setName( self, name ):
		self._name = name
	
	def setVisible( self, state ):
		self._visible = state
	
	def startEditing( self, event ):
		pass
	
	def stopEditing( self, event ):
		pass
	
	@staticmethod
	def createLayer( scene, layerType, name ):
		cls = AbstractPreviewLayer.layerClasses.get( layerType, CanvasLayer )
		if ( cls ):
			return cls( scene, name )

#----------------------------------------

class CanvasLayer( AbstractPreviewLayer ):
	def __init__( self, scene, name ):
		AbstractPreviewLayer.__init__( self, LayerType.Canvas, scene, name )
		
		from PyQt4.QtCore	import Qt
		from PyQt4.QtGui 	import QPixmap, QColor, QGraphicsPixmapItem
		
		# create the canvas
		self._canvas		= QPixmap( scene.canvasSize() )
		self._canvasPainter	= None
		self._canvas.fill( QColor( 0, 0, 0, 0 ) )
		
		# create the canvas item
		self._canvasItem 	= QGraphicsPixmapItem( self._canvas )
		self._canvasItem.setTransformationMode( Qt.SmoothTransformation )
		
		scene.addItem( self._canvasItem )
		scene.canvasSizeChanged.connect( self.resize )
	
	def canvas( self ):
		return self._canvas
	
	def edit( self, event ):
		if ( self._canvasPainter ):
			lp 	= event.lastScenePos()
			p	= event.scenePos()
			
#			deltax = abs(p.x() - lp.x())
#			deltay = abs(p.y() - lp.y())
			
#			if ( (deltax > 1) or (deltay > 1) ):
			self._canvasPainter.drawLine( lp, p )
			self.refresh()
			
	def fill( self, color ):
		self._canvas.fill( color )
		self.refresh()
	
	def loadFrom( self, filename ):
		from PyQt4.QtGui import QPixmap
		pixmap = QPixmap( filename )
		
		if ( not pixmap.isNull() ):
			self._canvas = pixmap
			self.refresh()
			return True
			
		return False
	
	def pixmap( self ):
		return self._canvas
	
	def refresh( self ):
		self._canvasItem.setPixmap( self._canvas )
	
	def resize( self, size ):
		self._canvas = self._canvas.scaled( size )
		self.refresh()
	
	def remove( self ):	
		self._scene.removeItem( self._canvasItem )
		self._scene.emitLayerRemoved( self )
		return True
	
	def saveTo( self, filename ):
		import os.path
		bpath = os.path.split( str(filename) )[0]
		if ( not os.path.exists( bpath ) ):
			os.mkdir( bpath )
			
		return self._canvas.save( filename )
	
	def startEditing( self, event ):
		scene = self._scene
		from previewscene import InteractionMode
		mode = scene.interactionMode()
		
		# handle drawing
		if ( mode & (InteractionMode.Pencil | InteractionMode.Brush) ):
			from PyQt4.QtGui import QPen, QPainter
			
			self._canvasPainter = QPainter()
			self._canvasPainter.begin( self._canvas )
			self._canvasPainter.setPen( scene.pen() )
			
			if ( InteractionMode.Brush == mode ):
				self._canvasPainter.setRenderHint( QPainter.Antialiasing )
				self._canvasPainter.setRenderHint( QPainter.HighQualityAntialiasing )
			
	def stopEditing( self, event ):
		if ( self._canvasPainter ):
			self._canvasPainter.end()
			self._canvasPainter = None
	
	def setVisible( self, state ):
		AbstractPreviewLayer.setVisible( self, state )
		self._canvasItem.setVisible( state )

#----------------------------------------

class MediaLayer( AbstractPreviewLayer ):
	def __init__( self, scene, name ):
		AbstractPreviewLayer.__init__( self, LayerType.Media, scene, name )
		
		from PyQt4.QtCore	import Qt
		from PyQt4.QtGui 	import QPixmap, QColor, QGraphicsPixmapItem
		
		self._filename 		= ''
		self._mediaItem 	= None

	def clear( self ):
		# clear the old item
		if ( self._mediaItem ):
			self._scene.removeItem( self._mediaItem )
			self._mediaItem = None
		
	def filename( self ):
		return self._filename
	
	def pixmap( self ):
		from PyQt4.QtGui import QGraphicsPixmapItem
		if ( isinstance( self._mediaItem, QGraphicsPixmapItem ) ):
			return self._mediaItem.pixmap()
			
		return AbstractPreviewLayer.pixmap( self )
	
	def remove( self ):
		self.clear()
		self._scene.emitLayerRemoved( self )
		return True
	
	def setFilename( self, filename, autoResizeCanvas = False ):	
		# make sure the name is actually changing
		if ( filename == self._filename ):
			return False
		
		self.clear()
		from blurdev import media
		
		# create the movie widget item
		if ( media.isMovie( filename ) ):
			print 'create movie widget item'
			
		elif ( media.isImageSequence( filename ) ):
			print 'create image sequence item'
			
		else:
			from PyQt4.QtCore import Qt
			from PyQt4.QtGui import QPixmap, QGraphicsPixmapItem, QMessageBox, QImage
			
			pixmap = QPixmap( filename )
			
			if ( pixmap.size() != self._scene.canvasSize() ):
				if ( autoResizeCanvas ):
					result = QMessageBox.Yes
				else:
					result = QMessageBox.question( None, 'Different Canvas Sizes', 'The media you are loading has a different size than the current canvas size.  Would you like to resize the canvas to fit the media?', QMessageBox.Yes | QMessageBox.No )
					
				if ( result == QMessageBox.Yes ):
					self._scene.setCanvasSize( pixmap.size() )
				else:
					pixmap = pixmap.scaled( self._scene.canvasSize(), Qt.KeepAspectRatio )
			
			self._mediaItem = QGraphicsPixmapItem( pixmap )
			self._mediaItem.setTransformationMode( Qt.SmoothTransformation )
			self._scene.addItem( self._mediaItem )
		
		return True
	
	def setVisible( self, state ):
		AbstractPreviewLayer.setVisible( self, state )
		self._mediaItem.setVisible(state)
	
#----------------------------------------

class TextLayer( AbstractPreviewLayer ):
	def __init__( self, scene, name ):
		AbstractPreviewLayer.__init__( self, LayerType.Text, scene, name )
		
		from PyQt4.QtGui import QGraphicsSimpleTextItem
		self._textItem = QGraphicsSimpleTextItem()
		scene.addItem( self._textItem )
	
	def activate( self, state ):
		from PyQt4.QtGui import QGraphicsItem
		
		if ( state ):
			self._textItem.setFlags( QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsFocusable )
		else:
			self._textItem.setFlags( QGraphicsItem.ItemIsFocusable )
	
	def font( self ):
		return self._textItem.font()
	
	def remove( self ):	
		self._scene.removeItem( self._textItem )
		self._scene.emitLayerRemoved( self )
		return True
	
	def setFont( self, font ):
		self._textItem.setFont( font )
	
	def setVisible( self, state ):
		AbstractPreviewLayer.setVisible( self, state )
		self._textItem.setVisible( state )
	
	def setText( self, text ):
		self._textItem.setText( text )
	
	def text( self ):
		return self._textItem.text()
	
#----------------------------------------

AbstractPreviewLayer.layerClasses[ LayerType.Media ] 	= MediaLayer
AbstractPreviewLayer.layerClasses[ LayerType.Canvas ] 	= CanvasLayer
AbstractPreviewLayer.layerClasses[ LayerType.Text ]		= TextLayer