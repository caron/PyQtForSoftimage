##
#	\namespace	python.blurdev.gui.dialogs.multiprogressdialog
#
#	\remarks	
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		03/14/11
#

from PyQt4.QtGui import QTreeWidgetItem

class ProgressSection( QTreeWidgetItem ):
	def __init__( self, name, count = 100, value = -1, allowsCancel = False ):
		QTreeWidgetItem.__init__( self, [ name ] )
		
		from PyQt4.QtCore import Qt, QSize
		self.setTextAlignment( 1, Qt.AlignRight | Qt.AlignVCenter )
		self.setSizeHint( 1, QSize( 20, 18 ) )
		
		self._value				= value
		self._count				= count
		self._cancelled 		= False
		self._cancelAccepted	= False
		self._allowsCancel		= allowsCancel
		self._errorText 		= ''
		
		self.refreshLook()
	
	def acceptCancel( self ):
		if ( self._cancelled ):
			self._cancelAccepted = True
			self.setText( 1, 'cancel accepted' )
			self.updateWindow()
	
	def allowsCancel( self ):
		return self._allowsCancel
	
	def cancelled( self ):
		return self._cancelled
	
	def cancel( self ):
		self._cancelled = True
		self.refreshLook()
	
	def cancelAccepted( self ):
		return self._cancelAccepted
	
	def completed( self ):
		return self._count <= (self._value+1)
	
	def count( self ):
		return self._count
	
	def errored( self ):
		return self._errorText != ''
	
	def finish( self ):
		self.setValue( self._count - 1 )
	
	def increment( self ):
		self.setValue( self._value + 1 )
	
	def message( self ):
		return self._message
	
	def percentComplete( self ):
		return float(self._value+1) / self._count
	
	def refreshLook( self ):
		from PyQt4.QtGui import QColor
		
		# set the error look
		if ( self._errorText ):
			text = 'error occurred'
			clr = QColor( 'red' )
		
		# set the cancel look
		elif ( self._cancelled ):
			text = 'user cancelled'
			clr = QColor( 'red' )
		
		# set the progress look
		elif ( self.completed() ):
			text = 'completed'
			clr = QColor( 'darkGreen' )
			
		
		# set the finished look
		elif ( 0 <= self._value ):
			text = '%i%%' % (100 * float(self._value)/self._count)
			clr = QColor( 'black' )
		
		# set the waiting look
		else:
			text = 'waiting'
			clr = QColor( 'gray' )
		
		self.setForeground( 0, clr )
		self.setForeground( 1, clr )
		self.setText( 1, text )
		self.updateWindow()
	
	def updateWindow( self ):
		tree = self.treeWidget()
		if ( tree ):
			tree.window().update()
	
	def setAllowsCancel( self, state ):
		self._allowsCancel = state
	
	def setErrorText( self, text ):
		self._errorText = text
		self.setToolTip( 0, text )
		self.setToolTip( 1, text )
		self.refreshLook()
	
	def setCount( self, count ):
		# make sure we have a valid count number
		if ( count < 1 ):
			count = 1
			
		self._count = count
		self.refreshLook()
	
	def setMessage( self, message ):
		self._message = message
	
	def setPercentComplete( self, percent ):
		self.setValue((percent / 100.0) * self._count)
	
	def setValue( self, value ):
		self._value = value
		tree = self.treeWidget()
		if ( tree ):
			tree.setCurrentItem( self, 0 )
		self.refreshLook()
	
	def value( self ):
		return self._value
		