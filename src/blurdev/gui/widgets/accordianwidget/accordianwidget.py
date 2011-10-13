##
#	\namespace	trax.gui.widgets.accordianwidget
#
#	\remarks	A container widget for creating expandable and collapsible components
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		04/29/10
#
#

from PyQt4.QtCore 	import pyqtSignal, pyqtProperty
from PyQt4.QtGui 	import QScrollArea
from accordianitem	import AccordianItem

class AccordianWidget( QScrollArea ):
	itemCollapsed 		= pyqtSignal(AccordianItem)
	itemMenuRequested	= pyqtSignal(AccordianItem)
	itemDragFailed		= pyqtSignal(AccordianItem)
	itemsReordered		= pyqtSignal()
	
	Boxed 		= 1
	Rounded 	= 2
	
	NoDragDrop 		= 0
	InternalMove	= 1
	
	def __init__( self, parent ):
		QScrollArea.__init__( self, parent )
		
		self.setFrameShape( QScrollArea.NoFrame )
		self.setAutoFillBackground( False )
		self.setWidgetResizable( True )
		self.setMouseTracking(True)
		self.verticalScrollBar().setMaximumWidth(10)
		
		from PyQt4.QtGui import QWidget
		widget = QWidget( self )
		
		# define custom properties
		self._rolloutStyle 	= AccordianWidget.Rounded
		self._dragDropMode 	= AccordianWidget.NoDragDrop
		self._scrolling		= False
		self._scrollInitY	= 0
		self._scrollInitVal	= 0
		self._itemClass		= AccordianItem
		
		# create the layout
		from PyQt4.QtGui import QVBoxLayout
		
		layout = QVBoxLayout()
		layout.setContentsMargins( 3, 3, 3, 3 )
		layout.setSpacing( 3 )
		layout.addStretch(1)
		
		widget.setLayout( layout )
		
		self.setWidget( widget )
	
	def addItem( self, title, widget, collapsed = False ):
		self.setUpdatesEnabled(False)
		item 	= self._itemClass( self, title, widget )
		item.setRolloutStyle( self.rolloutStyle() )
		item.setDragDropMode( self.dragDropMode() )
		layout	= self.widget().layout()
		layout.insertWidget( layout.count() - 1, item )
		layout.setStretchFactor( item, 0 )
		
		if ( collapsed ):
			item.setCollapsed(collapsed)
		
		self.setUpdatesEnabled(True)
		return item
	
	def clear( self ):
		self.setUpdatesEnabled(False)
		layout = self.widget().layout()
		while ( layout.count() > 1 ):
			item = layout.itemAt(0)
			
			# remove the item from the layout
			w = item.widget()
			layout.removeItem( item )
			
			# close the widget and delete it
			w.close()
			w.deleteLater()
			
		self.setUpdatesEnabled(True)
	
	def eventFilter( self, object, event ):
		from PyQt4.QtCore import QEvent
		
		if ( event.type() == QEvent.MouseButtonPress ):
			self.mousePressEvent( event )
			return True
			
		elif ( event.type() == QEvent.MouseMove ):
			self.mouseMoveEvent( event )
			return True
			
		elif ( event.type() == QEvent.MouseButtonRelease ):
			self.mouseReleaseEvent( event )
			return True
			
		return False
	
	def canScroll( self ):
		return self.verticalScrollBar().maximum() > 0
	
	def count( self ):
		return self.widget().layout().count() - 1
	
	def dragDropMode( self ):
		return self._dragDropMode
	
	def isBoxedMode( self ):
		return self._rolloutStyle == AccordianWidget.Boxed
	
	def itemClass( self ):
		return self._itemClass
	
	def itemAt( self, index ):
		layout = self.widget().layout()
		if ( 0 <= index and index < layout.count() - 1 ):
			return layout.itemAt( index ).widget()
		return None
	
	def emitItemCollapsed( self, item ):
		if ( not self.signalsBlocked() ):
			self.itemCollapsed.emit(item)
	
	def emitItemDragFailed( self, item ):
		if ( not self.signalsBlocked() ):
			self.itemDragFailed.emit(item)
		
	def emitItemMenuRequested( self, item ):
		if ( not self.signalsBlocked() ):
			self.itemMenuRequested.emit(item)
	
	def emitItemsReordered( self ):
		if ( not self.signalsBlocked() ):
			self.itemsReordered.emit()
	
	def enterEvent( self, event ):
		if ( self.canScroll() ):
			from PyQt4.QtCore import Qt
			from PyQt4.QtGui import QApplication
			QApplication.setOverrideCursor( Qt.OpenHandCursor )
	
	def leaveEvent( self, event ):
		if ( self.canScroll() ):
			from PyQt4.QtGui import QApplication
			QApplication.restoreOverrideCursor()
	
	def mouseMoveEvent( self, event ):
		if ( self._scrolling ):
			sbar 	= self.verticalScrollBar()
			smax	= sbar.maximum()
			
			# calculate the distance moved for the moust point
			dy 			= event.globalY() - self._scrollInitY
			
			# calculate the percentage that is of the scroll bar
			dval		= smax * ( dy / float(sbar.height()) )
			
			# calculate the new value
			sbar.setValue( self._scrollInitVal - dval )
			
		event.accept()
	
	def mousePressEvent( self, event ):
		# handle a scroll event
		from PyQt4.QtCore import Qt
		from PyQt4.QtGui import QApplication
		
		if ( event.button() == Qt.LeftButton and self.canScroll() ):
			self._scrolling 		= True
			self._scrollInitY		= event.globalY()
			self._scrollInitVal 	= self.verticalScrollBar().value()
			
			QApplication.setOverrideCursor( Qt.ClosedHandCursor )
		
		event.accept()
	
	def mouseReleaseEvent( self, event ):
		from PyQt4.QtCore 	import Qt
		from PyQt4.QtGui 	import QApplication
		
		if ( self._scrolling ):
			QApplication.restoreOverrideCursor()
		
		self._scrolling 		= False
		self._scrollInitY		= 0
		self._scrollInitVal		= 0
		event.accept()
	
	def setBoxedMode( self, state ):
		if ( state ):
			self._rolloutStyle = AccordianWidget.Boxed
		else:
			self._rolloutStyle = AccordianWidget.Rounded
	
	def setDragDropMode( self, dragDropMode ):
		self._dragDropMode = dragDropMode
		
		for item in self.findChildren( AccordianItem ):
			item.setDragDropMode( self._dragDropMode )
	
	def setItemClass( self, itemClass ):
		self._itemClass = itemClass
	
	def setRolloutStyle( self, rolloutStyle ):
		self._rolloutStyle = rolloutStyle
		
		for item in self.findChildren( AccordianItem ):
			item.setRolloutStyle( self._rolloutStyle )
	
	def rolloutStyle( self ):
		return self._rolloutStyle
	
	def takeAt( self, index ):
		self.setUpdatesEnabled(False)
		layout = self.widget().layout()
		widget = None
		if ( 0 <= index and index < layout.count() - 1 ):
			item = layout.itemAt(index)
			widget = item.widget()
			
			layout.removeItem(item)
			widget.close()
		self.setUpdatesEnabled(True)
		return widget
	
	def widgetAt( self, index ):
		item = self.itemAt( index )
		if ( item ):
			return item.widget()
		return None
	
	pyBoxedMode = pyqtProperty( 'bool', isBoxedMode, setBoxedMode )