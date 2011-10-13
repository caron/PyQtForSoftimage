##
#	\namespace	blurdev.gui.windows.loggerwindow.loggerwindow
#
#	\remarks	LoggerWindow class is an overloaded python interpreter for blurdev
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		01/15/08
#

from PyQt4.QtCore					import QObject
from PyQt4.QtGui 					import QTextEdit
import __main__

emailformat = """
<html>
	<head>
		<style>
			body {
				font-family: Verdana, sans-serif;
				font-size: 12px;
				color:#484848;
				background:lightGray;
			}
			h1, h2, h3 { font-family: "Trebuchet MS", Verdana, sans-serif; margin: 0px; }
			h1 { font-size: 1.2em; }
			h2, h3 { font-size: 1.1em; }
			a, a:link, a:visited { color: #2A5685;}
			a:hover, a:active { color: #c61a1a; }
			a.wiki-anchor { display: none; }
			hr {
				width: 100%%;
				height: 1px;
				background: gray;
				border: 0;
			}
			.footer {
				font-size: 0.9em;
				font-style: italic;
			}
		</style>
	</head>
	<body>
		<h1>%(subject)s</h1>
		<br><br>
		%(body)s
		<br><br><br><br>
		<hr/>
		<span class="footer">
			<p>You have received this notification because you have either subscribed to it, or are involved in it.<br/>
			To change your notification preferences, go into trax and change your options settings.
			</p>
		</span>
	</body>
</html>
"""

#----------------------------------------------------------------

class ErrorLog( QObject ):
	def flush( self ):
		""" flush the logger instance """
		self.parent().flush()
	
	def write( self, msg ):
		""" log an error message """
		self.parent().write( msg, error = True )

#----------------------------------------------------------------
		
class ConsoleEdit( QTextEdit ):
	def __init__( self, parent ):
		QTextEdit.__init__( self, parent )
		
		# store the error buffer
		self._completer		= None
		
		from PyQt4.QtCore import QTimer
		self._errorTimer	= QTimer()
		self._errorTimer.setSingleShot(True)
		self._errorTimer.timeout.connect( self.handleError )
		
		# create the completer
		from completer import PythonCompleter
		self.setCompleter( PythonCompleter( self ) )
		
		# overload the sys logger (if we are not on a high debugging level)
		from blurdev import debug
		if ( debug.debugLevel() != debug.DebugLevel.High ):
			import sys
			sys.stdout 	= self
			sys.stderr	= ErrorLog(self)
		
		# create the highlighter
		from blurdev.gui.highlighters.codehighlighter import CodeHighlighter
		highlight = CodeHighlighter(self)
		highlight.setLanguage( 'Python' )
		
		self.startInputLine()
	
	def clear( self ):
		""" clears the text in the editor """
		QTextEdit.clear( self )
		self.startInputLine()
	
	def completer( self ):
		""" returns the completer instance that is associated with this editor """
		return self._completer
	
	def emailError( self, emails, error ):
		from blurdev import debug
		
		# do not email when debugging
		if ( debug.debugLevel() ):
			return
		
		# get current user
		try:
			import win32api
			username 	= win32api.GetUserName()
		except:
			username 	= 'Anonymous'
		
		# get current host
		try:
			import socket
			host = socket.gethostname()
		except:
			host = 'Unknown'
			
		# Build the brief & subject information	
		subject = '[Python Error] %s' % error.split( '\n' )[-2]
		
		# Build the message
		message = [ '<ul>' ]
		
		import sys
		from PyQt4.QtCore import QDateTime
		message.append( '<li><b>user: </b>%s</li>' % username )
		message.append( '<li><b>host: </b>%s</li>' % host )
		message.append( '<li><b>date: </b>%s</li>' % QDateTime.currentDateTime().toString( 'MMM dd, yyyy @ h:mm ap' ) )
		message.append( '<li><b>python: </b>%s</li>' % sys.version )
		
		# notify where the error came from
		from PyQt4.QtGui import QApplication
		window = QApplication.activeWindow()
		
		# use the root application
		if ( window.__class__.__name__ == 'LoggerWindow' ):
			window = window.parent()
			
		if ( window ):
			message.append( '<li><b>window: </b>%s (from %s Class)</li>' % (window.objectName(),window.__class__.__name__) )
		
		message.append( '</ul>' )
		message.append( '<br>' )
		message.append( '<h3>Traceback Printout</h3>' )
		message.append( '<hr>' )
		message.append( '<div style="background:white;color:red;padding:5 10 5 10;border:1px black solid"><pre><code>' )
		message.append( unicode( error ).replace( '\n', '<br>' ) )
		message.append( '</code></pre></div>' )
		
		import blurdev
		blurdev.core.sendEmail( 'thePipe@blur.com', emails, subject, emailformat % { 'subject': subject, 'body': '\n'.join( message ) } ) 
	
	def errorTimeout( self ):
		""" end the error lookup """
		self._timer.stop()
	
	def executeCommand( self ):
		""" executes the current line of code """
		import re
		
		# grab the command from the line
		block 	= self.textCursor().block().text()
		results	= re.search( '>>> (.*)', unicode(block) )
		
		if ( results ):
			# if the cursor position is at the end of the line
			if ( self.textCursor().atEnd() ):
				# insert a new line
				self.insertPlainText( '\n' )
				
				# evaluate the command
				cmdresult = None
				try:
					cmdresult = eval( unicode( results.groups()[0] ), __main__.__dict__, __main__.__dict__ )
				except:
					exec ( unicode( results.groups()[0] ) ) in __main__.__dict__, __main__.__dict__
				
				# print the resulting commands
				if ( cmdresult != None ):
					self.write( unicode( cmdresult ) )
				
				self.startInputLine()
			
			# otherwise, move the command to the end of the line
			else:
				self.startInputLine()
				self.insertPlainText( unicode( results.groups()[0] ) )
				
		# if no command, then start a new line
		else:
			self.startInputLine()
	
	def focusInEvent( self, event ):
		""" overload the focus in event to ensure the completer has the proper widget """
		if ( self.completer() ):
			self.completer().setWidget( self )
		QTextEdit.focusInEvent( self, event )
	
	def insertCompletion( self, completion ):
		""" inserts the completion text into the editor """
		if ( self.completer().widget() == self ):
			from PyQt4.QtGui import QTextCursor
			
			cursor 	= self.textCursor()
			cursor.movePosition( QTextCursor.Left )
			cursor.movePosition( QTextCursor.EndOfWord )
			cursor.insertText( completion[len(self.completer().completionPrefix()):] )
			self.setTextCursor( cursor )
	
	def insertFromMimeData( self, mimeData ):
		html = False
		if mimeData.hasHtml():
			text = mimeData.html()
			html = True
		else:
			text = mimeData.text()
			
		from PyQt4.QtGui import QTextDocument
		doc = QTextDocument()
			
		if ( html ):
			doc.setHtml( text )
		else:
			doc.setPlainText( text )
		
		text = doc.toPlainText()
		
		import re
		exp = re.compile( '[^A-Za-z0-9\~\!\@\#\$\%\^\&\*\(\)\_\+\{\}\|\:\"\<\>\?\`\-\=\[\]\\\;\'\,\.\/ \t\n]' )
		newText = unicode( text ).encode( 'utf-8' )
		for each in exp.findall(newText):
			newText = newText.replace( each, '?' )
		
		self.insertPlainText( newText )
	
	def lastError( self ):
		import traceback, sys
		return ''.join( traceback.format_exception( sys.last_type, sys.last_value, sys.last_traceback ) )
	
	def keyPressEvent( self, event ):
		""" overload the key press event to handle custom events """
		
		from PyQt4.QtCore import Qt
		
		# enter || return keys will execute the command
		if ( event.key() in (Qt.Key_Return,Qt.Key_Enter) ):
			if ( self.completer().popup().isVisible() ):
				self.completer().popup().hide()
				event.ignore()
			else:
				self.executeCommand()
		
		# home key will move the cursor to home
		elif ( event.key() == Qt.Key_Home ):
			self.moveToHome()
		
		# otherwise, ignore the event for completion events
		elif ( event.key() in (Qt.Key_Tab,Qt.Key_Backtab) ):
			self.insertCompletion( self.completer().currentCompletion() )
			self.completer().popup().hide()
			
		elif ( event.key() == Qt.Key_Escape ):
			self.completer().popup().hide()
		
		# other wise handle the keypress
		else:
			QTextEdit.keyPressEvent( self, event )
			
			# check for particular events for the completion
			if ( self.completer() and not (event.modifiers() and event.text().isEmpty()) ):
				self.completer().refreshList( scope = __main__.__dict__ )
				self.completer().popup().setCurrentIndex( self.completer().completionModel().index(0,0) )
			
			rect = self.cursorRect()
			rect.setWidth( self.completer().popup().sizeHintForColumn(0) + self.completer().popup().verticalScrollBar().sizeHint().width() )
			self.completer().complete(rect)
	
	def moveToHome( self ):
		""" moves the cursor to the home location """
		from PyQt4.QtCore	import Qt
		from PyQt4.QtGui 	import QTextCursor, QApplication
		
		mode = QTextCursor.MoveAnchor
		
		# select the home
		if ( QApplication.instance().keyboardModifiers() == Qt.ShiftModifier ):
			mode = QTextCursor.KeepAnchor
		
		# grab the cursor
		cursor	= self.textCursor()
		block	= unicode( cursor.block().text() ).split()
		cursor.movePosition( QTextCursor.StartOfBlock, mode )
		cursor.movePosition( QTextCursor.Right, mode, 4 ) # the line is 4 characters long (>>> )
		self.setTextCursor( cursor )
	
	def setCompleter( self, completer ):
		""" sets the completer instance for this widget """
		if ( completer ):
			self._completer = completer
			completer.setWidget( self )
			completer.activated.connect( self.insertCompletion )
	
	def startInputLine( self ):
		""" create a new command prompt line """
		from PyQt4.QtCore import Qt
		from PyQt4.QtGui import QTextCursor
		from PyQt4.QtGui import QTextCharFormat
		
		self.moveCursor( QTextCursor.End )
		
		# if this is not already a new line
		if ( self.textCursor().block().text() != '>>> ' ):
			charFormat = QTextCharFormat()
			charFormat.setForeground( Qt.lightGray )
			self.setCurrentCharFormat( charFormat )
			
			inputstr = '>>> '
			if ( unicode( self.textCursor().block().text() ) ):
				inputstr = '\n' + inputstr
			
			self.insertPlainText( inputstr )
		
	def handleError( self ):
		""" process an error event handling """
		
		# determine the error email path
		from blurdev.tools import ToolsEnvironment
		emails = ToolsEnvironment.activeEnvironment().emailOnError()
		if ( emails ):
			self.emailError( emails, ''.join( self.lastError() ) )
		
		# if the logger is not visible, prompt the user
		from blurdev.gui.windows.loggerwindow import LoggerWindow
		inst = LoggerWindow.instance()
		if ( not inst.isVisible() ):
			from PyQt4.QtGui import QMessageBox
			import blurdev
			result = QMessageBox.question( blurdev.core.rootWindow(), 'Error Occurred', 'An error has occurred in your Python script.  Would you like to see the log?', QMessageBox.Yes | QMessageBox.No )
			if ( result == QMessageBox.Yes ):
				inst.show()
		
	def write( self, msg, error = False ):
		""" write the message to the logger """
		from PyQt4.QtCore import Qt
		from PyQt4.QtGui import QTextCharFormat
		from PyQt4.QtGui import QTextCursor, QColor
		
		self.moveCursor( QTextCursor.End )
		charFormat = QTextCharFormat()
		
		if ( not error ):
			charFormat.setForeground( QColor( 17, 154, 255 ) )
		else:
			# start recording information to the error buffer
			self._errorTimer.stop()
			self._errorTimer.start( 50 )
			
			charFormat.setForeground( Qt.red )
		
		self.setCurrentCharFormat( charFormat )
		self.insertPlainText( msg )