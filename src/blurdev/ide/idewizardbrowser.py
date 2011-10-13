##
#	\namespace	blurdev.ide.idewizardbrowser
#
#	\remarks	This dialog allows the user to create new python classes and packages based on plugin wizards
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		08/19/10
#

from blurdev.gui import Dialog

class IdeWizardBrowser( Dialog ):
	def __init__( self, parent ):
		Dialog.__init__( self, parent )
		
		# load the ui
		import blurdev.gui
		blurdev.gui.loadUi( __file__, self )
		
		# import the wizards
		import wizards
		
		from PyQt4.QtGui import QIcon
		folder = QIcon( blurdev.resourcePath( 'img/folder.png' ) )
		
		from PyQt4.QtCore import Qt, QSize
		from PyQt4.QtGui import QTreeWidgetItem
		for lang in wizards.wizardLanguages():
			item = QTreeWidgetItem( [ lang ]  )
			item.setSizeHint( 0, QSize( 250, 23 ) )
			item.setIcon( 0, folder )
			
			for grp in wizards.wizardGroups(lang):
				gitem = QTreeWidgetItem( [grp] )
				gitem.setSizeHint( 0, QSize( 250, 23 ) )
				gitem.setIcon( 0, QIcon( blurdev.resourcePath( 'img/%s.png' % grp ) ) )
				item.addChild( gitem )
			
			self.uiWizardTREE.addTopLevelItem(item)
			item.setExpanded(True)
	
		# create the thumbnail scene
		from blurdev.gui.scenes.thumbnailscene import ThumbnailScene
		thumbscene = ThumbnailScene(self.uiWizardsVIEW)
		self.uiWizardsVIEW.setVerticalScrollBarPolicy( Qt.ScrollBarAlwaysOff )
		
		thumbscene.setLayoutDirection( Qt.Horizontal )
		thumbscene.setThumbnailSize( QSize( 48, 48 ) )
		
		self.uiWizardsVIEW.setScene( thumbscene )
		self.uiWizardTREE.itemSelectionChanged.connect( self.refreshWizards )
		thumbscene.selectionChanged.connect( self.refreshDescription )
		thumbscene.itemDoubleClicked.connect( self.runWizard )
	
	def currentWizard( self ):
		items = self.uiWizardsVIEW.scene().selectedItems()
		if ( items ):
			item = items[0]
			from PyQt4.QtCore import Qt
			
			import wizards
			return wizards.find(item.data( Qt.UserRole ).toString())
		return None
	
	def refreshDescription( self ):
		templ = self.currentWizard()
		if ( templ ):
			self.uiDescriptionLBL.setText( templ.desc )
		else:
			self.uiDescriptionLBL.setText( '' )
	
	def refreshWizards( self ):
		scene = self.uiWizardsVIEW.scene()
		scene.clear()
		self.uiDescriptionLBL.setText( '' )
		
		item = self.uiWizardTREE.currentItem()
		if ( not (item and item.parent()) ):
			return
		
		import wizards
		from PyQt4.QtCore import Qt
		templs = wizards.wizards(item.parent().text(0),item.text(0))
		for templ in templs:
			item = scene.addThumbnail(templ.iconFile)
			item.setCaption(templ.name)
			item.setToolTip(templ.toolTip)
			item.setData( Qt.UserRole, templ.wizardId )
		
		scene.recalculate(scene.sceneRect(), True )
		
	def runWizard( self ):
		templ = self.currentWizard()
		if ( templ ):
			if ( templ.runWizard() ):
				self.accept()
		
	@staticmethod
	def createFromWizard():
		import blurdev
		if ( IdeWizardBrowser( blurdev.core.activeWindow() ).exec_() ):
			return True
		return False