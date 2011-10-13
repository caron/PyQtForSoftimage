##
#	\namespace	blurdev.gui.helpers.widgeteventhelper
#
#	\remarks	The WidgetEventHelper class provides some event filter and drag & drop override functionality
#				to widgets, making it simpler to provide an easy filtering system without having to sub
#				class and reimplement the functionality every time - specifically useful for QAbstractItemView items for drag & drop
#				functionality which does not behave properly with an event filter
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		04/15/10
#

from PyQt4.QtCore import QObject

class WidgetEventHelper( QObject ):
	def __init__( self, widget ):
		QObject.__init__( self, widget )
		self.setObjectName( 'eventHelper' )
		
		self._connections = {}
		
		# most events work just fine, but drag & drop do not get filtered properly 
		# to the eventFilter, so we have to custom bind them
		
		import blurdev
		blurdev.bindMethod( widget, 'dragEnterEvent',	self.handleDragEnterEvent )
		blurdev.bindMethod( widget, 'dragMoveEvent',	self.handleDragMoveEvent )
		blurdev.bindMethod( widget, 'dropEvent', 		self.handleDropEvent )
		
		widget.installEventFilter( self )
	
	def eventConnect( self, eventType, slot ):
		"""
			\remarks	Connects a specific event type to run the inputed slot function
			\param		eventType	<QEvent.Type>
			\param		slot		<function> || <method>
		"""
		self._connections[ int(eventType) ] = slot
	
	def eventFilter( self, object, event ):
		"""
			\remarks	overloaded the event filter for this item
			\param		object	<QObject>
			\param		event	<QEvent>
			\return		<bool> accept
		"""
		
		# run the slot for the event type
		etype = int( event.type() )
		if ( object == self.parent() and etype in self._connections ):
			if ( self._connections[ etype ]( object, event ) ):
				return True
		
		# if the event did not tell this to eat the event, then continue
		return QObject.eventFilter( self, object, event )
	
	def handleDragEnterEvent( widget, event ):
		"""
			\remarks	bound method to handle the drag enter event for the widget
			\param		widget	<QWidget>
			\param		event	<QEvent>
		"""
		handler = widget.findChild( WidgetEventHelper, 'eventHelper' )
		
		# if the handler accepts the event, then continue on
		if ( handler.eventFilter( widget, event ) ):
			return
		
		# otherwise, filter this object properly
		widget.__class__.dragEnterEvent( widget, event )
	
	def handleDragMoveEvent( widget, event ):
		"""
			\remarks	bound method to handle the drag move event for the widget
			\param		widget	<QWidget>
			\param		event	<QEvent>
		"""
		handler = widget.findChild( WidgetEventHelper, 'eventHelper' )
		
		# if the handler accepts the event, then continue on
		if ( handler.eventFilter( widget, event ) ):
			return
		
		# otherwise, filter this object properly
		widget.__class__.dragMoveEvent( widget, event )
	
	def handleDropEvent( widget, event ):
		"""
			\remarks	bound method to handle the drop event for the widget
			\param		widget	<QWidget>
			\param		event	<QEvent>
		"""
		handler = widget.findChild( WidgetEventHelper, 'eventHelper' )
		
		# if the handler accepts the event, then continue on
		if ( handler.eventFilter( widget, event ) ):
			return
		
		# otherwise, filter this object properly
		widget.__class__.dropEvent( widget, event )
	