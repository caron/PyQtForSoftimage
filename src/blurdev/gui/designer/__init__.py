##
#	\namespace	blurdev.gui.designer
#
#	\remarks	This package contains classes that expose blurdev widgets to the Qt Designer
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		12/07/08
#

plugindef = """##
#	\\namespace	blurdev.gui.designer.%(class)s
#
#	\\remarks	Defines a plugin file for the %(class)s widget
#	
#	\\author		beta@blur.com
#	\\author		Blur Studio
#	\\date		12/07/08
#

from PyQt4.QtDesigner 	import QPyDesignerCustomWidgetPlugin

class %(class)sPlugin( QPyDesignerCustomWidgetPlugin ):
	def __init__( self, parent = None ):
		QPyDesignerCustomWidgetPlugin.__init__( self )
		
		self.initialized = False
	
	def initialize( self, core ):
		if ( self.initialized ):
			return
		
		self.initialized = True
	
	def isInitialized( self ):
		return self.initialized
	
	def createWidget( self, parent ):
		from %(module)s import %(class)s
		return %(class)s( parent )
	
	def name( self ):
		return "%(class)s"
	
	def group( self ):
		return "%(group)s"
	
	def icon( self ):
		from PyQt4.QtGui import QIcon
		return QIcon( "%(icon)s" )
	
	def toolTip( self ):
		return ""
	
	def whatsThis( self ):
		return ""
	
	def isContainer( self ):
		return %(container)s
	
	def includeFile( self ):
		return "%(module)s"
	
	def domXml( self ):
		xml = []
		xml.append( '<widget class="%(class)s" name="%(class)s"/>' )
		return '\\n'.join( xml )

import blurdev.gui.designer
blurdev.gui.designer.register( '%(class)sPlugin', %(class)sPlugin )
"""

def init():
	import glob
	import os.path
	
	# load the plugins file
	import blurdev
	loadPlugins( blurdev.resourcePath( 'designer_plugins.xml' ) )
	
	# import the modules
	filenames = glob.glob( os.path.split( __file__ )[0] + '/*.py' )
	filenames.sort()
	for filename in filenames:
		modname = os.path.basename( filename ).split( '.' )[0]
		if ( modname != '__init__' ):
			fullname = 'blurdev.gui.designer.%s' % modname
			try:
				__import__( fullname )
			except:
				print 'Error loading %s' % fullname

def loadPlugins( filename ):
	from blurdev.XML import XMLDocument
	doc = XMLDocument()
	
	if ( doc.load( filename ) ):
		import os, sys
		
		blurdevpath = os.path.abspath( os.path.split( __file__ )[0] + '/../..' )
		
		for child in doc.root().children():
			if ( child.nodeName == 'include' ):
				import re
				href = child.attribute( 'href' )
				
				# replace sys globals
				results 	= re.findall( '\[([^\]]+)', href )
				for result in results:
					if ( result == 'BLURDEV' ):
						href = href.replace( '[%s]' % result, blurdevpath )
					else:
						href = href.replace( '[%s]' % result, os.environ.get( result, '[%s]' % result ) )
				
				# make sure the location is importable
				importPath = child.attribute( 'root' )
				if ( importPath ):
					results 	= re.findall( '\[([^\]]+)', importPath )
					for result in results:
						importPath = importPath.replace( '[%s]' % result, os.environ.get( result, '[%s]' % result ) )
					
					if ( os.path.exists( importPath ) and not importPath in sys.path ):
						sys.path.insert( 0, importPath )
				
				# load the include file
				loadPlugins( href )
			else:
				createPlugin( child.attribute( "module" ), child.attribute( "class" ), child.attribute( "icon" ), child.attribute( "group", 'Blur Widgets' ), eval(child.attribute( 'container', 'False' )) )

def register( name, plugin ):
	import blurdev.gui.designer
	blurdev.gui.designer.__dict__[ name ] = plugin

def createPlugin( module, cls, icon = '', group = 'Blur Widgets', container = False ):
	options = { 'module': module, 'class': cls, 'icon': icon, 'group': group, 'container': container }
	import os.path
	filename = os.path.split( __file__ )[0] + '/%splugin.py' % str( cls ).lower()
	f = open( filename, 'w' )
	f.write( plugindef % options )
	f.close()
	