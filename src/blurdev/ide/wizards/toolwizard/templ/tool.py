##
#	\namespace	[name].[module]
#
#	\remarks	The main [super] definition for the [name] tool
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		[date]
#

# we import from blurdev.gui vs. QtGui becuase there are some additional management features for running the [super] in multiple environments
from blurdev.gui import [super]

class [class]( [super] ):
	def __init__( self, parent = None ):
		[super].__init__( self, parent )
		[ui_logic]
		
		# initialize the ui
#!		self.uiSomeDDL.addItems( [ 'A', 'B', 'C' ] )

		# create connections
#!		self.uiSomeDDL.currentIndexChanged.connect( self.refreshUi )
		
		# restore settings from last session
		self.restoreSettings()
	
	def closeEvent( self, event ):
		"""
			\remarks	[virtual]	overload the close event to handle saving of preferences before shutting down
			\param		event		<QEvent>
		"""
		self.recordSettings()
		[super].closeEvent( self, event )
	
	def recordSettings( self ):
		"""
			\remarks	records settings to be used for another session
		"""
		from blurdev import prefs
		pref = prefs.find( 'tools/[name]' )
		
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
		pref = prefs.find( 'tools/[name]' )
		
		# reload the geometry
		from PyQt4.QtCore import QRect
		geom = pref.restoreProperty( 'geom', QRect() )
		if ( geom and not geom.isNull() ):
			self.setGeometry( geom )
		
		# restore additional settings
#!		self.uiSomeDDL.setCurrentIndex( pref.restoreProperty( 'index', 0 ) )