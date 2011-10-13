##
#	\namespace	blurdev.ide.wizards.widgetwizard.widgetwizard
#
#	\remarks	[ADD REMARKS]
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		11/04/10
#

from blurdev.gui import Wizard

class WidgetWizard( Wizard ):
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
		self.setWindowTitle( 'Widget Wizard' )
		
		# \todo			Add custom pages here
		
		from widgetoptions import WidgetOptions
		self.addPage( WidgetOptions( self ) )
		
		# \warning		the IdeWizardPreviewPage should always be the last page
		# 				Only remove this if you intend to write your own generation code
		from blurdev.ide.idewizardpreviewpage import IdeWizardPreviewPage
		self.addPage( IdeWizardPreviewPage( self, __file__ ) )