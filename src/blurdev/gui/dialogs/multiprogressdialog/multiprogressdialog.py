##
#	\namespace	python.blurdev.gui.dialogs.multiprogressdialog
#
#	\remarks	
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		03/14/11
#

from PyQt4.QtCore import pyqtSignal
from blurdev.gui import Dialog

class MultiProgressDialog( Dialog ):
	closed = pyqtSignal()
	
	_instance = None
	
	def __init__( self, parent = None ):
		Dialog.__init__( self, parent )
		
		# load the ui
		import blurdev
		blurdev.gui.loadUi( __file__, self )
		
		self._shutdown			= False
		self._cancelled			= False
		self._errored 			= False
		self._overriddenCursor	= False
		self._stackCount		= 1
		
		# create the columns
		self.uiProgressTREE.setColumnCount(2)
		header = self.uiProgressTREE.header()
		header.setResizeMode( 0, header.Stretch )
		header.setResizeMode( 1, header.ResizeToContents )
		
		# create connections
		self.uiProgressTREE.currentItemChanged.connect( self.updateOptions )
		self.uiDetailsCHK.toggled.connect( self.adjustSize )
		self.uiDialogBTNS.accepted.connect( self.close )
		self.uiDialogBTNS.rejected.connect( self.cancel )		# assumes there is a uiDialogBTNS in the ui file
	
	def addSection( self, name, count = 100, value = -1, allowsCancel = False ):
		self.uiProgressTREE.blockSignals(True)
		self.uiProgressTREE.setUpdatesEnabled(False)
		
		from blurdev.gui.dialogs.multiprogressdialog import ProgressSection
		section = ProgressSection( name, count = count, value = value, allowsCancel = allowsCancel )
		self.uiProgressTREE.addTopLevelItem(section)
		
		self.uiProgressTREE.blockSignals(False)
		self.uiProgressTREE.setUpdatesEnabled(True)
		
		self.update()
		
		return section
	
	def applyOverrideCursor( self ):
		# make sure we restore the override the cursor
		if ( not self._overriddenCursor ):
			from PyQt4.QtCore 	import Qt
			from PyQt4.QtGui 	import QApplication
			
			QApplication.setOverrideCursor( Qt.WaitCursor )
			self._overriddenCursor = True
	
	def cancel( self ):
		item = self.uiProgressTREE.currentItem()
		if ( item ):
			item.cancel()
	
	def clear( self ):
		self.uiProgressTREE.blockSignals(True)
		self.uiProgressTREE.setUpdatesEnabled(False)
		
		self.uiProgressTREE.clear()
		self._errored = False
		
		self.uiProgressTREE.blockSignals(False)
		self.uiProgressTREE.setUpdatesEnabled(True)
	
	def clearOverrideCursor( self ):
		# make sure we restore the override the cursor
		if ( self._overriddenCursor ):
			from PyQt4.QtGui import QApplication
			QApplication.restoreOverrideCursor()
			self._overriddenCursor = False
	
	def closeEvent( self, event ):
		from PyQt4.QtCore import Qt
		from PyQt4.QtGui import QApplication
		
		if ( not QApplication.instance().keyboardModifiers() == Qt.ShiftModifier ):
			if ( not (self._errored or self._shutdown) ):
				event.ignore()
				return
			
		self.clearOverrideCursor()
		self.closed.emit()
		Dialog.closeEvent( self, event )
		
	def complete( self ):
		self._stackCount -= 1
		if ( self._stackCount < 0 ):
			self._stackCount = 0
		
		if ( not self._stackCount ):
			self.shutdown()
		
	def errored( self ):
		return self._errored
	
	def incrementStack( self ):
		self._stackCount += 1
	
	def finish( self ):
		for i in range( self.uiProgressTREE.topLevelItemCount() ):
			item = self.uiProgressTREE.topLevelItem(i)
			item._value = item._count - 1
		
		self.update()
	
	def reset( self, items ):
		self.uiProgressTREE.blockSignals(True)
		self.uiProgressTREE.setUpdatesEnabled(False)
		
		self.uiProgressTREE.clear()
		for item in items:
			self.uiProgressTREE.addTopLevelItem(item)
		
		self.uiMainPBAR.setValue(0)
		self.uiItemPBAR.setValue(0)
		
		self.uiProgressTREE.blockSignals(False)
		self.uiProgressTREE.setUpdatesEnabled(True)
	
	def section( self, name ):
		for i in range( self.uiProgressTREE.topLevelItemCount() ):
			item = self.uiProgressTREE.topLevelItem(i)
			if ( item.text(0) == name ):
				return item
		return None
	
	def sectionUpdated( self, sectionName, percent, message = '' ):
		section = self.section(sectionName)
		if ( section ):
			section.setPercentComplete(percent)
			section.setMessage(message)
			self.update()
	
	def sectionErrored( self, sectionName, error ):
		section = self.section(sectionName)
		if ( section ):
			section.setErrorText(error)
			self.update()
	
	def show( self ):
		Dialog.show( self )
		
		from PyQt4.QtGui import QApplication
		QApplication.processEvents()
		
	def shutdown( self ):
		self._shutdown = True
		self.close()
		
	def update( self ):
		if ( self._shutdown ):
			return
			
		# we need to force the events to process to check if the user pressed the cancel button since this is not multi-threaded
		from PyQt4.QtGui import QApplication
		QApplication.processEvents()
		
		# update the progress
		tree 	= self.uiProgressTREE
		
		citem			= tree.currentItem()
		count 			= tree.topLevelItemCount()
		message			= ''
		completeCount	= 0.0
		secondaryPerc	= 0
		self._errored	= False
		self.uiDialogBTNS.setStandardButtons( self.uiDialogBTNS.Cancel )
		
		for i in range( count ):
			item = tree.topLevelItem(i)
			
			# if the item has accepted a user cancel, stop the progress dialog
			if ( item.cancelAccepted() ):
				self.shutdown()
				return
			
			# convert an errored item to a message box style system
			elif ( item.errored() ):
				self.uiDialogBTNS.setStandardButtons( self.uiDialogBTNS.Ok )
				self._errored = True
			
			# calculate overall percent complete for completed items
			if ( item.completed() ):
				completeCount += 1
				continue
			
			# calculate the secondary percentage
			iperc = item.percentComplete()
			completeCount += 1 * iperc
			
			if ( item == citem ):
				secondaryPerc = 100 * iperc
				message = item.message()
		
		if ( count < 1 ):
			count = 1
		
		self.uiMessageLBL.setText(message)
		self.uiMainPBAR.setValue( 100 * (completeCount / count) )
		self.uiItemPBAR.setValue( secondaryPerc )
		self.updateOptions()
		
		if ( self._errored ):
			self.clearOverrideCursor()
		else:
			self.applyOverrideCursor()
		
		# close out when all items are finished
		if ( self.uiMainPBAR.value() == 100 ):
			self.shutdown()
	
	def updateOptions( self ):
		item = self.uiProgressTREE.currentItem()
		if ( item ):
			self.uiDialogBTNS.setEnabled(item.allowsCancel() or self.errored())
		else:
			self.uiDialogBTNS.setEnabled(self.errored())
	
	@staticmethod
	def clearInstance():
		if ( MultiProgressDialog._instance ):
			Dialog.closeEvent( MultiProgressDialog._instance, None )
			MultiProgressDialog._instance.setParent(None)
			MultiProgressDialog._instance.deleteLater()
			MultiProgressDialog._instance = None
	
	@staticmethod
	def start( title = 'Progress', parent = None ):
		if ( MultiProgressDialog._instance ):
			MultiProgressDialog._instance.incrementStack()
		else:
			inst = MultiProgressDialog(parent)
			inst.setWindowTitle(title)
			inst.show()
			inst.closed.connect( MultiProgressDialog.clearInstance )
			
			MultiProgressDialog._instance = inst
			from PyQt4.QtCore import Qt
			inst.setAttribute( Qt.WA_DeleteOnClose, False )
		
		return MultiProgressDialog._instance