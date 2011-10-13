##
#	\namespace	build
#
#	\remarks	Sets up the build system for the package installers
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		06/11/10
#

if ( __name__ == '__main__' ):
	from blur.build import *
	import sys, os
	
	product = sys.argv[1]
	
	# make sure the path exists for the package
	path 			= os.path.dirname(os.path.abspath(__file__))
	dirpath			= os.path.abspath( path + '/..' )
	if ( not dirpath in sys.path ):
		sys.path.append( dirpath )
	
	from optparse import OptionParser
	
	import version
	
	# determine what python folder to install to
	parser = OptionParser()
	parser.add_option( '-v', '--version', dest = 'version', default = 'Python24' )
	parser.add_option( '-i', '--install', dest = 'install', default = '0' )
	parser.add_option( '-o', '--offline', dest = 'offline', default = '0' )
	
	(options,args) 	= parser.parse_args()
	dictionary		= options.__dict__
	
	# create the global defines from input
	f = open( path + '/installers/autogen.nsi', 'w' )
	f.write( '!define MUI_PRODUCT "%s"\n' % product )
	f.write( '!define MUI_VERSION "v1.0.X"\n' )
	f.write( '!define INSTALL_VERSION "v%i.%02i"\n' % (version.major(),version.minor()) )
	f.write( '!define PYTHON_VERSION "%s"\n' % dictionary[ 'version' ] )
	f.write( '!define OFFLINE %s\n' % dictionary['offline'] )
	
	if ( dictionary['offline'] == '1' ):
		f.write( '!define OUTPUT_FILENAME "bin\offline\${MUI_PRODUCT}-install-${INSTALL_VERSION}.${MUI_SVNREV}-offline.exe"\n' )
	else:
		f.write( '!define OUTPUT_FILENAME "bin\${MUI_PRODUCT}-install-${INSTALL_VERSION}.${MUI_SVNREV}.exe"\n' )
	
	f.close()
	
	svnnsi 	= WCRevTarget( 'svnrevnsi', path, path, 'installers/svnrev-template.nsi', 'installers/svnrev.nsi' )
	svnpy 	= WCRevTarget( 'svnrevpy', path, path, 'installers/version-template.txt', 'build.txt' )
	nsi		= NSISTarget('installer', path, 'installers/installer.nsi' )
	
	Target( product, path, [svnnsi,svnpy], [nsi] )
	
	build()
	
	# see if the user wants to run the installer
	if ( dictionary[ 'install' ] == '1' ):
		f = open( path + '/installers/svnrev.nsi', 'r' )
		lines = f.read()
		f.close()
		
		import re
		results = re.search( '!define MUI_SVNREV "(\d+)"', lines )
		
		if ( results ):
			filename = path + '/installers/bin/%s-install-v%i.%02i.%s.exe' % (product,version.major(),version.minor(),results.groups()[0])
			import os
			os.startfile( filename )