##
#	\namespace	[name].main
#
#	\remarks	[desc::commented]
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		[date]
#

def [name::lower]Execute():
	# rename method to desired function
	pass

# make sure this is being run as the main process
if ( __name__ in ( '__main__', '__builtin__' ) ):
	[name::lower]Execute()