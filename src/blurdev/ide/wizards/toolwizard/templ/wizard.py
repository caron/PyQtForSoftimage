##
#	\namespace	[name].[module]
#
#	\remarks	The main Wizard definition for the [name] tool
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		[date]
#

# we import from blurdev.gui vs. QtGui becuase there are some additional management features for running the Wizard in multiple environments
from blurdev.gui import Wizard

class [class]( Wizard ):
	def initializePages( self ):
		"""
			\remarks	[virtual]	Initializes the pages that are going to be used by this wizard
		"""
		# define custom pages for the wizard
#!		from mypage import MyPage
#!		self.addPage( MyPage(self) )

		pass