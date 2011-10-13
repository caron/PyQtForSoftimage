##
#	\namespace	blurdev.debug
#
#	\remarks	Handles the debugging system for the blurdev package
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		04/09/10
#

from enum import enum

_currentLevel 	= 0
_debugLogger	= None
_errorReport	= []

DebugLevel = enum( 'Low', 'Mid', 'High' )

#---------------------------------------

class DebugLogger:
	pass

#---------------------------------------
	
class Stopwatch:
	def __init__( self, name, debugLevel = 1 ):
		self._name			= str(name)
		self._count			= 0
		self._debugLevel	= debugLevel
		self._lapStack	= []
		
		self.reset()
	
	def reset( self ):
		import datetime
		self._starttime = datetime.datetime.now()
		self._laptime	= None
		self._records	= []
		self._laps	= []
	
	def startLap( self, message ):
		if ( _currentLevel < self._debugLevel ):
			return False
			
		import datetime
		self._lapStack.append( (message,datetime.datetime.now()) )
		return True
	
	def stop( self ):
		if ( _currentLevel < self._debugLevel ):
			return False
			
		# pop all the laps
		while ( self._lapStack ):
			self.stopLap()
		
		import datetime
		ttime = str(datetime.datetime.now() - self._starttime)
		
		# output the logs
		output = [ 'time:%s | %s Stopwatch' % (ttime,self._name) ]
		output.append( '------------------------------------------' )
		output += self._records
		output.append( '' )
		
		debugMsg( '\n'.join( output ), self._debugLevel )
		return True
	
	def stopLap( self ):
		if ( not self._lapStack ):
			return False
		
		import datetime
		curr = datetime.datetime.now()
		
		message, sstart = self._lapStack.pop()
		
		# process the elapsed time
		elapsed		= str(curr - sstart)
		if ( not '.' in elapsed ):
			elapsed += '.'
			
		while ( len( elapsed ) < 14 ):
			elapsed += '0'
		
		# record a lap
		self._records.append( '\tlap: %s | %s' % (elapsed,message) )
		
#---------------------------------------

def clearErrorReport():
	"""
		\remarks	clears the current report
	"""
	global _errorReport
	_errorReport = []
		
def debugMsg( msg, level = 2 ):
	"""
		\remarks	Prints out a debug message to the stdout if the inputed level is greater than or equal to the current debugging level
		\param		msg		<str>						message to output
		\param		level	<DebugLevel>				debug level
		\return		<void>
	"""
	if ( level <= debugLevel() ):
		print 'DEBUG (%s) : %s' % (DebugLevel.keyByValue(level),msg)

def debugObject( object, msg, level = 2 ):
	"""
		\remarks	Usees the debugMsg function to output to the stdout a debug message including the reference of where the object calling the method is located
		
		\sa			debugMsg
		
		\param		object		<module> || <class> || <method> || <function>
		\param		msg			<str>
		\param		level		<DebugLevel>
		
		\return		<void>
	"""
	import inspect
	
	# debug a module
	if ( inspect.ismodule( object ) ):
		debugMsg( '[%s module] :: %s' % (object.__name__,msg), level )
	
	# debug a class
	elif ( inspect.isclass( object ) ):
		debugMsg( '[%s.%s class] :: %s' % (object.__module__,object.__name__,msg), level )
	
	# debug an instance method
	elif ( inspect.ismethod( object ) ):
		debugMsg( '[%s.%s.%s method] :: %s' % (object.im_class.__module__,object.im_class.__name__,object.__name__,msg), level )
	
	# debug a function
	elif ( inspect.isfunction( object ) ):
		debugMsg( '[%s.%s function] :: %s' % (object.__module__,object.__name__,msg), level )

def debugStubMethod( object, msg, level = 2 ):
	"""
		\remarks	Uses the debugObject function to display that a stub method has not been provided functionality
		
		\sa			debugObject
		
		\param		object		<function> || <method>
		\param		msg			<str>
		\param		level		<DebugLevel>
		
		\return		<void>
	"""
	debugObject( object, 'Missing Functionality: %s' % msg, level )

def debugVirtualMethod( cls, object ):
	"""
		\remarks	Uses the debugObject function to display that a virtual function has not been overloaded
		
		\sa			debugObject
		
		\param		cls			<class>						base class where the method is defined
		\param		object		<function> || <method>
	"""
	debugObject( object, 'Virtual method has not been overloaded from %s class' % cls.__name__ )

def debugLevel():
	return _currentLevel

def emailList():
	import blurdev
	return blurdev.activeEnvironment().emailOnError()

def errorsReported():
	"""
		\remarks	returns whether or not the error report is empty
		\return		<bool>
	"""
	return len(_errorReport) > 0
	
def isDebugLevel( level ):
	"""
		\remarks	Checks to see if the current debug level greater than or equal to the inputed level
		\param		level		<DebugLevel> || <str> || <QString>
		\return		<boolean> success
	"""
	from PyQt4.QtCore import Qt, QString
	if ( type( level ) in (str,QString) ):
		level = DebugLevel.value( str( level ) )
	
	return level <= debugLevel()

def reportError( msg, debugLevel = 1 ):
	"""
		\remarks	adds the inputed message to the debug report
		\param		msg <str>
	"""
	if ( isDebugLevel(debugLevel) ):
		_errorReport.append( str(msg) )

def showErrorReport( subject = 'Errors Occurred', message = 'There were errors that occurred.  Click the Details button for more info.' ):
	if ( not errorsReported() ):
		from PyQt4.QtGui import QMessageBox
		QMessageBox.critical( None, subject, message )
	else:
		from blurdev.gui.dialogs.detailreportdialog import DetailReportDialog
		DetailReportDialog.showReport( None, subject, message, '<br>'.join( [ str(r) for r in _errorReport ] ) )
		return True
	
def setDebugLevel( level ):
	"""
		\remarks	Sets the debug level for the blurdev system module
		\param		level		<DebugLevel> || <str> || <QString>
		\return		<bool> success
	"""
	from PyQt4.QtCore 	import QString
	
	import blurdev
	global _currentLevel
	
	# clear the debug level
	if ( not level ):
		_currentLevel = 0
		
		if ( blurdev.core ):
			blurdev.core.emitDebugLevelChanged()
			
		return True
	
	# check for the debug value if a string is passed in
	if ( type( level ) in (str,QString) ):
		level = DebugLevel.value( str( level ) )
	
	# assign the debug flag
	if ( DebugLevel.isValid( level ) ):
		_currentLevel = level
		
		if ( blurdev.core ):
			blurdev.core.emitDebugLevelChanged()
			
		return True
	else:
		debugObject( setDebugLevel, '%s is not a valid <DebugLevel> value' % level )
		return False