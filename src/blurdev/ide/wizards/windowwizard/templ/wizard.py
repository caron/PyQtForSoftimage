##
#	\namespace	[package].[module]
#
#	\remarks	[desc::commented]
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		[date]
#

from blurdev.gui import Wizard

class [class]( Wizard ):
	def initWizardPages( self ):
		"""
			\remarks	[virtual]	overloaded from the Wizard class, this method allows a user to define the pages that are
									going to be used for this wizard.  Look up QWizard in the Qt Assistant for more advanced options
									and controlling flows for your wizard.
									
									Wizard classes don't need to specify UI information, all the data for the Wizard will be encased
									within WizardPage instances
		"""
#!		from mypage import MyPage		# import a QWizardPage class and add it to the wizard
#!		self.addPage( MyPage(self) )
		pass

#!	@classmethod
#!	def runWizard( cls, parent = None ):
#!		if ( cls(parent).exec_() ):
#!			return True
#!		return False