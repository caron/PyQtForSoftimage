##
#	\namespace	blurdev.ide.wizards.elementalnodewizard.elementalnodewizard
#
#	\remarks	Defines the main Wizard class for the ElementalNodeWizard wizard system
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		11/09/10
#

from blurdev.gui import Wizard

class ElementalNodeWizard( Wizard ):
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
		self.setWindowTitle( 'ElementalNode Wizard' )
		
		# create the main options page
		from elementalnodeoptions import ElementalNodeOptions
		self.addPage( ElementalNodeOptions( self ) )
		
		# create any additional pages
#!		from some_module import some_class
#!		self.addPage( some_class( self ) )
		
		# create the wizard creation page
		from blurdev.ide.idewizardpreviewpage import IdeWizardPreviewPage
		self.addPage( IdeWizardPreviewPage( self, __file__ ) )