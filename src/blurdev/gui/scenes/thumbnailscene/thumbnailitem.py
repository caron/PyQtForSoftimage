##
#	\namespace	blurdev.gui.scenes.thumbnailscene.thumbnailitem
#
#	\remarks	The ThumbnailItem is a QGraphicsRectItem that will contain and cache thumbnails for an image, allowing 
#				for fast rendering within a ThumbnailScene
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		03/31/10
#

from PyQt4.QtGui 	import QGraphicsRectItem
from blurdev.enum	import enum

ThumbnailHighlightMode = enum( 'Boxed', 'Text', 'Grayscale' )

#-------------------------------------------------------------------------------------------------------------

class ThumbnailItem( QGraphicsRectItem ):
	def __init__( self, filename ):
		QGraphicsRectItem.__init__( self )
		
		self._thumbnail			= None
		self._filename			= filename
		self._thumbGroup		= None
		self._sortData			= ''
		self._mimeText			= ''
		self._caption			= ''
		self._dragEnabled		= False
		self._highlightMode		= ThumbnailHighlightMode.Boxed
		self._customData		= {}
		
		# update the flag options
		self.setFlags( QGraphicsRectItem.ItemIsSelectable | QGraphicsRectItem.ItemIsFocusable )
	
	def caption( self ):
		return self._caption
	
	def clearThumbnail( self ):
		self._thumbnail = None
	
	def customData( self, key, default = None ):
		return self._customData.get( str(key), default )
	
	def dragEnabled( self ):
		return self._dragEnabled
	
	def highlightMode( self ):
		return self._highlightMode
	
	def paint( self, painter, option, widget ):
		from PyQt4.QtCore	import Qt, QRect
		
		# draw the thumbnail
		scene			= self.scene()
		padding 		= scene.cellPadding()
		captionPad		= scene.captionPadding()
		captionHeight	= scene.captionHeight()
		thumbsize		= scene.thumbnailSize()
		thumb 			= self.thumbnail()
		px				= ((thumbsize.width() + padding.width()) - thumb.width()) / 2
		py				= ((thumbsize.height() + padding.height()) - thumb.height()) / 2
		caption 		= self.caption()
		
		# draw highlight around the thumbnail
		if ( self.isSelected() ):
			painter.setBrush( Qt.NoBrush )
			pen = painter.pen()
			pen.setColor( scene.highlightBrush().color() )
			pen.setWidth( 2 ) 
			painter.setPen( pen )
			
			if ( self.highlightMode() & ThumbnailHighlightMode.Boxed ):
				painter.drawRect( px - 1, py - 1, thumb.width() + 2, thumb.height() + 2 )
	
		painter.drawPixmap( px, py, thumb )
		
		# draw caption
		if ( caption ):
			# draw the caption
			flags 	= int( Qt.AlignHCenter | Qt.AlignTop ) | int( Qt.TextWordWrap )
			font 	= painter.font()
			font.setPointSize( 7 )
			painter.setFont( font )
			painter.drawText( 0, thumbsize.height() + captionPad, thumbsize.width(), captionHeight, flags, caption )
			
	def mimeText( self ):
		return self._mimeText
	
	def mouseDoubleClickEvent( self, event ):
		from PyQt4.QtCore import Qt
		
		QGraphicsRectItem.mouseDoubleClickEvent( self, event )
		if ( event.button() == Qt.LeftButton ):
			self.scene().itemDoubleClicked.emit(self)
	
	def mousePressEvent( self, event ):
		from PyQt4.QtCore import Qt
		
		# emit the menu request signal
		if ( event.button() == Qt.RightButton ):
			self.scene().itemMenuRequested.emit(self)
			self.setSelected(True)
		
		else:
			QGraphicsRectItem.mousePressEvent( self, event )
			
			if ( self.dragEnabled() ):
				from PyQt4.QtCore 	import QMimeData, QPoint
				from PyQt4.QtGui 	import QDrag
				import blurdev
				
				# create the mimedata
				mimeData = QMimeData()
				mimeData.setText( self.mimeText() )
				
				# create the drag
				drag = QDrag(blurdev.core.activeWindow())
				drag.setMimeData( mimeData )
				drag.setPixmap( self.thumbnail() )
				drag.setHotSpot( QPoint( drag.pixmap().width() / 2, drag.pixmap().height() / 2 ) )
				
				drag.exec_()
	
	def setCaption( self, caption ):
		self._caption = str(caption)
		
		
		scene 			= self.scene()
		thumbsize 		= scene.thumbnailSize()
		captionPad		= scene.captionPadding()
		captionHeight	= scene.captionHeight()
		
		addtl = 0
		if ( caption ):
			addtl = captionPad + captionHeight
			
		self.setRect( 0, 0, thumbsize.width(), thumbsize.height() + addtl )
	
	def setCustomData( self, key, value ):
		self._customData[ str(key) ] = value
	
	def setDragEnabled( self, state ):
		self._dragEnabled = state
	
	def setHighlightMode( self, highlightMode ):
		self._highlightMode = highlightMode
			
	def setMimeText( self, text ):
		self._mimeText = text
	
	def setSortData( self, data ):
		self._sortData = data
	
	def setThumbnail( self, pixmap ):
		self._thumbnail = pixmap
	
	def setThumbGroup( self, thumbGroup ):
		self._thumbGroup = thumbGroup
	
	def sortData( self ):
		return self._sortData
	
	def thumbnail( self ):
		if ( not ( self._thumbnail ) ):
			from PyQt4.QtCore import Qt
			from PyQt4.QtGui import QPixmap
			
			import blurdev
			self._thumbnail = blurdev.gui.findPixmap( self._filename, thumbSize = self.scene().thumbnailSize() )
		return self._thumbnail
	
	def thumbGroup( self ):
		return self._thumbGroup
