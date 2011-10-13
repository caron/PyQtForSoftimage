##
#	\namespace	blurdev.cores.motionbuildercore
#
#	\remarks	This class is a reimplimentation of the blurdev.cores.core.Core class for running blurdev within Studiomax sessions
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		04/12/10
#

# to be in a 3dsmax session, we need to be able to import the Py3dsMax package
import pyfbsdk
from blurdev.cores.core import Core

#-------------------------------------------------------------------------------------------------------------

class MotionBuilderCore( Core ):
	def __init__( self ):
		Core.__init__( self )
		self.setObjectName( 'motionbuilder' )
	
	def activeWindow( self ):
		"""
			\remarks	make sure the root motion builder window is used, or it won't parent properly
			\return		<QWidget> || None
		"""
		from PyQt4.QtGui import QApplication
		
		window = None
		if ( QApplication.instance() ):
			window = QApplication.instance().activeWindow()
			
			while ( window.parent() ):
				window = window.parent()
			
		return window
	
	def toolTypes( self ):
		"""
			\remarks	Virtual method to determine what types of tools that the trax system should be looking at
			\return		<trax.api.tools.ToolType>
		"""
		from blurdev.tools 	import ToolsEnvironment, ToolType
		
		output = ToolType.MotionBuilder
		
		return output
	
		