##
#	\namespace	blurdev.gui.scenes.thumbnailscene.thumbnailscene
#
#	\remarks	The ThumbnailScene class is a QGraphicsScene subclass that allows the user to show thumbnails easily and in a graphically pleasing way -
#				with autoresizing to fit the view scope and selection capabilities
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		03/31/10
#

from PyQt4.QtCore	import pyqtSignal
from PyQt4.QtGui 	import QGraphicsScene
from thumbnailitem	import ThumbnailItem

#-------------------------------------------------------------------------------------------------------------

class ThumbnailScene( QGraphicsScene ):
	itemDoubleClicked 	= pyqtSignal( ThumbnailItem )
	itemMenuRequested	= pyqtSignal( ThumbnailItem )
	
	def __init__( self, view = None ):
		QGraphicsScene.__init__( self )
		
		from PyQt4.QtCore	import Qt, QRect, QSize
		from PyQt4.QtGui	import QBrush
		
		# set default parameters
		from PyQt4.QtGui import QColor
		self.setBackgroundBrush( QColor( 120, 120, 120 ) )
		
		# create the view linking
		if ( view ):
			view.setScene( self )
			view.installEventFilter( self )
			view.setAlignment( Qt.AlignLeft | Qt.AlignTop )
		
		# custom properties
		self._reverseSort		= False
		self._lastRect			= QRect()
		self._highlightBrush	= QBrush( QColor( 'lightGray' ) )
		self._layoutDirection	= Qt.Vertical
		self._thumbnailSize 	= QSize(128,128)
		self._cellPadding		= QSize(6,6)
		self._showCaptions		= False
		self._captionPadding	= 2
		self._captionHeight		= 24
	
	def addThumbGroup( self, name ):
		from thumbnailgroup import ThumbnailGroup
		
		output = ThumbnailGroup( name )
		self.addItem( output )
		return output
	
	def addThumbnail( self, filename ):
		from thumbnailitem	import ThumbnailItem
		
		newitem = ThumbnailItem( filename )
		self.addItem( newitem )
		return newitem
	
	def captionPadding( self ):
		return self._captionPadding
	
	def captionHeight( self ):
		return self._captionHeight
	
	def cellPadding( self ):
		return self._cellPadding
	
	def eventFilter( self, object, event ):
		from PyQt4.QtCore	import QEvent
		
		# handle the resize events
		if ( event.type() == QEvent.Resize ):
			self.recalculateFromView( object )
			
			# center on selection
			items = self.selectedItems()
			if ( items ):
				object.centerOn( items[0] )
			
		return QGraphicsScene.eventFilter( self, object, event )
	
	def highlightBrush( self ):
		return self._highlightBrush
	
	def lastRect( self ):
		return self._lastRect
	
	def layoutDirection( self ):
		return self._layoutDirection
		
	def keyPressEvent( self, event ):
		from PyQt4.QtCore	import Qt
		
		# select the item to the left
		if ( event.key() == Qt.Key_Left ):
			selection = self.selectedItems()
			if ( selection ):
				items 	= self.items()
				item 	= selection[0]
				if ( item in items ):
					index = items.index(item)
				
					# select the previous item
					if ( index > 0 ):
						self.blockSignals( True )  # don't emit the selectionChanged signal twice
						self.clearSelection()
						self.blockSignals( False )
						items[index-1].setSelected(True)
						
						# center on the selection
						for view in self.views():
							view.centerOn( items[index-1] )
			
			event.accept()
			
		# select the item to the right
		elif ( event.key() == Qt.Key_Right ):
			selection = self.selectedItems()
			if ( selection ):
				items 	= self.items()
				item	= selection[0]
				if ( item in items ):
					index = items.index(item)
					if ( index < len( items ) - 1 ):
						self.blockSignals( True )  # don't emit the selectionChanged signal twice
						self.clearSelection()
						self.blockSignals( False )
						items[index+1].setSelected(True)
						
						# center on item
						for view in self.views():
							view.centerOn( items[index+1] )
						
			event.accept()
		
		# select the item above this one
		elif ( event.key() == Qt.Key_Up ):
			selection = self.selectedItems()
			if ( selection ):
				item 	= selection[0]
				x		= item.pos().x() + item.rect().center().x()
				y		= item.pos().y() + item.rect().center().y() - (item.rect().height())
				
				newitem = self.itemAt( x, y )
				if ( newitem ):
					self.blockSignals( True ) # don't emit the selectionChanged signal twice
					self.clearSelection()
					self.blockSignals( False )
					newitem.setSelected( True )
					
					# center on item
					for view in self.views():
						view.centerOn( newitem )
			
			event.accept()
		
		# select the item below this one
		elif ( event.key() == Qt.Key_Down ):
			selection = self.selectedItems()
			if ( selection ):
				item	= selection[0]
				x		= item.pos().x() + item.rect().center().x()
				y		= item.pos().y() + item.rect().center().y() + (item.rect().height())
				
				newitem = self.itemAt( x, y )
				if ( newitem ):
					self.blockSignals( True ) # don't emit the selectionChanged signal twice
					self.clearSelection()
					self.blockSignals( False )
					newitem.setSelected( True )
					
					# center on item
					for view in self.views():
						view.centerOn( newitem )
					
			event.accept()
		
		# run the normal key event
		else:
			QGraphicsScene.keyReleaseEvent( self, event )
	
	def recalculateFromView( self, view, force = False ):
		from PyQt4.QtCore	import Qt
		
		rect = view.rect()
		if ( self.layoutDirection() == Qt.Vertical ):
			rect.setWidth( rect.width() - 25 ) # factor out vertical scroll bar
		else:
			rect.setHeight( rect.height() - 25 ) # factor out horizontal scroll bar
		
		self.recalculate( rect, force )
	
	def recalculate( self, rect, force = False ):
		from PyQt4.QtCore	import Qt
		from thumbnailitem 	import ThumbnailItem
		
		# figure out if this needs to be recalculated based on the change
		if ( self.layoutDirection() == Qt.Vertical and not (force or rect.width() != self.lastRect().width()) ):
			return True
		elif ( self.layoutDirection() == Qt.Horizontal and not (force or rect.height() != self.lastRect().height()) ):
			return True
		
		# cache the current rect
		self._lastRect = rect
		
		# setup the common variables
		width 		= rect.width()
		height		= rect.height()
		icowidth	= self.thumbnailSize().width()
		icoheight	= self.thumbnailSize().height()
		padding		= self.cellPadding()
		cellwidth	= (icowidth + (2 * padding.width()))
		cellheight	= (icoheight + (2 * padding.height()))
		if ( self.showCaptions() ):
			cellheight += self.captionPadding() + self.captionHeight()
			
		bottom		= 0
		right		= 0
		
		# load the thumbnails and groups
		items		= self.items()
		grp_map		= {}
		for item in items:
			# process a thumbnail item
			if ( isinstance( item, ThumbnailItem ) ):
				tgroup = item.thumbGroup()
				if ( not tgroup in grp_map ):
					grp_map[ tgroup ] = [ item ]
				else:
					grp_map[ tgroup ].append( item )
				
			# process a thumbnail group
			elif ( not item in grp_map ):
				grp_map[ item ] = []
			
		# calculate the group information
		keys = grp_map.keys()
		keys.sort( lambda x,y: cmp( x.sortData(), y.sortData() ) )
		
		if ( self.reverseSort() ):
			keys.reverse()
			
		ypos = padding.height()
		for key in keys:
			if ( key ):
				key.setRect( 0, 0, width, 25 )
				key.setPos( 0, ypos )
				
				ypos += 25 + padding.height()
			
			thumbs 		= grp_map[key]
			numthumbs 	= len( thumbs )
			
			# calculate the grid for a vertical scene
			if ( self.layoutDirection() == Qt.Vertical ):
				colcount = int( float( width - (2 * padding.width()) ) / cellwidth )
				if ( colcount == 0 ):
					colcount = 1
				
				if ( colcount < numthumbs ):
					rowcount = numthumbs / colcount + 1
					if ( numthumbs % colcount ):
						rowcount += 1
				else:
					rowcount = 1
			
			# calculate the grid for a horizontal scene
			else:
				rowcount = int( float( height - (2 * padding.height()) ) / cellheight )
				if ( rowcount == 0 ):
					rowcount = 1
				
				if ( rowcount < numthumbs ):
					colcount = numthumbs / rowcount + 1
					if ( numthumbs % rowcount ):
						colcount += 1
				else:
					colcount = 1
				
			# layout the items in the grid
			col		= 0
			row		= 0
			xpos 	= padding.width()
			
			thumbs.sort( lambda x,y: cmp( x.sortData(), y.sortData() ) )
			
			for item in thumbs:
				item.setRect( 0, 0, cellwidth, cellheight )
				item.setPos( xpos, ypos )
				
				# increment the information
				col += 1
				if ( col == colcount ):
					col 	= 0
					xpos 	= padding.width()
					ypos 	+= cellheight
				else:
					xpos	+= cellwidth
					
				if ( xpos > right ):
					right = xpos
			
			ypos += cellheight + padding.height()
			if ( ypos > bottom ):
				bottom = ypos
				
		self.setSceneRect( 0, 0, right, bottom )
	
	def reverseSort( self ):
		return self._reverseSort
	
	def setCaptionPadding( self, padding ):
		self._captionPadding = padding
	
	def setCaptionHeight( self, height ):
		self._captionHeight = height

	def setCellPadding( self, padding ):
		self._cellPadding = padding

	def setHighlightBrush( self, brush ):
		from PyQt4.QtGui	import QBrush
		self._highlightBrush = QBrush( brush )

	def setLayoutDirection( self, direction ):
		self._layoutDirection = direction
		
		from PyQt4.QtCore import Qt
		if ( direction == Qt.Vertical ):
			for view in self.views():
				view.setVerticalScrollBarPolicy( Qt.ScrollBarAlwaysOn )
				view.setHorizontalScrollBarPolicy( Qt.ScrollBarAlwaysOff )
		else:
			for view in self.views():
				view.setVerticalScrollBarPolicy( Qt.ScrollBarAlwaysOff )
				view.setHorizontalScrollBarPolicy( Qt.ScrollBarAlwaysOn )
	
	def setReverseSort( self, state = True ):
		self._reverseSort = state
	
	def setShowCaptions( self, state ):
		self._showCaptions = state
		
	def setThumbnailSize( self, size ):
		if ( size != self._thumbnailSize ):
			from PyQt4.QtCore	import Qt
			from thumbnailitem 	import ThumbnailItem
			
			self._thumbnailSize = size
			for item in self.items():
				if ( isinstance( item, ThumbnailItem ) ):
					item.clearThumbnail()
				
			self.recalculateFromView( self.views()[0], True )
	
	def showCaptions( self ):
		return self._showCaptions
	
	def thumbnailSize( self ):
		return self._thumbnailSize