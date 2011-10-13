##
#	\namespace	blurdev.ide.wizards
#
#	\remarks	These plugins allow you to quickly and easily create components of a tool or class
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		08/19/10
#

class WizardPlugin:
	def __init__( self ):
		self.name = ''
		self.wizardId = ''
		self.language = ''
		self.group = ''
		self.desc = ''
		self.toolTip = ''
		self.iconFile = ''
		self.module = ''
		self.cls = ''
	
	def runWizard( self ):
		import sys
		__import__( self.module )
		
		module = sys.modules[self.module]
		cls = module.__dict__.get( self.cls )
		return cls.runWizard()
	
	@staticmethod
	def fromXml( filename ):
		from blurdev.XML import XMLDocument
		doc = XMLDocument()
		import os.path
		
		output = []
		if (doc.load(filename)):
			root 				= doc.root()
			for xml in root.children():
				templ 				= WizardPlugin()
				templ.language		= xml.attribute( 'language', 'Python' )
				templ.name 			= xml.attribute( 'name', 'New Wizard' )
				templ.group 		= xml.attribute( 'group', 'Default' )
				templ.wizardId		= '%s::%s::%s' % (templ.language,templ.group,templ.name)
				templ.toolTip		= '<b>%s</b><br><small>%s</small>' % (templ.name,xml.findProperty( 'toolTip' ))
				templ.desc			= xml.findProperty( 'desc' )
				templ.iconFile		= os.path.join(os.path.split( filename )[0], xml.findProperty( 'icon' ))
				templ.module 		= xml.findProperty( 'module' )
				templ.cls			= xml.findProperty( 'class' )
				output.append(templ)
		return output

#-----------------------------------------------------------------------------

_wizards = {}

import os.path, glob
files = glob.glob( os.path.split( __file__ )[0] + '/*/register.xml' )
for filename in files:
	plugs = WizardPlugin.fromXml( filename )
	for plug in plugs:
		_wizards[plug.wizardId] = plug
	
#-----------------------------------------------------------------------------

def find( templ ):
	return _wizards.get(str(templ))

def wizards(language, group):
	language = str(language)
	group = str(group)
	out = [ templ for templ in _wizards.values() if templ.group == group and templ.language == language ]
	out.sort( lambda x,y: cmp( x.name, y.name ) )
	return out

def wizardGroups( language ):
	keymap = {}
	for templ in _wizards.values():
		if ( templ.language == language ):
			keymap[templ.group] = 0
	
	keys = keymap.keys()
	keys.sort()
	return keys

def wizardLanguages():
	keymap = {}
	for templ in _wizards.values():
		keymap[templ.language] = 0
	
	keys = keymap.keys()
	keys.sort()
	return keys