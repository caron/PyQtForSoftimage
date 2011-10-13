##
#	\namespace	blurdev.gui.helpers.hinthelper
#
#	\remarks	The HintHelper class helps provide a constant tool tip to
#				text editing fields
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		12/18/08
#

from PyQt4.QtGui import QLabel

class HintHelper( QLabel ):
	def __init__( self, parent, hint ):
		QLabel.__init__( self, parent )
		
		# connect to a combobox
		from PyQt4.QtGui import QComboBox, QLineEdit, QTextEdit
		if ( isinstance( parent, QComboBox ) ):
			if ( not parent.isEditable() ):
				parent.setEditable( True )
				parent.setInsertPolicy( QComboBox.NoInsert )
			
			# connect to the line edit method
			parent.lineEdit().textChanged.connect( self.toggleVisibility )
		
		# connect to a lineedit
		elif ( isinstance( parent, QLineEdit ) or isinstance( parent, QTextEdit ) ):
			parent.textChanged.connect( self.toggleVisibility )
		
		# update the information
		self.setText( hint )
		
		# show the palette in gray
		palette = self.palette()
		color	= palette.color( palette.AlternateBase ).darker( 125 )
		
		# set the color for all the roles
		palette.setColor( palette.WindowText, color )
		palette.setColor( palette.Text, color )
		
		parent.installEventFilter( self )
		
		self.setPalette( palette )
		self.move( 6, 4 )
	
	def eventFilter( self, object, event ):
		if ( event.type() == event.Resize ):
			self.resize( event.size().width() - 6, event.size().height() - 4 )
		return False
	
	def hint( self ):
		return self.text()
	
	def setHint( self, text ):
		self.setText( text )
		self.adjustSize()
	
	def setVisible( self, state ):
		self.toggleVisibility()
	
	def toggleVisibility( self ):
		""" Toggles the visibility of the hint based on the state of the widget """
		
		state 	= self.parent().isVisible()
		parent 	= self.parent()
		
		# check a combobox
		from PyQt4.QtGui import QComboBox, QLineEdit, QTextEdit
		if ( isinstance( parent, QComboBox ) ):
			state = parent.lineEdit().text() == ''
		
		# check a lineedit
		elif ( isinstance( parent, QLineEdit ) ):
			state = parent.text() == ''
		
		# check a textedit
		elif ( isinstance( parent, QTextEdit ) ):
			state = parent.toPlainText() == ''
		
		QLabel.setVisible( self, state )