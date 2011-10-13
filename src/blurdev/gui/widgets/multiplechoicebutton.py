##
#	\namespace	python.blurdev.gui.widgetsmultioptionwidget
#
#	\remarks	
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		03/28/11
#

from PyQt4.QtCore 	import pyqtSignal, QLine, pyqtProperty, Qt, QRect, QSize
from PyQt4.QtGui 	import QAbstractButton, QPainter, QColor, QPalette, QLinearGradient, QPainterPath, QBrush, QCursor

class MultipleChoiceButton( QAbstractButton ):
	currentChoiceChanged 	= pyqtSignal( str )		# emitted when the current choice is changed
	currentValueChanged		= pyqtSignal( int )		# emitted when the current choice is changed, only if an enum instance is provided for the system
	
	def __init__( self, parent ):
		# initialize the super class
		QAbstractButton.__init__( self, parent )
		
		self.setMouseTracking(True)
		self.setMinimumSize( QSize( 80, 22 ) )
		
		# create custom properties
		self._currentChoice		= 'Option A'
		self._choices			= [ 'Option A', 'Option B' ]
		self._highlightColor	= self.palette().color( QPalette.Highlight )
		self._cornerRadius		= 8
		self._enum				= None
	
	def choices( self ):
		return self._choices
	
	def cornerRadius( self ):
		return self._cornerRadius
	
	def currentChoice( self ):
		return self._currentChoice
	
	def currentValue( self ):
		if ( self._enum ):
			return self._enum.valueByLabel( self.currentChoice() )
		return 0
	
	def highlightColor( self ):
		return self._highlightColor
	
	def mouseReleaseEvent( self, event ):
		# determine the current choice based on the position
		count 	= len(self._choices)
		if ( not count ):
			self.setCurrentChoice( '' )
		else:
			currx	= 1
			y		= 1
			h		= self.height() - 2
			w 		= self.width() - 2
			bw 		= w / float(count)
			p		= event.pos()
			
			for i in range( count ):
				r = QRect( currx, y, bw, h )
				if ( r.contains( p ) ):
					self.setCurrentChoice( self._choices[i] )
					break
				
				currx += bw
		
		return QAbstractButton.mouseReleaseEvent( self, event )
	
	def paintEvent( self, event ):
		painter = QPainter()
		painter.begin(self)
		painter.setRenderHint( QPainter.Antialiasing )
		pen = painter.pen()
		pen.setWidthF( 0.5 )
		painter.setPen(pen)
		
		# draw the base of the button
		x			= 1
		y			= 1
		w			= self.width() - 2		# width
		r			= self.cornerRadius()	# radius
		h			= self.height() - 2		# height
		ch			= h / 2.0				# center-height
		
		# create the base path
		path 		= QPainterPath()
		path.moveTo( r, y )
		path.lineTo( w - r, y )
		path.quadTo( w, y, w, r )
		path.lineTo( w, h - r )
		path.quadTo( w, h, w - r, h )
		path.lineTo( r, h )
		path.quadTo( x, h, x, h - r )
		path.lineTo( x, r )
		path.quadTo( x, y, r, y )
		
		# create the base brush
		grad		= QLinearGradient( x, y, x, h )
		
		# \TODO: 	figure out a good way to do "mouse over" look	- # EKH 03/28/11
		if ( False ):
			grad.setColorAt( 0, 	self.highlightColor() )
			grad.setColorAt( 0.05, 	self.palette().color( QPalette.Button ).lighter(110) )
			grad.setColorAt( 0.95,	self.palette().color( QPalette.Button ).darker(110) )
			grad.setColorAt( 1,		self.highlightColor() )
		else:
			grad.setColorAt( 0, 	self.palette().color( QPalette.Button ).lighter(110) )
			grad.setColorAt( 1,		self.palette().color( QPalette.Button ).darker(110) )
		
		brush		= QBrush(grad)
		
		painter.setBrush(brush)
		painter.drawPath(path)
		
		# create the choice brush
		choicegrad	= QLinearGradient( x, y, x, h )
		choicegrad.setColorAt( 0, self.highlightColor().darker(110) )
		choicegrad.setColorAt( 1, self.highlightColor().lighter(110) )
		
		choicebrush = QBrush(choicegrad)
		
		# create the choice path
		choicepath 	= QPainterPath()
		currchoice	= self.currentChoice()
		
		# determine the width of the choices based on the current width and the number of chioces
		count = len(self._choices)
		if ( count > 1 ):
			painter.setBrush( brush )
			painter.drawPath( path )
			
			bw = w / float(count)
			currx	= x
			lines 	= []
			found	= False
			
			for i in range( count - 1 ):
				lines.append( QLine( currx + bw, y, currx + bw, h ) )
				
				# see if the current button is part of the choices
				if ( self._choices[i] == currchoice ):
					# draw the first section
					if ( not i ):
						choicepath.moveTo( r, y )
						choicepath.lineTo( bw, y )
						choicepath.lineTo( bw, h )
						choicepath.lineTo( r, h )
						choicepath.quadTo( x, h, x, h - r )
						choicepath.lineTo( x, r )
						choicepath.quadTo( x, y, r, y )
						
						painter.setBrush( choicebrush )
						painter.drawPath( choicepath )
					
					# draw a middle section
					else:
						choicepath.moveTo( currx, y )
						choicepath.lineTo( currx + bw, y )
						choicepath.lineTo( currx + bw, h )
						choicepath.lineTo( currx, h )
						choicepath.lineTo( currx, y )
					
						painter.setBrush( choicebrush )
						painter.drawPath( choicepath )
					
					found = True
				
				# draw the text for this button
				painter.drawText( currx, y, bw, h, Qt.AlignCenter, self._choices[i] )
				
				# move the xpos along
				currx += bw
			
			# otherwise, the last section is the active choice
			if ( not found ):
				choicepath.moveTo( w - bw, y )
				choicepath.lineTo( w - r, y )
				choicepath.quadTo( w, y, w, r )
				choicepath.lineTo( w, h - r )
				choicepath.quadTo( w, h, w - r, h )
				choicepath.lineTo( w - bw, h )
				choicepath.lineTo( w - bw, y )
				
				painter.setBrush( choicebrush )
				painter.drawPath( choicepath )
				
			# draw the text for the last button
			painter.drawText( w - bw, y, bw, h, Qt.AlignCenter, self._choices[-1] )
			painter.drawLines(lines)
		
		# if there is only 1 choice, it will always be on
		else:
			painter.setBrush( choicebrush )
			painter.drawPath( path )
		
		painter.end()
	
	def setChoices( self, choices ):
		self._choices = [ str(choice) for choice in choices ]
		self.repaint()
	
	def setCurrentChoice( self, choice ):
		if ( choice == self._currentChoice ):
			return False
			
		self._currentChoice = choice
		
		# emit the current choice changed signal
		if ( not self.signalsBlocked() ):
			self.currentChoiceChanged.emit(choice)
			if ( self._enum ):
				self.currentValueChanged.emit(self.currentValue())
			
		self.repaint()
		return True
	
	def setCurrentValue( self, value ):
		if ( self._enum ):
			return self._enum.labelByValue(value)
		return False
	
	def setEnum( self, enum ):
		self._enum = enum
		self.setChoices( enum.labels() )
	
	def setHighlightColor( self, color ):
		self._highlightColor = color
		self.repaint()
	
	def setCornerRadius( self, cornerRadius ):
		self._cornerRadius = cornerRadius
	
	pyCornerRadius		= pyqtProperty( 'int',			cornerRadius,		setCornerRadius	)
	pyCurrentChoice		= pyqtProperty( 'QString',		currentChoice,		setCurrentChoice )
	pyChoices			= pyqtProperty( 'QStringList',	choices,			setChoices )