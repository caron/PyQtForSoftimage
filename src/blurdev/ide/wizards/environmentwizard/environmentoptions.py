##
#	\namespace	python.blurdev.ide.wizards.environmentwizard.environmentoptions
#
#	\remarks	Defines the Options Wizard page for the EnvironmentWizard wizard system
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		03/01/11
#

from PyQt4.QtGui import QWizardPage

class EnvironmentOptions( QWizardPage ):
	def __init__( self, parent ):
		QWizardPage.__init__( self, parent )
		
		# load the ui
		import blurdev.gui
		blurdev.gui.loadUi( __file__, self )
		
		# register the options field to this widget
		self.registerField( 'options', self )
		
	def validatePage( self ):
		"""
			\remarks	[virtual]	overloaded method from the QWizardPage designed to control whether or not this
									page can be accepted before continuing on with the rest of the wizard
			\return		<bool> success
		"""
		
 		# check to see if the user has entered all required information before continuing
		if ( not self.uiEnvironmentTXT.text() ):
			from PyQt4.QtGui import QMessageBox
			QMessageBox.critical( None, 'Missing Required Fields', 'You need to provide an environment name.' )
			return False
		
		# define the options dictionary of terms for the template files
		options = {}
		
		# define the option key/value pairings
		options[ 'environment' ] 	= self.uiEnvironmentTXT.text()
		options[ 'development' ] 	= self.uiDevelopmentCHK.isChecked()
		options[ 'default' ]		= self.uiDefaultCHK.isChecked()
		
		# store the template options for the wizard and let the system move on
		self.setField( 'options', options )
		
		return True