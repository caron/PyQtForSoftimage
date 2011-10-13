##
#	\namespace	python.blurdev.gui.widgets.colorwidgets
#
#	\remarks	Creates a generic color widget
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		01/20/11
#

# used in painting, faster to do global import
from PyQt4.QtCore 	import Qt, pyqtSlot, pyqtProperty, pyqtSignal, QPoint, QRect
from PyQt4.QtGui 	import QPainter, QColor, QWidget, QLinearGradient, QPushButton, QConicalGradient, QRadialGradient

class ColorPickerWidget( QWidget ):
	BarWidth		= 15

	colorChanged	= pyqtSignal( QColor )
	editingFinished	= pyqtSignal()
	
	def __init__( self, parent ):
		# initialize the super class
		QWidget.__init__( self, parent )
		
		self._hue			= 0			# defines red color
		self._saturation	= 255
		self._lightness		= 255
		self._alpha			= 255
		self._showAlpha		= True
		self._editing		= None
		
	def alpha( self ):
		return self._alpha
	
	def alphaPercent( self ):
		return self._alpha / 255.0
	
	def alphaRect( self ):
		if ( self.showAlpha() ):
			return QRect( ColorPickerWidget.BarWidth + 7, self.height() - ColorPickerWidget.BarWidth - 2, self.width() - ColorPickerWidget.BarWidth - 8, ColorPickerWidget.BarWidth )
		return QRect()
	
	def color( self ):
		return QColor.fromHsv( self.hue(), self.saturation(), self.lightness(), self.alpha() )
	
	def colorRect( self ):
		if ( self.showAlpha() ):
			return QRect( ColorPickerWidget.BarWidth + 7, 1, self.width() - ColorPickerWidget.BarWidth - 8, self.height() - ColorPickerWidget.BarWidth - 8 )
		else:
			return QRect( ColorPickerWidget.BarWidth + 7, 1, self.width() - ColorPickerWidget.BarWidth - 8, self.height() - 2 )
	
	def emitColorChanged( self, color ):
		if ( not self.signalsBlocked() ):
			self.colorChanged.emit( color )
	
	def hue( self ):
		return self._hue
	
	def huePercent( self ):
		return self._hue / 359.0
	
	def hueRect( self ):
		if ( self.showAlpha() ):
			return QRect( 1, 1, ColorPickerWidget.BarWidth, self.height() - ColorPickerWidget.BarWidth - 8 )
		else:
			return QRect( 1, 1, ColorPickerWidget.BarWidth, self.height() - 2 )
	
	def lightness( self ):
		return self._lightness
	
	def mousePressEvent( self, event ):
		# edit the hue
		r = self.hueRect()
		if ( r.contains( event.pos() ) ):
			self._editing = 'hue'
			self.setHueFromPoint( event.pos() )
			return QWidget.mousePressEvent( self, event )
		
		# edit the alpha
		r = self.alphaRect()
		if ( r.contains( event.pos() ) ):
			self._editing = 'alpha'
			self.setAlphaFromPoint( event.pos() )
			return QWidget.mousePressEvent( self, event )
	
		# edit the color
		r = self.colorRect()
		if ( r.contains( event.pos() ) ):
			self._editing = 'color'
			self.setSaturationAndLightnessFromPoint( event.pos() )
			return QWidget.mousePressEvent( self, event )
		
		return QWidget.mousePressEvent( self, event )
	
	def mouseMoveEvent( self, event ):
		# edit the color
		if ( self._editing == 'color' ):
			self.setSaturationAndLightnessFromPoint( event.pos() )
		
		# edit the alpha
		elif ( self._editing == 'alpha' ):
			self.setAlphaFromPoint( event.pos() )
		
		# edit the hue
		elif ( self._editing == 'hue' ):
			self.setHueFromPoint( event.pos() )
		
		return QWidget.mouseMoveEvent( self, event )
	
	def mouseReleaseEvent( self, event ):
		if ( self._editing and not self.signalsBlocked() ):
			self.editingFinished.emit()
			
		self._editing = None
		
		return QWidget.mouseReleaseEvent( self,event )
	
	def paintEvent( self, event ):
		painter = QPainter()
		painter.begin( self )
		
		painter.setPen( Qt.black )
		
		# create the hue rect
		hrect = self.hueRect()
		
		# create the hue gradient
		grad = QLinearGradient()
		grad.setStart( 0, hrect.top() )
		grad.setFinalStop( 0, hrect.bottom() )
		
		for i in range( 10 ):
			perc = i / 10.0
			grad.setColorAt( perc, QColor.fromHsv( perc * 360, 255, 255 ) )
		
		grad.setColorAt( 1.0, QColor.fromHsv( 359, 255, 255 ) )
			
		painter.setBrush( grad )
		painter.drawRect( hrect )
		
		# create the hue line
		y = (hrect.y() + 2) + self.huePercent() * (hrect.height() - 3)
		pen = painter.pen()
		pen.setColor( Qt.white )
		pen.setWidth( 2 )
		painter.setPen( pen )
		painter.drawLine( hrect.left() + 2, y, hrect.right(), y )
		painter.setPen( Qt.black )
		
		# create the alpha rect
		if ( self.showAlpha() ):
			arect = self.alphaRect()
			
			# create the alpha gradient
			grad = QLinearGradient()
			grad.setStart( arect.left(), 0 )
			grad.setFinalStop( arect.right(), 0 )
			grad.setColorAt( 0.0, QColor( Qt.white ) )
			grad.setColorAt( 1.0, QColor( Qt.black ) )
			painter.setBrush( grad )
			painter.drawRect( arect )
		
			# create the alpha line
			x = (arect.x() + 2) + (1 - self.alphaPercent()) * (arect.width() - 3)
			pen = painter.pen()
			pen.setColor( Qt.yellow )
			pen.setWidth( 2 )
			painter.setPen( pen )
			painter.drawLine( x, arect.top() + 2, x, arect.bottom() )
			painter.setPen( Qt.black )
		
		crect = self.colorRect()
		
		# create the color scale gradient
		grad = QLinearGradient()
		grad.setStart( crect.left(), 0 )
		grad.setFinalStop( crect.right(), 0 )
		grad.setColorAt( 0.0, QColor( 255, 255, 255, self.alpha() ) )
		grad.setColorAt( 1.0, QColor.fromHsv( self.hue(), 255, 255, self.alpha() ) )
		painter.setBrush( grad )
		painter.drawRect( crect )
		
		# create the grayscale gradient
		grad = QLinearGradient()
		grad.setStart( 0, crect.top() )
		grad.setFinalStop( 0, crect.bottom() )
		grad.setColorAt( 0.0, QColor( 0, 0, 0, 0 ) )
		grad.setColorAt( 1.0, QColor( 0, 0, 0, self.alpha() ) )
		painter.setBrush( grad )
		painter.drawRect( crect )
		
		# create the color location
		x = crect.x() + (self.saturation() / 255.0) * crect.width()
		y = crect.y() + (1 - (self.lightness() / 255.0)) * crect.height()
		
		painter.setPen( Qt.black )
		painter.setBrush( QColor( 255, 255, 255, 128 ) )
		
		painter.setClipRect( crect )
		painter.setRenderHint( QPainter.Antialiasing )
		painter.drawEllipse( QPoint( x, y ), 5, 5 )
			
		painter.end()
	
	def saturation( self ):
		return self._saturation
	
	def setAlphaFromPoint( self, point ):
		rect	= self.alphaRect()
		rmin	= rect.left()
		rmax	= rect.right()
		ex		= point.x()
		
		if ( ex < rmin ):
			self._alpha = 255
		elif ( rmax < ex ):
			self._alpha = 0
		else:
			self._alpha = (1 - (float( ex - rmin ) / float( rmax - rmin ))) * 255
		
		self.emitColorChanged( self.color() )
		
		self.repaint()
	
	@pyqtSlot(QColor)
	def setColor( self, color ):
		self._alpha 		= color.alpha()
		self._hue			= color.hue()
		self._lightness		= color.value()
		self._saturation	= color.saturation()
		
		self.repaint()
	
	def setHueFromPoint( self, point ):
		rect	= self.hueRect()
		rmin	= rect.top()
		rmax	= rect.bottom()
		ey		= point.y()
		
		if ( ey < rmin ):
			self._hue = 0
		elif ( rmax < ey ):
			self._hue = 359
		else:
			self._hue = (float( ey - rmin ) / float( rmax - rmin )) * 359
		
		self.emitColorChanged( self.color() )
		
		self.repaint()
	
	def setSaturationAndLightnessFromPoint( self, point ):
		rect	= self.colorRect()
		
		x = point.x()
		y = point.y()
		
		# normalize the x position
		if ( x < rect.x() ):	
			x = 0
		elif ( rect.right() < x ):
			x = rect.width()
		else:
			x -= rect.x()
		
		# normalize the y position
		if ( y < rect.y() ):
			y = 0
		elif ( rect.bottom() < y ):
			y = rect.height()
		else:
			y -= rect.y()
		
		self._saturation 	= ( x / float(rect.width()) ) 			* 255
		self._lightness		= (1 - ( y / float(rect.height()) )) 	* 255
		
		self.emitColorChanged( self.color() )
		
		self.repaint()

	@pyqtSlot(bool)
	def setShowAlpha( self, state ):
		self._showAlpha = state
	
	def showAlpha( self ):
		return self._showAlpha
	
	pyShowAlpha		= pyqtProperty( 'bool', showAlpha, 		setShowAlpha )

class ColorPickerButton( QPushButton ):
	colorPicked 	= pyqtSignal( QColor )
	colorChanged	= pyqtSignal( QColor )
	
	def __init__( self, parent ):
		QPushButton.__init__( self, parent )
		
		self._cancelled		= False
		self._originalColor = None
		self._color 		= QColor( 'black' )
		self._colorPickerWidget = ColorPickerWidget( self )
		self._colorPickerWidget.setWindowFlags( Qt.Popup )
		self._colorPickerWidget.hide()
		self._colorPickerWidget.installEventFilter( self )
		self._colorPickerWidget.resize( 80, 80 )
		self.refresh()
	
		self._colorPickerWidget.colorChanged.connect( self.refresh )
		self.clicked.connect( self.togglePopup )
		
	def color( self ):
		return self._color
	
	def eventFilter( self, object, event ):
		if ( event.type() == event.KeyPress ):
			# cancel the change
			if ( event.key() == Qt.Key_Escape ):
				self._cancelled = True
				self._colorPickerWidget.hide()
				self.refresh()
			
			# accept the color
			elif ( event.key() in ( Qt.Key_Return, Qt.Key_Enter ) ):
				color = self._colorPickerWidget.color()
				self.setColor( color )
				if ( not self.signalsBlocked() ):
					self.colorPicked.emit( color )
				self._colorPickerWidget.hide()
		
		elif ( event.type() == event.Close ):
			# accept the change
			if ( not self._cancelled ):
				color = self._colorPickerWidget.color()
				self.setColor( color )
				if ( not self.signalsBlocked() ):
					self.colorPicked.emit( color )
		
		return False
	
	def refresh( self, color = None ):
		if ( color == None ):
			color = self.color()
			
		palette = self.palette()
		palette.setColor( palette.Button, color )
		self.setPalette( palette )
	
	def setColor( self, color ):
		if ( color == self._color ):
			return False
			
		self._color = color
		self.refresh()	
		
		if ( not self.signalsBlocked() ):
			self.colorChanged.emit( color )
	
	def togglePopup( self ):
		if ( not self._colorPickerWidget.isVisible() ):
			w = self.width()
			if ( w < 120 ):
				w = 120
			
			self._cancelled = False
			self._colorPickerWidget.resize( w, 120 )
			self._colorPickerWidget.move( self.mapToGlobal( QPoint( 0, self.height() ) ) )
			self._colorPickerWidget.setColor( self.color() )
			self._colorPickerWidget.show()
	
def test():
	from blurdev.gui import Dialog
	dlg = Dialog()
	dlg.setWindowTitle( 'Color Test' )
	from PyQt4.QtGui import QVBoxLayout
	layout = QVBoxLayout()
	layout.addWidget( ColorPickerWidget(dlg) )
	layout.addWidget( ColorPickerButton(dlg) )
	dlg.setLayout(layout)
	return dlg

if ( __name__ == '__main__' ):
	from PyQt4.QtGui import QApplication
	app = QApplication([])
	app.setStyle( 'Plastique' )
	dlg = test()
	dlg.show()
	app.exec_()