##
#	\namespace	python.blurdev.gui.dialogs.detailreportdialog
#
#	\remarks	
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		03/11/11
#

from blurdev.gui import Dialog

class DetailReportDialog( Dialog ):
	def __init__( self, parent = None ):
		Dialog.__init__( self, parent )
		
		# load the ui
		import blurdev
		blurdev.gui.loadUi( __file__, self )
		
		self.uiDetailTXT.hide()
		self.uiDetailLBL.linkActivated.connect( self.toggleDetails )
		
		self.adjustSize()
	
	def toggleDetails( self, link ):
		if ( link == 'show_details' ):
			self.uiDetailTXT.show()
			self.uiDetailLBL.setText( '<a href="hide_details">hide details</a>' )
		else:
			self.uiDetailTXT.hide()
			self.uiDetailLBL.setText( '<a href="show_details">show details</a>' )
		
		self.adjustSize()
	
	@staticmethod
	def showReport( parent, title, message, details ):
		dlg = DetailReportDialog(parent)
		dlg.setWindowTitle(title)
		dlg.uiMessageLBL.setText(message)
		dlg.uiDetailTXT.setText(details)
		dlg.exec_()