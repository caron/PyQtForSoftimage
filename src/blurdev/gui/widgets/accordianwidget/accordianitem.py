##
#	\namespace	blurdev.gui.widgets.accordianwidget.accordianitem
#
#	\remarks	The container class for a widget that is collapsible within the accordian widget system
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		04/29/10
#
#

from PyQt4.QtGui 	import QGroupBox

class AccordianItem( QGroupBox ):
	def __init__( self, accordian, title, widget ):
		QGroupBox.__init__( self, accordian )
		
		# create the layout
		from PyQt4.QtCore import Qt
		from PyQt4.QtGui import QVBoxLayout
		
		layout = QVBoxLayout()
		layout.setContentsMargins( 6, 6, 6, 6 )
		layout.setSpacing( 0 )
		layout.addWidget( widget )
		
		self._accordianWidget = accordian
		self._rolloutStyle = 2
		self._dragDropMode = 0
		
		self.setAcceptDrops(True)
		self.setLayout( layout )
		self.setContextMenuPolicy( Qt.CustomContextMenu )
		self.customContextMenuRequested.connect( self.showMenu )
		
		# create custom properties
		self._widget		= widget
		self._collapsed		= False
		self._collapsible	= True
		self._clicked		= False
		self._customData	= {}
		
		from PyQt4.QtGui import QPixmap
		import os.path
		self._pixmap = QPixmap( os.path.split( __file__ )[0] + '/img/triangle.png' )
		
		# set common properties
		self.setTitle( title )
	
	def accordianWidget( self ):
		"""
			\remarks	grabs the parent item for the accordian widget
			\return		<blurdev.gui.widgets.accordianwidget.AccordianWidget>
		"""
		return self._accordianWidget
	
	def customData( self, key, default = None ):
		"""
			\remarks	return a custom pointer to information stored with this item
			\param		key			<str>
			\param		default		<variant>	default value to return if the key was not found
			\return		<variant> data
		"""
		return self._customData.get( str(key), default )
	
	def dragEnterEvent( self, event ):
		if ( not self._dragDropMode ):
			return
			
		source = event.source()
		if ( source != self and source.parent() == self.parent() and isinstance( source, AccordianItem ) ):
			event.acceptProposedAction()
	
	def dragDropRect( self ):
		from PyQt4.QtCore import QRect
		return QRect( 25, 7, 10, 6 )
	
	def dragDropMode( self ):
		return self._dragDropMode
		
	def dragMoveEvent( self, event ):
		if ( not self._dragDropMode ):
			return
			
		source = event.source()
		if ( source != self and source.parent() == self.parent() and isinstance( source, AccordianItem ) ):
			event.acceptProposedAction()
	
	def dropEvent( self, event ):
		widget = event.source()
		layout = self.parent().layout()
		layout.insertWidget( layout.indexOf(self), widget )
		self._accordianWidget.emitItemsReordered()
	
	def expandCollapseRect( self ):
		from PyQt4.QtCore import QRect
		return QRect( 0, 0, self.width(), 20 )
	
	def enterEvent( self, event ):
		self.accordianWidget().leaveEvent( event )
		event.accept()
	
	def leaveEvent( self, event ):
		self.accordianWidget().enterEvent( event )
		event.accept()
	
	def mouseReleaseEvent( self, event ):
		if ( self._clicked and self.expandCollapseRect().contains( event.pos() ) ):
			self.toggleCollapsed()
			event.accept()
		else:
			event.ignore()
		
		self._clicked = False
	
	def mouseMoveEvent( self, event ):
		event.ignore()
		
	def mousePressEvent( self, event ):
		# handle an internal move
		from PyQt4.QtCore import Qt
		
		# start a drag event
		if ( event.button() == Qt.LeftButton and self.dragDropRect().contains( event.pos() ) ):
			from PyQt4.QtCore import QMimeData
			from PyQt4.QtGui import QDrag, QPixmap
			
			# create the pixmap
			pixmap = QPixmap.grabWidget( self, self.rect() )
			
			# create the mimedata
			mimeData = QMimeData()
			mimeData.setText( 'ItemTitle::%s' % (self.title()) )
			
			# create the drag
			drag = QDrag(self)
			drag.setMimeData( mimeData )
			drag.setPixmap( pixmap )
			drag.setHotSpot( event.pos() )
			
			if ( not drag.exec_() ):
				self._accordianWidget.emitItemDragFailed(self)
			
			event.accept()
		
		# determine if the expand/collapse should occur
		elif ( event.button() == Qt.LeftButton and self.expandCollapseRect().contains( event.pos() ) ):
			self._clicked = True
			event.accept()
		
		else:
			event.ignore()
	
	def isCollapsed( self ):
		return self._collapsed
	
	def isCollapsible( self ):
		return self._collapsible
	
	def paintEvent( self, event ):
		from PyQt4.QtCore 	import Qt
		from PyQt4.QtGui	import QPainter, QPainterPath, QPalette, QPixmap, QPen
		
		painter = QPainter()
		painter.begin( self )
		painter.setRenderHint( painter.Antialiasing )
		
		x = self.rect().x()
		y = self.rect().y()
		w = self.rect().width() - 1
		h = self.rect().height() - 1
		r = 8
		
		# draw a rounded style
		if ( self._rolloutStyle == 2 ):
			
			# draw the text
			painter.drawText( x + 22, y + 3, w, 16, Qt.AlignLeft | Qt.AlignTop, self.title() )
			
			# draw the triangle
			pixmap = self._pixmap
			if ( not self.isCollapsed() ):
				from PyQt4.QtGui import QMatrix
				pixmap = pixmap.transformed( QMatrix().rotate(90) )
				
			painter.drawPixmap( x + 7, y + 4, pixmap )
			
			# draw the borders
			pen = QPen( self.palette().color( QPalette.Light ) )
			pen.setWidthF( 0.6 )
			painter.setPen( pen )
			
			painter.drawRoundedRect( x + 1, y + 1, w - 1, h - 1, r, r )
			
			pen.setColor( self.palette().color( QPalette.Shadow ) )
			painter.setPen( pen )
			
			painter.drawRoundedRect( x, y, w - 1, h - 1, r, r )
			
		# draw a boxed style
		elif ( self._rolloutStyle == 1 ):
			from PyQt4.QtCore import QRect
			if ( self.isCollapsed() ):
				arect 	= QRect( x + 1, y + 9, w - 1, 4 )
				brect 	= QRect( x, y + 8, w - 1, 4 )
				text 	= '+'
			else:
				arect	= QRect( x + 1, y + 9, w - 1, h - 9 )
				brect 	= QRect( x, y + 8, w - 1, h - 9 )
				text	= '-'
			
			# draw the borders
			pen = QPen( self.palette().color( QPalette.Light ) )
			pen.setWidthF( 0.6 )
			painter.setPen( pen )
			
			painter.drawRect( arect )
			
			pen.setColor( self.palette().color( QPalette.Shadow ) )
			painter.setPen( pen )
			
			painter.drawRect( brect )
			
			painter.setRenderHint( painter.Antialiasing, False )
			painter.setBrush( self.palette().color( QPalette.Window ).darker( 120 ) )
			painter.drawRect( x + 10, y + 1, w - 20, 16 )
			painter.drawText( x + 16, y + 1, w - 32, 16, Qt.AlignLeft | Qt.AlignVCenter, text )
			painter.drawText( x + 10, y + 1, w - 20, 16, Qt.AlignCenter, self.title() )
		
		if ( self.dragDropMode() ):
			rect 	= self.dragDropRect()
			
			# draw the lines
			l		= rect.left()
			r		= rect.right()
			cy		= rect.center().y()
			
			for y in (cy - 3, cy, cy + 3):
				painter.drawLine( l, y, r, y )
			
		painter.end()
	
	def setCollapsed( self, state = True ):
		if ( self.isCollapsible() ):
			accord = self.accordianWidget()
			accord.setUpdatesEnabled(False)
			
			self._collapsed = state
			
			if ( state ):
				self.setMinimumHeight( 22 )
				self.setMaximumHeight( 22 )
				self.widget().setVisible( False )
			else:
				self.setMinimumHeight( 0 )
				self.setMaximumHeight( 1000000 )
				self.widget().setVisible( True )
			
			self._accordianWidget.emitItemCollapsed( self )
			accord.setUpdatesEnabled(True)
	
	def setCollapsible( self, state = True ):
		self._collapsible = state
	
	def setCustomData( self, key, value ):
		"""
			\remarks	set a custom pointer to information stored on this item
			\param		key		<str>
			\param		value	<variant>
		"""
		self._customData[ str(key) ] = value
	
	def setDragDropMode( self, mode ):
		self._dragDropMode = mode
	
	def setRolloutStyle( self, style ):
		self._rolloutStyle = style
	
	def showMenu( self ):
		from PyQt4.QtCore import QRect
		from PyQt4.QtGui import QCursor
		if ( QRect( 0, 0, self.width(), 20 ).contains( self.mapFromGlobal( QCursor.pos() ) ) ):
			self._accordianWidget.emitItemMenuRequested( self )
	
	def rolloutStyle( self ):
		return self._rolloutStyle
	
	def toggleCollapsed( self ):
		self.setCollapsed( not self.isCollapsed() )
	
	def widget( self ):
		return self._widget
