##
#	\namespace	blurdev.cores.studiomaxcore
#
#	\remarks	This class is a reimplimentation of the blurdev.cores.core.Core class for running blurdev within Studiomax sessions
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		04/12/10
#

# to be in a 3dsmax session, we need to be able to import the Py3dsMax package
import Py3dsMax
from blurdev.cores.core import Core

#-------------------------------------------------------------------------------------------------------------

STUDIOMAX_MACRO_TEMPLATE = """
macroscript Blur_%(id)s_Macro
category: "Blur Tools"
toolTip: "%(tooltip)s"
buttonText: "%(displayName)s"
icon:#( "Blur_%(id)s_Macro", 1 )
(
	local blurdev 	= python.import "blurdev"
	blurdev.runTool "%(tool)s" macro:"%(macro)s"
)
"""

# initialize callback scripts
STUDIOMAX_CALLBACK_TEMPLATE = """
global pyblurdev
if ( pyblurdev == undefined ) then ( pyblurdev = python.import "blurdev" )
if ( pyblurdev != undefined ) then ( 
	local ms_args = (callbacks.notificationParam())
	pyblurdev.core.dispatch "%(signal)s" %(args)s 
)
"""

class StudiomaxCore( Core ):
	def __init__( self ):
		Core.__init__( self )
		self.setObjectName( 'studiomax' )
		self._supportLegacy 	= False
		
	def connectAppSignals( self ):
		self.connectStudiomaxSignal( 'systemPreNew',		'sceneNewRequested' )
		self.connectStudiomaxSignal( 'systemPostNew',		'sceneNewFinished' )
		self.connectStudiomaxSignal( 'filePreOpen',			'sceneOpenRequested', 	'""'	)
		self.connectStudiomaxSignal( 'filePostOpen',		'sceneOpenFinished', 	'""' )
		self.connectStudiomaxSignal( 'filePreMerge',		'sceneMergeRequested' )
		self.connectStudiomaxSignal( 'filePostMerge',		'sceneMergeFinished' )
		self.connectStudiomaxSignal( 'filePreSave', 		'sceneSaveRequested', 	'(if (ms_args != undefined) then (ms_args as string) else "")' )
		self.connectStudiomaxSignal( 'filePostSave', 		'sceneSaveFinished', 	'(if (ms_args != undefined) then (ms_args as string) else "")' )
		self.connectStudiomaxSignal( 'systemPostReset',		'sceneReset' )
		self.connectStudiomaxSignal( 'layerCreated',		'layerCreated' )
		self.connectStudiomaxSignal( 'layerDeleted',		'layerDeleted' )
		self.connectStudiomaxSignal( 'postSystemStartup',	'startupFinished' )
		self.connectStudiomaxSignal( 'preSystemShutdown',	'shutdownStarted' )
		
		# create a signal linking between 2 signals
		self.linkSignals( 'sceneNewFinished', 		'sceneInvalidated' )
		self.linkSignals( 'sceneOpenFinished', 		'sceneInvalidated' )
		self.linkSignals( 'sceneMergeFinished',		'sceneInvalidated' )
		self.linkSignals( 'sceneReset',				'sceneInvalidated' )

	def connectStudiomaxSignal( self, maxSignal, blurdevSignal, args = '' ):
		from Py3dsMax import mxs
		
		# store the maxscript methods needed
		_n			= mxs.pyhelper.namify
		callbacks 	= mxs.callbacks
		blurdevid 	= _n('blurdev')
		
		callbacks.addScript( _n(maxSignal), STUDIOMAX_CALLBACK_TEMPLATE % { 'signal': blurdevSignal, 'args': args } )

	def createToolMacro( self, tool, macro = '' ):
		"""
			\remarks	Overloads the createToolMacro virtual method from the Core class, this will create a macro for the
						Studiomax application for the inputed Core tool
			
			\return		<bool> success
		"""
		# create the options for the tool macro to run
		options = { 'tool': tool.objectName(), 'displayName': tool.displayName(), 'macro': macro, 'tooltip': tool.displayName(), 'id': str( tool.displayName() ).replace( ' ', '_' ).replace( '::', '_' ) }
		
		# create the macroscript
		from Py3dsMax import mxs
		
		filename = mxs.pathConfig.resolvePathSymbols( '$usermacros/Blur_%s_Macro.mcr' % options[ 'id' ] )
		f = open( filename, 'w' )
		f.write( STUDIOMAX_MACRO_TEMPLATE % options )
		f.close()
		
		# convert icon files to max standard ...
		from PyQt4.QtGui import QImage
		root	= QImage( tool.icon() )
		icon24	= root.scaled( 24, 24 )
		
		# ... for 24x24 pixels (image & alpha icons)
		basename = mxs.pathConfig.resolvePathSymbols( '$usericons/Blur_%s_Macro' % options[ 'id' ] )
		icon24.save( basename + '_24i.bmp' )
		icon24.alphaChannel().save( basename + '_24a.bmp' )
		
		# ... and for 16x16 pixels (image & alpha icons)
		icon16	= root.scaled( 16, 16 )
		icon16.save( basename + '_16i.bmp' )
		icon16.alphaChannel().save( basename + '_16a.bmp' )
		
		# run the macroscript & refresh the icons
		mxs.filein( filename )
		mxs.colorman.setIconFolder( '.' )
		mxs.colorman.setIconFolder( 'Icons' )
		
		return True
		
	def disableKeystrokes( self ):
		"""
			\remarks	[overloaded] disables keystrokes in maxscript
		"""
		from Py3dsMax import mxs
		mxs.enableAccelerators = False
		
		return Core.disableKeystrokes( self )
		
	def enableKeystrokes( self ):
		"""
			\remarks	[overloaded] disables keystrokes in maxscript - max will always try to turn them on
		"""
		from Py3dsMax import mxs
		mxs.enableAccelerators = False
		
		return Core.enableKeystrokes( self )
		
	def init( self ):
		# connect the plugin to 3dsmax
		import Py3dsMax
		self.connectPlugin( Py3dsMax.GetPluginInstance(), Py3dsMax.GetWindowHandle() )
		
		# init the base class
		return Core.init( self )
		
	def registerPaths( self ):
		from blurdev.tools import ToolsEnvironment
		env = ToolsEnvironment.activeEnvironment()
		
		# update the old blur maxscript library system
		envname = str(env.objectName()).lower()
		if ( envname != 'local' ):
			envname = 'network'
		
		# update the old library system
		if ( self.supportLegacy() ):
			from Py3dsMax import mxs
			blurlib = mxs._blurLibrary
			if ( blurlib ):
				blurlib.setCodePath( envname )
		
		# register standard paths
		return Core.registerPaths( self )
	
	def runScript( self, filename = '', scope = None, argv = None, toolType = None ):
		"""
			\remarks	[overloaded] handle maxscript script running
		"""
		
		if ( not filename ):
			from PyQt4.QtGui import QApplication, QFileDialog
			
			# make sure there is a QApplication running
			if ( QApplication.instance() ):
				filename = str( QFileDialog.getOpenFileName( None, 'Select Script File', '', 'Python Files (*.py);;Maxscript Files (*.ms);;All Files (*.*)' ) )
				if ( not filename ):
					return
		
		filename = str(filename)
		
		# run a maxscript file
		import os.path
		if ( os.path.splitext( filename )[1] in ('.ms','.mcr') ):
			if ( os.path.exists( filename ) ):
				import Py3dsMax
				try:
					runcmd = Py3dsMax.runMaxscript
				except:
					from Py3dsMax import mxs
					runcmd = mxs.filein
					
				runcmd( filename )
				return True
			return False
		
		return Core.runScript( self, filename, scope, argv, toolType )
	
	def setSupportLegacy( self, state ):
		self._supportLegacy = state
	
	def supportLegacy( self ):
		return self._supportLegacy
	
	def toolTypes( self ):
		"""
			\remarks	Overloads the toolTypes method from the Core class to show tool types that are related to
						Studiomax applications
						
			\return		<blurdev.tools.ToolType>
		"""
		from blurdev.tools 	import ToolsEnvironment, ToolType
		
		output = ToolType.Studiomax | ToolType.LegacyStudiomax
		
		return output