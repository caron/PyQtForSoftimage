##
#	\namespace	blurdev
#
#	\remarks	The blurdev package is the core library methods for tools development at Blur Studio
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		06/11/10
#

__DOCMODE__	= False		# this variable will be set when loading information for documentation purposes

# track the install path
import os.path
installPath = os.path.split( __file__ )[0]

# include the blur path
from tools import ToolsEnvironment

# register the standard blur path
ToolsEnvironment.registerPath( 'c:/blur' )

# register the beta blur path as an overload for beta tools
ToolsEnvironment.registerPath( 'c:/blur/beta' )

application = None	# create a managed QApplication
core 		= None	# create a managed Core instance

def activeEnvironment():
	from blurdev.tools import ToolsEnvironment
	return ToolsEnvironment.activeEnvironment()

def bindMethod( object, name, method ):
	""" Properly binds a new python method to an existing C++ object as a dirty alternative to sub-classing when not possible """
	import types
	object.__dict__[ name ] = types.MethodType( method.im_func, object, object.__class__ )

def findDevelopmentEnvironment():
	from blurdev.tools import ToolsEnvironment
	return ToolsEnvironment.findDevelopmentEnvironment()
	
def findTool( name, environment = '' ):
	init()
	
	from tools import ToolsEnvironment
	if ( not environment ):
		env = ToolsEnvironment.activeEnvironment()
	else:
		env = ToolsEnvironment.findEnvironment( environment )
	
	if ( env ):
		return env.index().findTool( name )
	
	from tools.tool import Tool
	return Tool()

def init():
	global core
	global application
	if ( not core ):
		# create the core instance
		from blurdev.cores import Core
		
		# create the core
		core 		= Core()
		
		# initialize the application
		application = core.init()

def launch( ctor, modal = False, coreName = 'external' ):
	"""
		\remarks	This method is used to create an instance of a widget (dialog/window) to be run inside
					the blurdev system.  Using this function call, blurdev will determine what the application is
					and how the window should be instantiated, this way if a tool is run as a standalone, a
					new application instance will be created, otherwise it will run on top of a currently
					running application.
		
		\param		ctor		QWidget || method 	(constructor for a widget, most commonly a Dialog/Window/Wizard>
		\param		modal		<bool>	whether or not the system should run modally
		\param		coreName	<str>	string to give to the core if the application is going to be rooted under this widget
		
		\return		<bool>	success (when exec_ keyword is set) || <ctor> instance (when exec_ keyword is not set)
	"""
	init()
	
	# create the app if necessary
	app = None
	from PyQt4.QtGui import QWizard
	from blurdev.cores.core import Core
	
	if ( application ):
		application.setStyle( 'Plastique' )
		
		if ( core.objectName() == 'blurdev' ):
			core.setObjectName( coreName )
			
	# always run wizards modally
	iswiz = False
	try:
		iswiz = issubclass( ctor, QWizard )
	except:
		pass
		
	if ( iswiz ):
		modal = True
	
	# create the output instance from the class
	widget = ctor(None)
	
	# check to see if the tool is running modally and return the result
	if ( modal ):
		return widget.exec_()
	else:
		widget.show()
		
		# run the application if this item controls it
		if ( application ):
			application.setWindowIcon( widget.windowIcon() )
			application.exec_()
		
		return widget

def quickReload( modulename ):
	"""	
		\remarks	searches through the loaded sys modules and looks up matching module names based on the imported module
		\param		modulename 	<str>
	"""
	import sys, re
	expr = re.compile( str(modulename).replace( '.', '\.' ).replace( '*', '[A-Za-z0-9_]*' ) )
	
	# reload longer chains first
	keys = sys.modules.keys()
	keys.sort()
	keys.reverse()
	
	for key in keys:
		module = sys.modules[key]
		if ( expr.match(key) and module != None ):
			print 'reloading', key
			reload( module )

def packageForPath( path ):
	import os.path
	
	path		= str(path)
	splt 		= os.path.normpath( path ).split( os.path.sep )
	index		= 1
	
	filename 	= os.path.join( path, '__init__.py' )
	package = []
	while ( os.path.exists( filename ) ):
		package.append( splt[-index] )
		filename = os.path.join( os.path.sep.join( splt[:-index] ), '__init__.py' )
		index += 1
	
	package.reverse()
	return '.'.join( package )
		
def registerScriptPath( filename ):
	from tools import ToolsEnvironment
	ToolsEnvironment.registerScriptPath( filename )

def relativePath( path, additional ):
	import os.path
	return os.path.join( os.path.split( str( path ) )[0], additional )
	
def resourcePath( relpath ):
	return relativePath( __file__, 'resource/%s' % relpath )
		
def runTool( toolId, macro = "" ):
	init()
	
	# special case scenario - treegrunt
	if ( toolId == 'Treegrunt' ):
		core.showTreegrunt()
	
	# otherwise, run the tool like normal
	else:	
		from PyQt4.QtGui	import QApplication
		from tools 			import ToolsEnvironment
		
		# load the tool
		tool = ToolsEnvironment.activeEnvironment().index().findTool( toolId )
		if ( not tool.isNull() ):
			tool.exec_( macro )
			
		# let the user know the tool could not be found
		elif ( QApplication.instance() ):
			from PyQt4.QtGui import QMessageBox
			QMessageBox.critical( None, 'Tool Not Found', '%s is not a tool in %s environment.' % (toolId,ToolsEnvironment.activeEnvironment().objectName()) )

def setActiveEnvironment( env ):
	from blurdev.tools import ToolsEnvironment
	return ToolsEnvironment.findEnvironment( env ).setActive()

def startProgress( title = 'Progress', parent = None ):
	from blurdev.gui.dialogs.multiprogressdialog import MultiProgressDialog
	return MultiProgressDialog.start(title)

# the blurdev system will create and manage a QApplication instance
init()