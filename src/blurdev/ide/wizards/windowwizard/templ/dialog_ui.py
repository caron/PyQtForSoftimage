##
#	\namespace	[package].[module]
#
#	\remarks	[desc::commented]
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		[date]
#

from blurdev.gui import Dialog

class [class]( Dialog ):
	def __init__( self, parent = None ):
		Dialog.__init__( self, parent )
		
		# load the ui
		import blurdev
		blurdev.gui.loadUi( __file__, self )
		
		# define custom properties
#!		self._customParam = 1

		# create connections
#!		self.uiDialogBTNS.accepted.connect( self.accept )		# assumes there is a uiDialogBTNS in the ui file
#!		self.uiDialogBTNS.rejected.connect( self.reject )		# assumes there is a uiDialogBTNS in the ui file
		
	# define instance methods
#!	def customParam( self ):
#!		"""
#!			\remarks	returns the value for my parameter
#!			\return		<variant>
#!		"""
#!		return self._customParam

#!	def setCustomParam( self, value ):
#!		"""
#!			\remarks	sets the value for my parameter to the inputed value
#!			\param		value	<variant>
#!		"""
#!		self._customParam = value

	# define static methods
#!	@staticmethod
#!	def edit( value ):
#!		import blurdev
#!		dlg = [class]( blurdev.core.activeWindow() )
#!		dlg.setCustomParam( value )
#!		if ( dlg.exec_() ):
#!			return True
#!		return False