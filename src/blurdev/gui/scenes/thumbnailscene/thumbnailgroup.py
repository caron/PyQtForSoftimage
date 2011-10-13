##
#	\namespace	blurdev.gui.scenes.thumbnailscene.thumbnailgroup
#
#	\remarks	The ThumbnailGroup is a QGraphicsRectItem that will contain and cache thumbnails for an image, allowing 
#				for fast rendering within a ThumbnailScene
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		03/31/10
#

from PyQt4.QtGui 	import QGraphicsRectItem

#-------------------------------------------------------------------------------------------------------------

class ThumbnailGroup( QGraphicsRectItem ):
	def __init__( self, text ):
		QGraphicsRectItem.__init__( self )
		
		self._text			= text
		self._sortData		= text
	
	def paint( self, painter, option, widget ):
		from PyQt4.QtCore	import Qt
		
		# initialize the painter
		painter.setRenderHint( painter.Antialiasing )
		painter.setRenderHint( painter.TextAntialiasing )
		
		# set the font
		font = painter.font()
		font.setBold( True )
		painter.setFont( font )
		
		# draw the text
		scene		= self.scene()
		palette		= scene.palette()
		padding		= scene.cellPadding()
		painter.setPen( palette.color( palette.Highlight ) )
		painter.drawText( padding.width(), padding.height(), self.rect().width() - 2 * padding.width(), self.rect().height() - 2 * padding.height(), Qt.AlignLeft | Qt.AlignVCenter, self.text() )
		
		# draw the line
		painter.drawLine( padding.width(), self.rect().bottom() - 2, self.rect().width() - 2 * padding.width(), self.rect().bottom() - 2 )
	
	def setSortData( self, data ):
		self._sortData = data
	
	def sortData( self ):
		return self._sortData
	
	def text( self ):
		return self._text
	
	def setText( self, text ):
		self._text = text