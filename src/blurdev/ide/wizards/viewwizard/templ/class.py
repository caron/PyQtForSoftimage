##
#	\namespace	[package].[class::lower]
#
#	\remarks	The main View class for the [name] Trax View
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		[date]
#

from PyQt4.QtGui import QWidget

class [class]( QWidget ):
	def __init__( self, parent ):
		QWidget.__init__( self, parent )
		
		# create the ui controls
#!		from PyQt4.QtGui import QTreeWidget, QTreeWidgetItem, QVBoxLayout
#!		layout = QVBoxLayout()
#!		widget = QTreeWidget(self)
#!		widget.addTopLevelItem( QTreeWidgetItem( [ 'Test' ] ) )
#!		layout.addWidget( widget )
#!		self.setLayout( layout )