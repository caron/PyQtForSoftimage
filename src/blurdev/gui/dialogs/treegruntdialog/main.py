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
	from blurdev.gui.dialogs.treegruntdialog import TreegruntDialog
	
	# launch the editor
	blurdev.launch( TreegruntDialog.instance, coreName = 'treegrunt' )