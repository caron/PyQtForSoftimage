##
#	\namespace	[package].[module].[opt_module]
#
#	\remarks	Defines the Options Wizard page for the [class] wizard system
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		[date]
#

from PyQt4.QtGui import QWizardPage

class [opt_class]( QWizardPage ):
	def __init__( self, parent ):
		QWizardPage.__init__( self, parent )
		
		# load the ui
		import blurdev.gui
		blurdev.gui.loadUi( __file__, self )
		
		# register the options field to this widget
		self.registerField( 'options', self )
		
#!		finish loading the options for this wizard page
	
	def validatePage( self ):
		"""
			\remarks	[virtual]	overloaded method from the QWizardPage designed to control whether or not this
									page can be accepted before continuing on with the rest of the wizard
			\return		<bool> success
		"""
		
 		# check to see if the user has entered all required information before continuing
#!		finished = True
#!		if ( not finished ):
#!			from PyQt4.QtGui import QMessageBox
#!			QMessageBox.critical( None, 'Missing Required Fields', 'Not all the required fields have been met.' )
#!			return False
		
		# define the options dictionary of terms for the template files
		options = {}
		
		# define the option key/value pairings
#!		options[ 'name' ] = 'Test'
#!		options[ 'version' ] = 1.0
		
		# store the template options for the wizard and let the system move on
		self.setField( 'options', options )
		
#!		# define components location (optional if you want to create more complex templates)
#!		self.setField( 'components', 'default' )
		
		return True