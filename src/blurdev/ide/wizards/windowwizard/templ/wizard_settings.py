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
	def __init__( self, parent = None ):
		Wizard.__init__( self, parent )
		
		# restore settings
		self.restoreSettings()
	
	def closeEvent( self, event ):
		Wizard.closeEvent( self, event )
		
		# record the settings
		self.recordSettings()
	
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

	def recordSettings( self ):
		"""
			\remarks	records settings to be used for another session
		"""
		from blurdev import prefs
		pref = prefs.find( '[class]' )
		
		# record the geometry
		pref.recordProperty( 'geom', self.geometry() )
		
		# record additional settings
#!		pref.recordProperty( 'index', self.uiSomeDDL.currentIndex() )
		
		# save the settings
		pref.save()
	
	def restoreSettings( self ):
		"""
			\remarks	restores settings that were saved by a previous session
		"""
		from blurdev import prefs
		pref = prefs.find( '[class]' )
		
		# reload the geometry
		from PyQt4.QtCore import QRect
		geom = pref.restoreProperty( 'geom', QRect() )
		if ( geom and not geom.isNull() ):
			self.setGeometry( geom )
		
		# restore additional settings
#!		self.uiSomeDDL.setCurrentIndex( pref.restoreProperty( 'index', 0 ) )
