##
#	\namespace	python.blurdev.ide.wizards.codewizard.codewizard
#
#	\remarks	Defines the main Wizard class for the CodeWizard wizard system
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		03/01/11
#

from blurdev.gui import Wizard

class CodeWizard( Wizard ):
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
		self.setWindowTitle( 'Code Wizard' )
		
		# create the main options page
		from codeoptions import CodeOptions
		self.addPage( CodeOptions( self ) )
		
		# create any additional pages
#!		from some_module import some_class
#!		self.addPage( some_class( self ) )
		
		# create the wizard creation page
		from blurdev.ide.idewizardpreviewpage import IdeWizardPreviewPage
		self.addPage( IdeWizardPreviewPage( self, __file__ ) )