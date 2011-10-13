##
#	\namespace	[name].main
#
#	\remarks	[desc::commented]
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		[date]
#

# make sure this is being run as the main process
if ( __name__ in ( '__main__', '__builtin__' ) ):
	# since this file is being executed in the main scope, we need to register the tool package to the sys.path
	import blurdev
	blurdev.registerScriptPath( __file__ )
	
	# depending on our environment, Python initializes the script differently for scope, so try both methods:
	# importing from a sub-module
	try:
		from [module] import [class]
	
	# importing from the main package
	except:
		from [name].[module] import [class]
	
	blurdev.launch( [class] )