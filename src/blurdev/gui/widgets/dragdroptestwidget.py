##
#	\namespace	blurdev.gui.widgets
#
#	\remarks	Contains classes for generic widget controls
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		07/09/10
#

from PyQt4.QtGui import QTextEdit

class DragDropTestWidget( QTextEdit ):
	def logEvent( self, event ):
		html = [ '<b>Drop Event</b>' ]
		
		data = event.mimeData()
		
		html.append( '<small><b>source:</b></small> %s' % event.source() )
		html.append( '<hr>' )
		html.append( '<small><b>has color:</b></small>%s' % data.hasColor() )
		html.append( '<small><b>has html:</b></small>%s' % data.hasHtml() )
		html.append( '<small><b>has image:</b></small>%s' % data.hasImage() )
		html.append( '<small><b>has text:</b></small>%s' % data.hasText() )
		html.append( '<small><b>has urls:</b></small>%s' % data.hasUrls() )
		html.append( '<hr>' )
		html.append( '<small><b>text:</b></small>%s' % str(data.text()) )
		html.append( '<small><b>html:</b></small>%s' % str(data.html()) )
		html.append( '<small><b>urls:</b></small><br>%s' % '<br>'.join( [ str( url.toString() ) for url in data.urls() ] ) )
		
		self.setText( '<br>'.join( html ) )
		
	def dragEnterEvent( self, event ):
		event.acceptProposedAction()
	
	def dragMoveEvent( self, event ):
		event.acceptProposedAction()
	
	def dropEvent( self, event ):
		self.logEvent( event )
	
	@staticmethod
	def runTest():
		from blurdev.gui import Dialog
		from PyQt4.QtGui import QVBoxLayout
		
		dlg = Dialog()
		dlg.setWindowTitle( 'Drag Drop Test' )
		
		widget = DragDropTestWidget(dlg)
		
		layout = QVBoxLayout()
		layout.addWidget(widget)
		dlg.setLayout(layout)
		
		dlg.show()