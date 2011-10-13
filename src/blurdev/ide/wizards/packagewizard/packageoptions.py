##
#	\namespace	python.blurdev.ide.wizards.packagewizard.packageoptions
#
#	\remarks	Defines the Options Wizard page for the PackageWizard wizard system
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		11/19/10
#

from PyQt4.QtGui import QWizardPage

class PackageOptions( QWizardPage ):
	def __init__( self, parent ):
		QWizardPage.__init__( self, parent )
		
		# load the ui
		import blurdev.gui
		blurdev.gui.loadUi( __file__, self )
		
		# register the options field to this widget
		self.registerField( 'options', self )
		
		self.uiModuleTXT.textChanged.connect( self.updateText )
	
	def updateText( self, text ):
		import re
		text = ''.join( re.findall( '[A-Za-z]*', str( text ) ) )
		self.uiModuleTXT.blockSignals(True)
		self.uiModuleTXT.setText( text )
		self.uiModuleTXT.blockSignals(False)
	
	def validatePage( self ):
		"""
			\remarks	[virtual]	overloaded method from the QWizardPage designed to control whether or not this
									page can be accepted before continuing on with the rest of the wizard
			\return		<bool> success
		"""
		
 		# check to see if the user has entered all required information before continuing
		if ( not self.uiModuleTXT.text() ):
			from PyQt4.QtGui import QMessageBox
			QMessageBox.critical( None, 'Missing Required Fields', 'You need to provide a package name.' )
			return False
		
		# define the options dictionary of terms for the template files
		options = {}
		
		# define the option key/value pairings
		options[ 'module' ] = self.uiModuleTXT.text()
		options[ 'desc' ]	= self.uiDescriptionTXT.toPlainText()

		# store the template options for the wizard and let the system move on
		self.setField( 'options', options )
		
		# define components location (optional if you want to create more complex templates)
		if ( self.uiPluginCHK.isChecked() ):
			if ( self.uiPackageCHK.isChecked() and self.uiXmlBasedCHK.isChecked() ):
				self.setField( 'components', 'plugins_packaged_xml' )
			elif ( self.uiPackageCHK.isChecked() ):
				self.setField( 'components', 'plugins_packaged' )
			else:
				self.setField( 'components', 'plugins' )
		else:
			self.setField( 'components', 'default' )
		
		return True