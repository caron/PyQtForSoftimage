##
#	\namespace	Treegrunt.delegates
#
#	\remarks	Defines common item delegates for this system
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		08/07/09
#

from PyQt4.QtGui import QItemDelegate

#-------------------------------------------------------------------------------------------------------------

class GridDelegate( QItemDelegate ):
	def __init__( self, parent, gridColor = None ):
		
		QItemDelegate.__init__( self, parent )
		from PyQt4.QtGui 	import QPen, QColor
		from PyQt4.QtCore	import Qt
		
		if ( gridColor == None ):
			gridColor = QColor( 60, 60, 60 )
		
		# store the pen for the grid
		self._editor	= None
		self._pen		= QPen( Qt.SolidLine )
		self._pen.setColor( gridColor )
		
		# store the custom properties
		self._showColumnBorders = True
		self._showTree			= True
	
	def clearEditor( self ):
		"""
			\remarks	clears the reference to this editor
		"""
		try:
			self._editor.close()
			self._editor.deleteLater()
		except:
			pass
		
		self._editor = None
		
	def createEditor( self, parent, option, index ):
		"""
			\remarks	overloaded from QItemDelegate, creates a new editor for the inputed widget
			\param		parent	<QWidget>
			\param		option	<QStyleOptionViewItem>
			\param		index	<QModelIndex>
			\return		<QWidget> editor
		"""
		from PyQt4.QtCore 	import Qt
		from PyQt4.QtGui 	import QLineEdit
		
		# clear out the old editor
		self.clearEditor()
		self._editor = QLineEdit( parent )
		self._editor.setFocus()
		self._editor.setFocusPolicy( Qt.StrongFocus )
		
		return self._editor
		
	def drawCheck( self, painter, option, rect, state ):
		from PyQt4.QtCore import Qt
		from PyQt4.QtGui import QFont
		if ( state == Qt.Checked ):
			font = QFont( 'Webdings' )
			font.setPointSize( 16 )
			painter.setFont( font )
			painter.setPen( Qt.gray )
			painter.drawText( rect, Qt.AlignCenter, 'a' )
			
	def drawGrid( self, painter, style, index ):
		""" draw gridlines for this item """
		from PyQt4.QtCore 	import Qt, QLine
		
		data = index.model().data( index, Qt.UserRole )
		
		# clear the brush & set the painter pen
		painter.setBrush( Qt.NoBrush )
		painter.setPen( self.pen() )
		
		# draw the lines
		lines = []
		
		# add the column line
		if ( self.showColumnBorders() ):
			lines.append( QLine( style.rect.right(), style.rect.y(), style.rect.right(), style.rect.bottom() ) )
		
		# determine if this line should be drawn to the 0 mark
		x = style.rect.x()
		if ( not (self.showTree() or index.column()) ):
			x = 0
		elif ( not index.column() and x ):
			lines.append( QLine( x, style.rect.y(), x, style.rect.bottom() ) )
		
		# add the bottom line
		lines.append( QLine( x, style.rect.bottom(), style.rect.right(), style.rect.bottom() ) )
		
		painter.drawLines( lines )
	
	def editor( self ):
		"""
			\remarks	returns the current editor for this delegate
			\return		<QWidget> || None
		"""
		return self._editor
	
	def gridColor( self ):
		""" returns the color for the current pen """
		return self._pen.color()
	
	def paint( self, painter, option, index ):
		""" draw the delegate and the grid """
		QItemDelegate.paint( self, painter, option, index )
		self.drawGrid( painter, option, index )
	
	def pen( self ):
		""" returns this delegates pen """
		return self._pen
	
	def setGridColor( self, color ):
		""" sets the pen color for this delegate """
		from PyQt4.QtGui import QColor
		self._pen.setColor( QColor( color ) )
	
	def setPen( self, pen ):
		""" sets the current grid delegate pen """
		from PyQt4.QtGui import QPen
		
		self._pen = QPen( pen )
	
	def setShowColumnBorders( self, state = True ):
		""" sets whether or not column borders are drawn """
		self._showColumnBorders = state
	
	def setShowTree( self, state = True ):
		""" sets whether or not the delegate show a tree """
		self._showTree = state
	
	def showColumnBorders( self ):
		""" returns if this item shows the column divider """
		return self._showColumnBorders
	
	def showTree( self ):
		""" returns if this item shows a tree """
		return self._showTree

#-------------------------------------------------------------------------------------------------------------

class PixmapCheckDelegate( GridDelegate ):
	""" QItemDelegate designed to show a pixmap when toggled on/off """
	def __init__( self, parent, checked, unchecked, size = 12 ):
		"""
			\remark		Initializes the checkbox system with the checked/unchecked images
			\param		parent		<QObject>
			\param		checked		<filename>		location of the checked pixmap
			\param		unchecked	<filename>		location of the unchecked pixmap
			\param		size		<int>			the size to scale the icons
		"""
		GridDelegate.__init__( self, parent )
		
		from PyQt4.QtGui import QPixmap
		self._checkedMap 	= QPixmap( checked ).scaled( size, size )
		self._uncheckedMap 	= QPixmap( unchecked ).scaled( size, size )
	
	def checkedMap( self ):
		""" returns the checked pixmap for this delegate """
		return self._checkedMap
	
	def drawCheck( self, painter, option, rect, state ):
		""" overloaded QItemDelegate.drawCheck method to handle the drawing of the checkbox to paint the pixmaps """
		if ( rect.isValid() ):
			from PyQt4.QtCore import Qt
			if ( state == Qt.Checked ):
				painter.drawPixmap( rect.x(), rect.y(), self.checkedMap() )
			else:
				painter.drawPixmap( rect.x(), rect.y(), self.uncheckedMap() )
		
	def uncheckedMap( self ):
		""" returns the unchecked pixmap for this delegate """
		return self._uncheckedMap
