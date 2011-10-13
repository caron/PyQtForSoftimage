##
#	\namespace	[FILENAME]
#
#	\remarks	[ADD REMARKS]
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		11/01/10
#

from blurdev.gui import Wizard

class IDETemplateWizard( Wizard ):
	def initWizardPages( self ):
		# set the wizard title
		self.setWindowTitle( 'IDE Template Wizard' )
		
		# create additional options pages
		from idetemplateoptions import IDETemplateOptions
		self.addPage( IDETemplateOptions( self ) )
		
		# always add the template preview page
		from blurdev.ide.idewizardpreviewpage import IdeWizardPreviewPage
		self.addPage( IdeWizardPreviewPage( self, __file__ ) )