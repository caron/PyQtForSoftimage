##
#	\namespace	blurdev.gui.dialogs.configdialog.configdialog
#
#	\remarks	Defines the ConfigDialog class that is used to display config plugins for the blurdev system
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		04/20/10
#

from blurdev.gui 		import Dialog
from PyQt4.QtGui		import QTreeWidgetItem

class ConfigTreeItem( QTreeWidgetItem ):
	def __init__( self, configSetItem ):
		QTreeWidgetItem.__init__( self, [ configSetItem.objectName() ] )
		
		from PyQt4.QtCore 	import QSize
		from PyQt4.QtGui 	import QIcon
		
		# store the config set item
		self._configSetItem = configSetItem
		
		# set the icon
		self.setIcon( 0, QIcon( configSetItem.icon() ) )
		self.setSizeHint( 0, QSize( 200, 20 ) )
	
	def configSetItem( self ):
		return self._configSetItem

#--------------------------------------------------------------------------------
		
class ConfigDialog( Dialog ):
	def __init__( self, parent ):
		Dialog.__init__( self, parent )
		
		import blurdev.gui
		blurdev.gui.loadUi( __file__, self )
		
		# clear the widget
		widget = self.uiWidgetAREA.takeWidget()
		widget.close()
		widget.setParent(None)
		widget.deleteLater()
		
		# initialize the header
		self.uiPluginsTREE.header().setVisible( False )
		
		# create custom properties
		self._configSet = None
		
		# create connections
		self.uiExitBTN.clicked.connect( 					self.reject )
		self.uiSaveExitBTN.clicked.connect( 				self.accept )
		self.uiResetBTN.clicked.connect(					self.reset )
		self.uiSaveBTN.clicked.connect(						self.commit )
		self.uiPluginsTREE.itemSelectionChanged.connect( 	self.refreshWidget )
	
	def accept( self ):
		""" commits the config information and then closes down """
		if ( self.commit() ):
			Dialog.accept( self )
	
	def checkForSave( self ):
		""" tries to run the active config widget's checkForSave method, if it exists """
		widget = self.uiWidgetAREA.widget()
		
		if ( widget ):
			return widget.checkForSave()
		return True
	
	def commit( self ):
		""" tries to run the active config widget's commit method, if it exists """
		widget = self.uiWidgetAREA.widget()
		if ( widget ):
			widget.recordUi()
			return widget.commit()
		return True
		
	def setConfigSet( self, configSet ):
		""" 
			\remarks	sets the config set that should be edited
			\param		configSet	<blurdev.gui.dialogs.configdialog.ConfigSet>
		"""
		import blurdev
		
		from PyQt4.QtCore	import QSize
		from PyQt4.QtGui 	import QTreeWidgetItem, QIcon
		
		self.uiPluginsTREE.blockSignals( True )
		self.uiPluginsTREE.setUpdatesEnabled( False )
		
		# clear the tree
		self.uiPluginsTREE.clear()
		
		for group in configSet.configGroups():
			# create the group item
			grpItem = QTreeWidgetItem( [ group ] )
			grpItem.setIcon( 0, QIcon( blurdev.resourcePath( 'img/folder.png' ) ) )
			grpItem.setSizeHint( 0, QSize( 200, 20 ) )
			
			# update the font
			font	= grpItem.font(0)
			font.setBold( True )
			grpItem.setFont( 0, font )
			
			# create the config set items
			for configSetItem in configSet.configGroupItems( group ):
				grpItem.addChild( ConfigTreeItem( configSetItem ) )
			
			# add the group item to the tree
			self.uiPluginsTREE.addTopLevelItem( grpItem )
			grpItem.setExpanded( True )
	
		self.uiPluginsTREE.blockSignals( False )
		self.uiPluginsTREE.setUpdatesEnabled( True )
			
	def reject( self ):
		""" checks this system to make sure the current widget has been saved before exiting """
		if ( self.checkForSave() ):
			Dialog.reject( self )
	
	def refreshWidget( self ):
		""" reloads this dialog with the current plugin instance """
		self.uiPluginsTREE.blockSignals( True )
		
		item = self.uiPluginsTREE.currentItem()
		
		if ( isinstance( item, ConfigTreeItem ) ):
			widget = self.uiWidgetAREA.takeWidget()
			
			# clear out an old widget
			if ( widget ):
				# make sure the old widget can be saved
				if ( not widget.checkForSave() ):
					self.uiPluginsTREE.blockSignals( True )
					self.uiPluginsTREE.clearSelection()
					self.uiPluginsTREE.selectItem( widget.objectName() )
					self.uiPluginsTREE.blockSignals( False )
					return False
				
				# close the old widget
				widget.close()
				widget.setParent( None )
				widget.deleteLater()
				
			# create the new widgets plugin
			widget = item.configSetItem().configClass()(self)
			widget.setObjectName( item.configSetItem().objectName() )
			self.uiWidgetAREA.setWidget( widget )
		
		return True
	
	def reset( self ):
		""" resets the data for the current widget """
		widget = self.uiWidgetAREA.widget()
		
		if ( widget ):
			widget.reset()
			widget.refreshUi()
			
		return True
	
	def selectItem( self, name ):
		""" selects the widget item whose name matches the inputed name """
		# go through the group level
		for i in range( self.uiPluginsTREE.topLevelItemCount() ):
			item = self.uiPluginsTREE.topLevelItem(i)
			
			# go through the config level
			for c in range( item.childCount() ):
				pitem = item.child(c)
				
				# select the item if the name matches
				if ( pitem.text(0) == name ):
					pitem.setSelected( True )
					return True
					
		return False
	
	@staticmethod
	def edit( configSet, parent = None ):
		""" 
			\remarks 	creates a modal config dialog using the specified plugins 
			\param		configSet	<blurdev.gui.dialogs.configdialog.ConfigSet>
		"""
		dialog = ConfigDialog( parent )
		dialog.setConfigSet( configSet )
		return dialog.exec_()
	