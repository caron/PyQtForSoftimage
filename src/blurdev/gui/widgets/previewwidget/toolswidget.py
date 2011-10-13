##
#	\namespace	python.blurdev.gui.widgets.previewwidgettoolswidget
#
#	\remarks	Defines the tools side bar widget for the preivew widget utility
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		01/21/11
#

from PyQt4.QtGui import QWidget

class ToolsWidget( QWidget ):
	def __init__( self, parent ):
		# initialize the super class
		QWidget.__init__( self, parent )
		
		# load the ui
		import blurdev
		blurdev.gui.loadUi( __file__, self )
		
		self.setMaximumWidth( 26 )
		scene = parent.scene()
		
		from layerswidget import LayersWidget
		self._layersWidget = LayersWidget( self, scene )
		
		# set the icons
		from PyQt4.QtGui import QIcon
		self.uiNavigateModeBTN.setIcon( 	QIcon( blurdev.resourcePath( 'img/preview/navigate.png' ) ) )
		self.uiSelectionModeBTN.setIcon( 	QIcon( blurdev.resourcePath( 'img/preview/select.png' ) ) )
		self.uiPencilModeBTN.setIcon( 		QIcon( blurdev.resourcePath( 'img/preview/pencil.png' ) ) )
		self.uiBrushModeBTN.setIcon( 		QIcon( blurdev.resourcePath( 'img/preview/brush.png' ) ) )
		self.uiTextBTN.setIcon( 			QIcon( blurdev.resourcePath( 'img/preview/type.png' ) ) )
		self.uiMediaBTN.setIcon( 			QIcon( blurdev.resourcePath( 'img/preview/media.png' ) ) )
		self.uiLayersBTN.setIcon( 			QIcon( blurdev.resourcePath( 'img/preview/layers.png' ) ) )
		
		self.uiForegroundColorBTN.setColor( scene.foregroundColor() )
		self.uiBackgroundColorBTN.setColor( scene.backgroundColor() )
		
		# create connections
		scene.interactionModeChanged.connect( 		self.refreshMode )
		self.uiLayersBTN.clicked.connect(			self.showLayersWidget )
		self.uiNavigateModeBTN.clicked.connect( 	scene.setNavigateMode )
		self.uiSelectionModeBTN.clicked.connect(	scene.setSelectionMode )
		self.uiPencilModeBTN.clicked.connect(		scene.setPencilMode )
		self.uiBrushModeBTN.clicked.connect(		scene.setBrushMode )
		self.uiTextBTN.clicked.connect(				self.createTextLayer )
		self.uiMediaBTN.clicked.connect(			self.createMediaLayer )
		self.uiForegroundColorBTN.colorPicked.connect(	scene.setForegroundColor )
		self.uiBackgroundColorBTN.colorPicked.connect(	scene.setBackgroundColor )
		
		# update the ui
		self.refreshMode()
	
	def createTextLayer( self ):
		return self.parent().scene().createTextLayer()
	
	def createMediaLayer( self ):
		return self.parent().scene().createMediaLayer()
	
	def refreshMode( self ):
		from previewscene import InteractionMode
		
		scene 	= self.parent().scene()
		mode 	= scene.interactionMode()
		self.uiNavigateModeBTN.setChecked(		mode == InteractionMode.Navigate )
		self.uiSelectionModeBTN.setChecked( 	mode == InteractionMode.Selection )
		self.uiPencilModeBTN.setChecked(		mode == InteractionMode.Pencil )
		self.uiBrushModeBTN.setChecked(			mode == InteractionMode.Brush )
	
	def showLayersWidget( self ):
		self._layersWidget.show()