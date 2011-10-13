##
#	\namespace	blurdev.cores.softimagecore
#
#	\remarks	This class is a reimplimentation of the blurdev.cores.core.Core class for running blurdev within Softimage sessions
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		04/12/10
#

# to be in a 3dsmax session, we need to be able to import the Py3dsMax package
import PySoftimage
from blurdev.cores.core import Core

#-------------------------------------------------------------------------------------------------------------

class SoftimageCore( Core ):
	def __init__( self ):
		Core.__init__( self )
		self.setObjectName( 'softimage' )
	
	def isKeystrokesEnabled( self ):
		from PyQt4.QtGui import QApplication, QCursor
		
		disabled = False
		if ( QApplication.instance().focusWidget() ):
			window 		= QApplication.instance().focusWidget().window()
			geom 		= window.geometry()
			disabled 	= geom.contains( QCursor.pos() )
			
		return not disabled
		
	def init( self ):
		# connect the plugin to 3dsmax
		from PySoftimage import xsi
		self.connectPlugin( xsi.GetPluginInstance(), xsi.GetWindowHandle() )
		
		self.protectModule( 'PySoftimage' )
			
		# load this file as a plugin for XSI
		xsi.LoadPlugin( __file__ )
		
		# init the base class
		return Core.init( self )
		
	def toolTypes( self ):
		"""
			\remarks	Overloads the toolTypes method from the Core class to show tool types that are related to
						Studiomax applications
						
			\return		<blurdev.tools.ToolType>
		"""
		from blurdev.tools 	import ToolsEnvironment, ToolType
		
		output = ToolType.Softimage | ToolType.LegacySoftimage
		
		return output