##
#	\namespace	blurdev.ide.wizards.toolwizard.toolwizard
#
#	\remarks	[ADD REMARKS]
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		11/04/10
#

from blurdev.gui import Wizard

class MaxscriptToolWizard( Wizard ):
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
		self.setWindowTitle( 'Python Tool Wizard' )
		
		# \todo			Add custom pages here
		
		from tooloptions import MaxscriptToolOptions
		self.addPage( MaxscriptToolOptions( self ) )
		
		# \warning		the IdeWizardPreviewPage should always be the last page
		# 				Only remove this if you intend to write your own generation code
		from blurdev.ide.idewizardpreviewpage import IdeWizardPreviewPage
		self.addPage( IdeWizardPreviewPage( self, __file__ ) )
		
class PythonToolWizard( Wizard ):
	def accept( self ):
		Wizard.accept( self )
		
		# after a tool wizard finishes, try to load its application
		options = self.field('options').toPyObject()
		
		# load the key/value pairing
		pyoptions = {}
		for key,val in options.items():
			pyoptions[str(key)] = str(val)
		
		from blurdev import template
		projpath = template.formatText( '[installpath]/[name]/[name].blurproj', pyoptions )
		import os.path
		if ( os.path.exists( projpath ) ):
			from blurdev.ide.ideeditor import IdeEditor
			from blurdev.ide.ideproject import IdeProject
			IdeEditor.instance().setCurrentProject( IdeProject.fromXml( projpath ) )
		else:
			print 'could not find file: ', projpath
			
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
		from PyQt4.QtCore import QDir
		
		self.setWindowTitle( 'Python Tool Wizard' )
		
		# \todo			Add custom pages here
		
		from tooloptions import PythonToolOptions
		self.addPage( PythonToolOptions( self ) )
		
		# \warning		the IdeWizardPreviewPage should always be the last page
		# 				Only remove this if you intend to write your own generation code
		from blurdev.ide.idewizardpreviewpage import IdeWizardPreviewPage
		self.addPage( IdeWizardPreviewPage( self, __file__ ) )