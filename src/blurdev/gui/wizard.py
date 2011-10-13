##
#	\namespace	blurdev.gui.wizard
#
#	\remarks	Defines the main Wizard instance for this system
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		12/05/08
#

from PyQt4.QtGui 	import QWizard

class Wizard( QWizard ):
	def __init__( self, parent = None, flags = 0 ):
		import blurdev
		
		# if there is no root, create 
		if ( not parent ):
			if ( blurdev.core.isMfcApp() ):
				from winwidget import WinWidget
				parent = WinWidget.newInstance(blurdev.core.hwnd())
			else:
				parent = blurdev.core.rootWindow()
			
		# create a QWizard
		if ( flags ):
			QWizard.__init__( self, parent, flags )
		else:
			QWizard.__init__( self, parent )
		
		# use the default palette
		palette = blurdev.core.defaultPalette()
		if ( palette ):
			self.setPalette( palette )
		
		# set the delete attribute to clean up the window once it is closed
		from PyQt4.QtCore import Qt
		self.setAttribute( Qt.WA_DeleteOnClose )
	
		# set this property to true to properly handle tracking events to control keyboard overrides
		self.setMouseTracking( True )
		
		self.initWizardStyle()
	
	def initWizardStyle( self ):
		# set the window title
		self.setWizardStyle( QWizard.MacStyle )
		
		import blurdev
		from PyQt4.QtGui import QPixmap
		self.setPixmap( QWizard.BackgroundPixmap, QPixmap( blurdev.resourcePath( 'img/watermark.png' ) ) )
		
		self.initWizardPages()
	
	def initWizardPages( self ):
		pass
	
	def closeEvent( self, event ):
		QWizard.closeEvent( self, event )
		
		# uncache the win widget if necessary
		from PyQt4.QtCore import Qt
		if ( self.testAttribute( Qt.WA_DeleteOnClose ) ):
			if ( self.parent() and self.parent().inherits( 'QWinWidget' ) ):
				from winwidget import WinWidget
				WinWidget.uncache( self.parent() )
	
	def exec_( self ):
		# do not use the DeleteOnClose attribute when executing a wizard as often times a user will be accessing
		# information from the wizard instance after it closes.  This function properly transfers ownership of the
		# wizard instance back to Python anyway
		from PyQt4.QtCore	import Qt
		self.setAttribute( Qt.WA_DeleteOnClose, False )
		
		# execute the wizard
		return QWizard.exec_( self )
	
	@classmethod
	def runWizard( cls, parent = None ):
		if ( cls(parent).exec_() ):
			return True
		return False