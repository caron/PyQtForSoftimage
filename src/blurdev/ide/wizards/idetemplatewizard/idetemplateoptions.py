##
#	\namespace	[FILENAME]
#
#	\remarks	[ADD REMARKS]
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		11/01/10
#

from PyQt4.QtGui import QWizardPage

class IDETemplateOptions( QWizardPage ):
	def __init__( self, parent ):
		QWizardPage.__init__( self, parent )
		
		# load the ui
		import blurdev.gui
		blurdev.gui.loadUi( __file__, self )
		
		# register the options field to this widget
		self.registerField( 'options', self )
		
		# load the languages from the lexers
		from blurdev.ide import lexers
		self.uiLanguageDDL.addItems( [ '' ] + lexers.languages() )
		
		self._iconFile = ''
		self.uiIconBTN.clicked.connect( self.pickIcon )
	
	def pickIcon( self ):
		from PyQt4.QtGui import QFileDialog
		filename = QFileDialog.getOpenFileName( None, 'Select Icon File', self._iconFile, 'PNG Files (*.png);;All Files (*.*)' )
		if ( filename ):
			self._iconFile = str(filename)
			
			from PyQt4.QtGui import QIcon
			self.uiIconBTN.setIcon( QIcon( filename ) )
	
	def validatePage( self ):
		if ( not (self.uiLanguageDDL.currentText() and self.uiGroupTXT.text() and self.uiNameTXT.text()) ):
			from PyQt4.QtGui import QMessageBox
			QMessageBox.critical( None, 'Missing Fields', 'You need to provide at least a Language, Group, and Name for your IDE Wizard.' )
			return False
		
		# set the template options
		options = {}
		options[ 'language' ] 	= self.uiLanguageDDL.currentText()
		options[ 'group' ] 		= self.uiGroupTXT.text()
		options[ 'name' ] 		= self.uiNameTXT.text()
		options[ 'tooltip' ] 	= self.uiTooltipTXT.text()
		options[ 'desc' ] 		= self.uiDescriptionTXT.toPlainText()
		options[ 'icon' ] 		= self._iconFile
		
		# define some of the additional options
		import re
		options[ 'opt_class' ]	= '%sOptions' % ''.join( re.findall( '[A-Za-z]', str( self.uiNameTXT.text() ) ) )
		options[ 'opt_module' ] = options['opt_class'].lower()
		
		options[ 'class' ]		= '%sWizard' % ''.join( re.findall( '[A-Za-z]', str( self.uiNameTXT.text() ) ) )
		options[ 'module' ] 	= options['class'].lower()
		
		self.setField( 'options', options )
			
		return True