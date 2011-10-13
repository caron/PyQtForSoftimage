##
#	\namespace	python.blurdev.gui.widgetspreviewgraphicsview
#
#	\remarks	Creates a previewing system for media files
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		01/21/11
#

from PyQt4.QtGui import QWidget

class PreviewWidget( QWidget ):
	def __init__( self, parent ):
		# initialize the super class
		QWidget.__init__( self, parent )
		
		# create the QGraphicsView
		from PyQt4.QtGui import QGraphicsView, QVBoxLayout
		self._view = QGraphicsView( self )
		
		layout = QVBoxLayout()
		layout.setContentsMargins(0,0,0,0)
		layout.addWidget(self._view)
		self.setLayout(layout)
		
		# create the scene
		from previewscene import PreviewScene
		self._view.setScene( PreviewScene( self._view ) )
		
		# create the tools widget
		from toolswidget import ToolsWidget
		self._toolsWidget = ToolsWidget( self._view )
		
		# update the geometry
		self.updateGeometry()
	
	def scene( self ):
		return self._view.scene()
	
	def resizeEvent( self, event ):
		QWidget.resizeEvent( self, event )
		self.updateGeometry()
	
	def updateGeometry( self ):
		# update the tools widget
		self._toolsWidget.move( 5, 5 )
		self._toolsWidget.resize( self._toolsWidget.width(), self.height() - 10 )
	