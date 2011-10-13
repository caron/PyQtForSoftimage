##
#	\namespace	blurdev.gui.widgets.progresswidget
#
#	\remarks	The ProgressWidget allows for progress bar and progress spinner widgets to display while loading
#				a user interface
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		01/06/09
#

from PyQt4.QtCore	import Qt
from PyQt4.QtCore	import QEventLoop

from PyQt4.QtGui	import QColor
from PyQt4.QtGui	import QLabel
from PyQt4.QtGui	import QMovie
from PyQt4.QtGui	import QPalette
from PyQt4.QtGui	import QPainter
from PyQt4.QtGui	import QPixmap
from PyQt4.QtGui	import QProgressBar
from PyQt4.QtGui	import QVBoxLayout
from PyQt4.QtGui 	import QWidget

class ProgressSection:
	def __init__( self, parent, total ):
		self._parent 	= parent
		self._total 	= total
		self._index		= 0
	
	def increment( self ):
		self._index += 1
		
	def index( self ):
		return self._index
	
	def isValid( self ):
		return self._total != None
		
	def parent( self ):
		return self._parent
	
	def percent( self, recursive = True ):
		outPercent = 1.0
		
		if ( self._total ):
			outPercent /= self._total
		
		if ( recursive ):
			section = self.parent()
			
			while ( section ):
				outPercent *= section.percent()
				section		= section.parent()
		
		return outPercent
	
	def value( self, recursive = True ):
		if ( recursive ):
			outValue	= 0
			
			section		= self.parent()
			while ( section ):
				outValue	+= 100 * ( section.index() * section.percent() )
				section		= section.parent()
			
			return outValue + ( 100 * self.index() * self.percent() )
		else:
			return ( 100 * self.index() * self.percent( recursive = False ) )

class ProgressBar( QProgressBar ):
	def paintEvent( self, event ):
		painter = QPainter()
		painter.begin( self )
		
		x = ( self.width() - 80 ) / 2 - 2
		y = 0
		w = 80
		h = self.height() - 1
		
		# Draw Percent
		painter.setBrush( Qt.lightGray )
		painter.drawRect( x, ( self.height() - 8 ) / 2, 80 * ( self.value() / 100.0 ), 8 )
		
		# Draw Border
		painter.setBrush( Qt.NoBrush )
		painter.setPen( Qt.gray )
		painter.drawRect( x, ( self.height() - 8 ) / 2, w, 8 )
		
		# Draw Text
		painter.drawText( x + 80, y, 32, h, Qt.AlignRight | Qt.AlignVCenter, '%i%%' % self.value() )
		
		painter.end()

class ProgressWidget( QWidget ):
	def __init__( self, parent ):
		QWidget.__init__( self, parent )
		#-------------------------------------------------------------------------------------------------------------
		
		self._pixmap	= None
		self._sections	= []
		
		#-------------------------------------------------------------------------------------------------------------
		
		self.setAttribute( Qt.WA_DeleteOnClose )
		self.setAutoFillBackground( True )
		
		# Set Colors
		palette = self.palette()
		
		# Set palette
		palette.setColor( QPalette.Window, QColor( 40, 40, 40 ) )
		palette.setColor( QPalette.Base, Qt.gray )
		palette.setColor( QPalette.AlternateBase, Qt.lightGray )
		palette.setColor( QPalette.WindowText, Qt.gray )
		self.setPalette( palette )
		
		# Create Movie Label
		self._movieLabel 	= QLabel( self )
		movie = QMovie( self._movieLabel )
		
		import blurdev
		movie.setFileName( blurdev.resourcePath( 'img/ajax-loader.gif' ) )
		self._movieLabel.setAlignment( Qt.AlignCenter )
		self._movieLabel.setMovie( movie )
		
		# Create Text Label
		self._messageLabel		= QLabel( self )
		self._messageLabel.setAlignment( Qt.AlignCenter )
		self._messageLabel.setText( 'Loading...' )
		
		# Create Secondary Progress Bar
		self._secondaryProgress	= ProgressBar( self )
		self._secondaryProgress.setMaximumHeight( 12 )
		
		# Create Primary Progress Bar
		self._primaryProgress	= ProgressBar( self )
		self._primaryProgress.setMaximumHeight( 12 )
		
		self.setLayout( QVBoxLayout() )
		self.layout().addStretch()
		self.layout().addWidget( self._movieLabel )
		self.layout().addWidget( self._primaryProgress )
		self.layout().addWidget( self._secondaryProgress )
		self.layout().addWidget( self._messageLabel )
		self.layout().addStretch()
		
		#-------------------------------------------------------------------------------------------------------------
		
		self._primaryProgress.hide()
		self._secondaryProgress.hide()
	
	def paintEvent( self, event ):
		painter = QPainter()
		painter.begin( self )
		
		# draw the background
		if ( self._pixmap ):
			painter.drawPixmap( 0, 0, self._pixmap.scaled(self.size()) )
		
		# draw the foreground
		color = QColor( Qt.black )
		color.setAlpha( 180 )
		painter.setBrush(color)
		painter.drawRect(self.rect())
		
		painter.end()
	
	def increment( self ):
		success = False
		
		if ( self._sections ):
			section = self._sections[-1]
			section.increment()
			success = self.update()
		
		return success
	
	def setMessage( self, message ):
		self._messageLabel.setText( message )
	
	def setValue( self, value ):
		self._primaryProgress.setValue( value )
	
	def setTotal( self, total ):
		# Set the total for the progress to calculate
		self._sections = [ ProgressSection( None, total ) ]
		return self.update()
	
	def startMovie( self ):
		self._movieLabel.movie().start()
	
	def startSection( self, total = None, message = '' ):
		if ( self._sections ):
			if ( self._primaryProgress.isVisible() and total ):
				self._secondaryProgress.show()
			self._sections.append( ProgressSection( self._sections[-1], total ) )
		else:
			self._sections.append( ProgressSection( None, total ) )
		
		if ( message ):
			self.setMessage( message )
	
	def stopSection( self ):
		if ( self._sections ):
			self._sections.pop()
	
	def stop( self ):
		self.stopSection()
		if ( not self._sections ):
			# enable all the child widgets
			for child in self.parent().findChildren( QWidget ):
				if ( child != self ):
					child.setUpdatesEnabled(True)
					child.blockSignals(False)
			
			self.parent().blockSignals(False)
			self.close()
			self.setParent( None )
			self.deleteLater()
		
	def total( self ):
		if ( self._sections ):
			return self._sections[0].total()
		return 0
	
	def update( self ):
		success = False
		
		# update the size
		self.resize( self.parent().size() )
		
		# Update the movie
		if ( self._sections and self._sections[0].isValid() ):
			section = self._sections[-1]
			self._primaryProgress.show()
			self._movieLabel.hide()
			self._primaryProgress.setValue( section.value() )
			
			if ( self._secondaryProgress.isVisible() ):
				self._secondaryProgress.setValue( section.value( recursive = False ) )
		else:
			# Update the movie
			self._movieLabel.show()
			self._primaryProgress.hide()
			self._secondaryProgress.hide()
			
			from PyQt4.QtGui import QApplication
			QApplication.instance().processEvents( QEventLoop.ExcludeUserInputEvents )
	
	def value( self ):
		return self._primaryProgress.value()
	
	@staticmethod
	def start( widget, total = None, message = 'Loading...' ):
		if ( not widget ):
			return None
			
		progressWidget 	= widget.findChild( ProgressWidget )
	
		if ( not progressWidget ):
			# Store a pixmap of the widget
			pixmap = QPixmap.grabWidget(widget)
			
			# block the signals and updates
			widget.blockSignals(True)
			for child in widget.findChildren( QWidget ):
				child.setUpdatesEnabled( False )
				child.blockSignals(True)
				
			# create the progress widget
			progressWidget = ProgressWidget( widget )
			progressWidget._pixmap = pixmap
			progressWidget.setTotal( total )
			progressWidget.setValue( 0 )
			progressWidget.setMessage( message )
			progressWidget.startMovie()
			progressWidget.update()
			progressWidget.show()
		else:
			if ( message != 'Loading...' ):
				progressWidget.setMessage( message )
				
			progressWidget.update()
			progressWidget.startSection( total )	
		
		return progressWidget