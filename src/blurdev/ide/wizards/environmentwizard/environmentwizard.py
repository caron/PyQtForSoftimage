##
#	\namespace	python.blurdev.ide.wizards.environmentwizard.environmentwizard
#
#	\remarks	Defines the main Wizard class for the EnvironmentWizard wizard system
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		03/01/11
#

from blurdev.gui import Wizard

class EnvironmentWizard( Wizard ):
	def initWizardPages( self ):
		"""
			\remarks	[virtual]	Initialize the wizards pages with any additional options in custom WizardPages you want for your wizard
									When definining a new Wizard for the Blur IDE system, you can set 2 fields defined in the IdeWizardPreviewPage:
									
									mypage.setField( 'options', { 'module': 'mypagewizard' )
									
									You should always set the options field to a <dict> { <str> option: <str> value } that will be used when the wizard
									generates.
									
									mypage.setField( 'components', 'dialog_ui' )
									
									The second field is optional, and is used to override the default components XML file that the wizard system uses.  This is
									useful to switch the structure of your wizard based on some user defined options.
			\return		<void>
		"""
		self.setWindowTitle( 'Environment Wizard' )
		
		# create the main options page
		from environmentoptions import EnvironmentOptions
		self.addPage( EnvironmentOptions( self ) )
		
		# create any additional pages
#!		from some_module import some_class
#!		self.addPage( some_class( self ) )
		
		# create the wizard creation page
		from blurdev.ide.idewizardpreviewpage import IdeWizardPreviewPage
		self.addPage( IdeWizardPreviewPage( self, __file__ ) )
	
	def accept( self ):
		Wizard.accept( self )
		
		# save the new environment to the treegrunt and refresh
		foptions = self.field( 'options' ).toPyObject()
		if ( not type(foptions) == dict ):
			foptions = {}
		
		options = {}
		for opt,val in foptions.items():
			options[str(opt)] = str(val)
		
		# add a new tool to the user's local environments
		from blurdev.tools import ToolsEnvironment
		ToolsEnvironment.createNewEnvironment( options['environment'], options['installpath'] + '/%s' % str(options['environment']).lower(), options[ 'default' ], options[ 'development' ] )
		ToolsEnvironment.recordConfig()