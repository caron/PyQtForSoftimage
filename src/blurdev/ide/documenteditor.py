##
#	\namespace	blurdev.ide.documenteditor
#
#	\remarks	This dialog allows the user to create new python classes and packages based on plugin templates
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		08/19/10
#

from PyQt4.QtCore import pyqtProperty
from PyQt4.Qsci import *

class DocumentEditor( QsciScintilla ):
	def __init__( self, parent, filename = '', lineno = 0 ):
		QsciScintilla.__init__( self, parent )
		
		# create custom properties
		self._filename 	= ''
		self._language = ''
		self._lastSearch = ''
		self._lastSearchBackward = False
		
		# initialize the look of the system
		from PyQt4.QtCore import Qt
		from PyQt4.QtGui import QFont, QFontMetrics, QColor
		font = QFont()
		font.setFamily( 'Courier New' )
		font.setFixedPitch( True )
		font.setPointSize( 9 )
		
		# set the font information
		self.setFont( font )
		mfont = QFont( font )
		mfont.setPointSize( 7 )
		self.setMarginsFont( mfont )
		
		# set the margin information
		self.setMarginWidth( 0, QFontMetrics(mfont).width( '00000' ) + 5 )
		self.setMarginLineNumbers( 0, True )
		self.setAutoIndent( True )	# automatically match line indentations on new lines
		self.setAutoCompletionSource( QsciScintilla.AcsAll )
		self.setIndentationsUseTabs( True )
		self.setTabIndents(True)
		self.setTabWidth(4)
		
		# set code folding options
		self.setFolding( QsciScintilla.BoxedTreeFoldStyle )
		
		# set brace matching
		self.setBraceMatching( QsciScintilla.SloppyBraceMatch )
		
		# set editing line color
		self.setCaretLineVisible(True)
		self.setCaretLineBackgroundColor( QColor( Qt.white ) )
		
		# set margin colors
		self.setMarginsBackgroundColor( QColor( Qt.lightGray ) )
		self.setMarginsForegroundColor( QColor( Qt.gray ) )
		self.setFoldMarginColors( QColor( Qt.yellow ), QColor( Qt.blue ) )
		
		self.setContextMenuPolicy( Qt.CustomContextMenu )
		self.customContextMenuRequested.connect( self.showMenu )
		
		# create the connections
		self.textChanged.connect( self.refreshTitle )
		
		# load the file
		if ( filename ):
			self.load( filename )
		else:
			self.refreshTitle()
		
		# goto the line
		if ( lineno ):
			self.setCursorPosition( lineno, 0 )
	
	def checkForSave( self ):
		if ( self.isModified() ):
			from PyQt4.QtGui import QMessageBox
			result = QMessageBox.question( self.window(), 'Save changes to...', 'Do you want to save your changes?', QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel )
			if ( result == QMessageBox.Yes ):
				return self.save()
			elif ( result == QMessageBox.Cancel ):
				return False
		return True
	
	def commentAdd( self ):
		from blurdev.ide import lexers
		lexerMap 	= lexers.lexerMap( self._language )
		lineComment	= ''
		if ( lexerMap ):
			lineComment = lexerMap.lineComment
			
		if ( not lineComment ):
			from PyQt4.QtGui import QMessageBox
			QMessageBox.critical( None, 'Line Comment Not Defined', 'There is no line comment symbol defined for the "%s" language' % (self._language) )
			return False
		
		# lookup the selected text positions
		startline, startcol, endline, endcol = self.getSelection()
		
		for line in range( startline, endline+1 ):
			self.setCursorPosition( line, 0 )
			self.insert( lineComment )
		return True
		
	def commentRemove( self ):
		from blurdev.ide import lexers
		lexerMap = lexers.lexerMap( self._language )
		
		lineComment	= ''
		if ( lexerMap ):
			lineComment = lexerMap.lineComment
		
		lineComment = lexerMap.lineComment
		if ( not lineComment ):
			from PyQt4.QtGui import QMessageBox
			QMessageBox.critical( None, 'Line Comment Not Defined', 'There is no line comment symbol defined for the "%s" language' % (self._language) )
			return False
		
		# lookup the selected text positions
		startline, startcol, endline, endcol = self.getSelection()
		commentlen = len(lineComment)
		
		for line in range( startline, endline+1 ):
			self.setSelection( line, 0, line, commentlen )
			if ( self.selectedText() == lineComment ):
				self.removeSelectedText()
		
		return True
		
	def exec_( self ):
		if ( self.save() ):
			import blurdev
			blurdev.core.runScript( self.filename() )
	
	def execStandalone( self ):
		if ( self.save() ):
			import os
			os.startfile( str(self.filename()) )
	
	def findInFiles( self ):
		from ideeditor import IdeEditor
		window = self.window()
		if ( isinstance( window, IdeEditor ) ):
			window.uiFindInFilesACT.triggered.emit()
	
	def goToLine( self ):
		from PyQt4.QtGui import QInputDialog
		line, accepted = QInputDialog.getInt( self, 'Line Number', 'Line:' )
		if ( accepted ):
			self.setCursorPosition( line + 1, 0 )
	
	def language( self ):
		return self._language
	
	def languageChosen( self, action ):
		if ( action.text() == 'Plain Text' ):
			self.setLanguage( '' )
		else:
			self.setLanguage( action.text() )
	
	def lineMarginWidth( self ):
		return self.marginWidth( self.SymbolMargin )
	
	def load( self, filename ):
		import os.path
		filename = str( filename )
		if ( filename and os.path.exists( filename ) ):
			self.setText( open( filename ).read() )
			
			self._filename = filename
			
			import lexers
			lexers.load()
			lexer = lexers.lexerFor( os.path.splitext( filename )[1] )
			if ( lexer ):
				lexer.setFont( self.font() )
				lexer.setParent(self)
				self._language = lexers.languageFor( lexer )
			
			self.setLexer( lexer )
			self.refreshTitle()
			self.setModified( False )
			return True
		return False
	
	def filename( self ):
		return self._filename
	
	def findNext( self, text, flags ):
		from PyQt4.QtGui import QTextDocument
		if ( not (text == self._lastSearch and not self._lastSearchBackward) ):
			self._lastSearch = text
			self._lastSearchBackward = True
			re 			= False
			cs 			= (flags & QTextDocument.FindCaseSensitively) != 0
			wo 			= (flags & QTextDocument.FindWholeWords) != 0
			wrap		= True
			forward 	= True
			
			result = self.findFirst( text, re, cs, wo, wrap, forward )
		else:
			result = QsciScintilla.findNext( self )
		
		if ( not result ):
			from PyQt4.QtGui import QMessageBox
			QMessageBox.critical( None, 'No Text Found', 'Search string "%s" was not found.' % text )
		
		return result
	
	def findPrev( self, text, flags ):
		from PyQt4.QtGui import QTextDocument
		if ( not (text == self._lastSearch and self._lastSearchBackward) ):
			self._lastSearch 			= text
			self._lastSearchBackward 	= True
			re 			= False
			cs 			= (flags & QTextDocument.FindCaseSensitively) != 0
			wo 			= (flags & QTextDocument.FindWholeWords) != 0
			wrap		= True
			forward 	= False
			
			result = self.findFirst( text, re, cs, wo, wrap, forward )
		else:
			result = QsciScintilla.findNext( self )
		
		if ( not result ):
			from PyQt4.QtGui import QMessageBox
			QMessageBox.critical( None, 'No Text Found', 'Search string "%s" was not found.' % text )
		
		return result
	
	def keyPressEvent( self, event ):
		from PyQt4.QtCore import Qt
		if (event.key() == Qt.Key_Backtab):
			self.unindentSelection()
		else:
			return QsciScintilla.keyPressEvent( self, event )
	
	def markerNext( self ):
		line, index = self.getCursorPosition()
		newline = self.markerFindNext(line+1,self.marginMarkerMask(1))
		
		# wrap around the document if necessary
		if ( newline == -1 ):
			newline = self.markerFindNext(0,self.marginMarkerMask(1))
			
		self.setCursorPosition(newline,index)
	
	def markerToggle( self ):
		line, index = self.getCursorPosition()
		markers = self.markersAtLine(line)
		if ( not markers ):
			marker = self.markerDefine( self.Circle )
			self.markerAdd( line, marker )
		else:
			self.markerDelete( line )
	
	def save( self ):
		return self.saveAs( self.filename() )
	
	def saveAs( self, filename = '' ):
		if ( not filename ):
			from PyQt4.QtGui import QFileDialog
			filename = QFileDialog.getSaveFileName( self.window(), 'Save File as...', self.filename() )
		
		if ( filename ):
			filename = str(filename)
			f = open( filename, 'w' )
			f.write( unicode(self.text()).replace( '\r', '' ) )		# scintilla puts both 
			f.close()
			
			self._filename = filename
			self.setModified( False )
			self.window().documentTitleChanged.emit()
			self.refreshTitle()
			
			import os.path
			import lexers
			lexers.load()
			lexer = lexers.lexerFor( os.path.splitext( filename )[1] )
			if ( lexer ):
				lexer.setFont( self.font() )
				self._language = lexers.languageFor( lexer )
				
			self.setLexer( lexer )
			return True
		return False
	
	def refreshTitle( self ):
		if ( self.filename() ):
			import os.path
			title = os.path.basename( str( self.filename() ) )
		else:
			title = 'New Document'
			
		if ( self.isModified() ):
			title += '*'
		
		self.setWindowTitle( title )
		parent = self.parent()
		if ( parent.inherits( 'QMdiSubWindow' ) ):
			parent.setWindowTitle( self.windowTitle() )
	
	def setLanguage( self, language ):
		language = str(language)
		self._language = language
	
		from blurdev.ide import lexers
		lexers.load()
		lexer = lexers.lexer( language )
		if ( lexer ):
			lexer.setFont(self.font())
			lexer.setParent(self)
		
		self.setLexer( lexer )
		
	def setLineMarginWidth( self, width ):
		self.setMarginWidth( self.SymbolMargin, width )
	
	def setShowFolding( self, state ):
		if ( state ):
			self.setFolding( self.BoxedTreeFoldStyle )
		else:
			self.setFolding( self.NoFoldStyle )
	
	def setShowLineNumbers( self, state ):
		self.setMarginLineNumbers( self.SymbolMargin, state )
	
	def showMenu( self ):
		from PyQt4.QtGui import QMenu, QCursor
		
		menu = QMenu( self )
		
		menu.addAction( 'Find in Files...' ).triggered.connect( self.findInFiles )
		menu.addAction( 'Go to Line...' ).triggered.connect( self.goToLine )
		
		menu.addSeparator()
		
		menu.addAction( 'Collapse/Expand All' ).triggered.connect( self.toggleFolding )
		
		menu.addSeparator()
		
		menu.addAction( 'Comment Add' ).triggered.connect( self.commentAdd )
		menu.addAction( 'Comment Remove' ).triggered.connect( self.commentRemove )
		
		menu.addSeparator()
		
		submenu = menu.addMenu( 'View as...' )
		submenu.addAction( 'Plain Text' )
		submenu.addSeparator()
		
		import lexers
		for language in lexers.languages():
			submenu.addAction( language )
		
		submenu.triggered.connect( self.languageChosen )
		
		menu.popup( QCursor.pos() )
	
	def showFolding( self ):
		return self.folding() != self.NoFoldStyle
	
	def showLineNumbers( self ):
		return self.marginLineNumbers( self.SymbolMargin )
	
	def toggleFolding( self ):
		from PyQt4.QtGui import QApplication
		from PyQt4.QtCore import Qt
		self.foldAll( QApplication.instance().keyboardModifiers() == Qt.ShiftModifier )
	
	def unindentSelection( self ):
		lineFrom 	= 0
		indexFrom 	= 0
		lineTo 		= 0
		indexTo 	= 0
		
		lineFrom, indexFrom, lineTo, indextTo = self.getSelection()
		
		for line in range(lineFrom,lineTo+1):
			self.unindent(line)
	
	# expose properties for the designer
	pyLanguage 							= pyqtProperty( "QString", 		language, 				setLanguage )
	pyLineMarginWidth					= pyqtProperty( "int",			lineMarginWidth,		setLineMarginWidth )
	pyShowLineNumbers					= pyqtProperty( "bool",			showLineNumbers,		setShowLineNumbers )
	pyShowFolding						= pyqtProperty( "bool",			showFolding,			setShowFolding )
	
	
	pyAutoCompletionCaseSensitivity		= pyqtProperty( "bool", 		QsciScintilla.autoCompletionCaseSensitivity, 		QsciScintilla.setAutoCompletionCaseSensitivity )
	pyAutoCompletionReplaceWord			= pyqtProperty( "bool", 		QsciScintilla.autoCompletionReplaceWord, 			QsciScintilla.setAutoCompletionReplaceWord )
	pyAutoCompletionShowSingle			= pyqtProperty( "bool", 		QsciScintilla.autoCompletionShowSingle, 			QsciScintilla.setAutoCompletionShowSingle )
	pyAutoCompletionThreshold			= pyqtProperty( "int",			QsciScintilla.autoCompletionThreshold, 				QsciScintilla.setAutoCompletionThreshold )
	pyAutoIndent						= pyqtProperty( "bool",			QsciScintilla.autoIndent,							QsciScintilla.setAutoIndent )
	pyBackspaceUnindents				= pyqtProperty( "bool",			QsciScintilla.backspaceUnindents,					QsciScintilla.setBackspaceUnindents )
	pyIndentationGuides					= pyqtProperty( "bool",			QsciScintilla.indentationGuides,					QsciScintilla.setIndentationGuides )
	pyIndentationsUseTabs				= pyqtProperty( "bool",			QsciScintilla.indentationsUseTabs,					QsciScintilla.setIndentationsUseTabs )
	pyTabIndents						= pyqtProperty( "bool",			QsciScintilla.tabIndents,							QsciScintilla.setTabIndents )
	pyUtf8								= pyqtProperty( "bool",			QsciScintilla.isUtf8,								QsciScintilla.setUtf8 )
	pyWhitespaceVisibility				= pyqtProperty( "bool",			QsciScintilla.whitespaceVisibility,					QsciScintilla.setWhitespaceVisibility )