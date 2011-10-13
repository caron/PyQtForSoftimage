##
#	\namespace	python.blurdev.ide.wizards.configwizard.configoptions
#
#	\remarks	Defines the Options Wizard page for the ConfigWizard wizard system
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		11/19/10
#

from PyQt4.QtGui import QWizardPage

class ConfigOptions( QWizardPage ):
	def __init__( self, parent ):
		QWizardPage.__init__( self, parent )
		
		# load the ui
		import blurdev.gui
		blurdev.gui.loadUi( __file__, self )
		
		# register the options field to this widget
		self.registerField( 'options', self )
		
		self._iconFile = ''
		self.uiIconBTN.clicked.connect( self.pickIcon )
	
	def pickIcon( self ):
		from PyQt4.QtGui import QFileDialog
		icon = QFileDialog.getOpenFileName( None, 'Select Icon File', '', 'PNG Files (*.png);;All Files (*.*)' )
		if ( icon ):
			self._iconFile = icon
			from PyQt4.QtGui import QIcon
			self.uiIconBTN.setIcon( QIcon( icon ) )
	
	def validatePage( self ):
		"""
			\remarks	[virtual]	overloaded method from the QWizardPage designed to control whether or not this
									page can be accepted before continuing on with the rest of the wizard
			\return		<bool> success
		"""
		
 		# check to see if the user has entered all required information before continuing
		if ( not (self.uiGroupTXT.text() and self.uiNameTXT.text()) ):
			from PyQt4.QtGui import QMessageBox
			QMessageBox.critical( None, 'Missing Required Fields', 'Not all the required fields have been met.' )
			return False
		
		# define the options dictionary of terms for the template files
		options = {}
		
		# define the option key/value pairings
		options[ 'name' ] 	= self.uiNameTXT.text()
		options[ 'group' ] 	= self.uiGroupTXT.text()
		options[ 'desc' ]	= self.uiDescriptionTXT.toPlainText()
		options[ 'icon' ] 	= self._iconFile
		
		import re
		classname 			= ''.join( re.findall( '[A-Za-z]*', str(self.uiNameTXT.text()) ) ) + 'Config'
		options[ 'class' ] 	= classname
		
		# store the template options for the wizard and let the system move on
		self.setField( 'options', options )
		
		return True