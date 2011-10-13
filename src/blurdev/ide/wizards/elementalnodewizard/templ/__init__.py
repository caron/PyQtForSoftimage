##
#	\namespace	[package].[module]
#
#	\remarks	[desc::commented]
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		11/09/10
#

def registerPlugins( system ):
	"""
		\remarks	this method will be run by the elemental plugin registration system, and will pass in the current
					ElementalSystem instance that the plugins should be registered to.  This method must exist or your
					plugins will not be registered
					
		\param		<elemental.elementalsystem.ElementalSystem>
	"""
	# register all the nodes for this package
	from [module] import [class]
	system.registerPlugin( '[group]::[name]', [class] )
