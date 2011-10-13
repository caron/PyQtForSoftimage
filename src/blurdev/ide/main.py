##
#	\namespace	blurdev.ide.main.py
#
#	\remarks	Runs the IdeEditor as an application
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		08/19/10
#

# if this is run directly
if ( __name__ == '__main__' ):
	import blurdev
	from blurdev.ide.ideeditor import IdeEditor
	
	# launch the editor
	blurdev.launch( IdeEditor.instance, coreName = 'ide' )