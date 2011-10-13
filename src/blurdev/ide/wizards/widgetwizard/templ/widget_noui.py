##
#	\namespace	[package][module]
#
#	\remarks	[desc::commented]
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		[date]
#

from [super_module] import [super]

class [class]( [super] ):
	def __init__( self, parent ):
		# initialize the super class
		[super].__init__( self, parent )
		
		# define the user interface data
#! 		finish initializing the class
		
		# create custom properties
#! 		self._customProperty = ''
		
		# create connections
#! 		self.uiNameTXT.textChanged.connect( self.setCustomProperty )
	
#!	def customProperty( self ):
#!		"""
#!			\remarks	our system works with the getter/setter style that Qt uses - lowercase/camel hump methods, with the getter
#!						having no 'get' at the front of it, and the setter having a 'set'<getter> syntax
#!			\return		<variant>
#!		"""
#!		return self._customProperty		# in python, a '_' lets a programmer know that this member should be considered protected
#!
#!	def setCustomProperty( self, prop ):
#!		"""
#!			\remarks	this setter completes the definition for a custom property in our system
#!			\param		prop		<variant>
#!		"""
#!		self._customProperty = prop