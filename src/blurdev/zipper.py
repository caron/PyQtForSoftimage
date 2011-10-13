##
#	\namespace	blurdev.zipper
#
#	\remarks	methods for archiving and unarchiving files
#	
#	\author		eric@blur.com
#	\author		Blur Studio
#	\date		03/21/11
#

_ZIP_EXE = 'c:/blur/assburner/zip.exe'

def packageFiles( files, outputfile ):
	"""
		\remarks	packages the inputed files to the output file location
		\param		files		<list> [ <str> filename, .. ]
		\param		outputfile	<str>
		\return		<bool> success
	"""
	if ( not files ):
		return False
	
	import random, os, shutil
	temppath = 'c:/temp/archive%i' % int(random.random() * 1000000)
	
	# create the temp path
	if ( not os.path.exists(temppath) ):
		os.makedirs(temppath)
	
	# copy the files to the temp path
	for filename in files:
		shutil.copyfile( filename, '%s/%s' % (temppath,os.path.basename(filename)) )
	
	# call the package path function
	success = packagePath( temppath, outputfile )
	
	# remove the temp path
	shutil.rmtree( temppath )
	
	return success

def packagePath( path, outputfile ):
	"""
		\remarks	packages all the information at the inputed path to the output file location
		\param		path		<str>
		\param		outputfile	<str>
		\return		<bool> success
	"""
	from blurdev import debug
	import os.path
	from PyQt4.QtCore import QProcess
	
	# create the zip command
	zipcmd 	= r'%s -j %s %s\*' % (os.path.normpath(_ZIP_EXE),os.path.normpath(outputfile),os.path.normpath(path))
	
	# determine based on debugging level if we should let this process with or without a try/catch
	if ( debug.isDebugLevel(debug.DebugLevel.Mid) ):
		debug.debugObject( packagePath, 'Running zip command: %s' % (zipcmd) )
		failure = QProcess.execute(zipcmd)
		
	else:
		try:
			failure = QProcess.execute(zipcmd)
		except:
			debug.debugObject( packagePath, 'Could not package %i files to %s path (%s zip EXE)' % (len(files),path,_ZIP_EXE) )
			failure = 1
	
	return (not failure)