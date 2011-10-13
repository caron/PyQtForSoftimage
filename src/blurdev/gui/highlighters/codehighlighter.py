##
#	\namespace	blurdev.gui.highlighter
#
#	\remarks	Handles generic code highlighting based on an XML file
#				The language definitions files for blurdev can be found in [blurdev]/config/lang/*.xml
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		11/12/08
#

from PyQt4.QtGui import QSyntaxHighlighter

class CodeHighlighter( QSyntaxHighlighter ):
	def __init__( self, widget ):
		QSyntaxHighlighter.__init__( self, widget )
		
		# setup the search rules
		self._keywords 		= []
		self._strings		= []
		self._comments		= []
		self._consoleMode	= False
		
		# setup the font
		font = widget.font()
		font.setFamily( 'Courier New' )
		widget.setFont( font )
	
	def commentFormat( self ):
		""" returns the comments QTextCharFormat for this highlighter """
		from PyQt4.QtGui import QTextCharFormat, QColor
		
		format = QTextCharFormat()
		format.setForeground( QColor( 0, 206, 52 ) )
		format.setFontItalic( True )
		
		return format
	
	def isConsoleMode( self ):
		""" checks to see if this highlighter is in console mode """
		return self._consoleMode
	
	def highlightBlock( self, text ):
		""" highlights the inputed text block based on the rules of this code highlighter """
		if ( not self.isConsoleMode() or str( text ).startswith( '>>>' ) ):
			from PyQt4.QtCore import QRegExp
			
			# format the keywords
			format = self.keywordFormat()
			for kwd in self._keywords:
				self.highlightText( text, QRegExp( r'\b%s\b' % kwd ), format )
			
			# format the strings
			format = self.stringFormat()
			for string in self._strings:
				self.highlightText( text, QRegExp( '%s[^%s]*' % (string,string) ), format, includeLast = True )
			
			# format the comments
			format = self.commentFormat()
			for comment in self._comments:
				self.highlightText( text, QRegExp( comment ), format )
	
	def highlightText( self, text, expr, format, offset = 0, includeLast = False ):
		"""
			\remarks	Highlights a text group with an expression and format
			
			\param		text		<str> || <QString>		text to highlight
			\param		expr		<QRegExp>				search parameter
			\param		format		<QTextCharFormat>		formatting rule
			\param		offset		<int>					number of characters to offset by when highlighting
			\param		includeLast	<bool>					whether or not the last character should be highlighted
			
			\return		<void>
		"""
		pos = expr.indexIn( text, 0 )
		
		# highlight all the given matches to the expression in the text
		while ( pos != -1 ):
			pos 	= expr.pos(offset)
			length	= expr.cap(offset).length()
			
			# use the last character if desired
			if ( includeLast ):
				length += 1
			
			# set the formatting
			self.setFormat( pos, length, format )
			
			matched = expr.matchedLength()
			if ( includeLast ):
				matched += 1
			
			pos = expr.indexIn( text, pos + matched )
	
	def keywordFormat( self ):
		""" returns the keywords QTextCharFormat for this highlighter """
		from PyQt4.QtGui import QTextCharFormat, QColor
		
		format  = QTextCharFormat()
		format.setForeground( QColor( 17, 154, 255 ) )
		
		return format
	
	def setConsoleMode( self, state = False ):
		""" sets the highlighter to only apply to console strings (lines starting with >>>) """
		self._consoleMode = state
	
	def setLanguage( self, lang ):
		""" sets the language of the highlighter by loading the XML definition """
		from blurdev.XML import XMLDocument
		import blurdev
		import os.path
		doc = XMLDocument()
		if ( doc.load( blurdev.resourcePath( 'lang/%s.xml' % lang ) ) ):
			# clear out the current definition
			root = doc.root()
			self.setObjectName( root.attribute( 'name' ) )
			
			# clear the current definitions
			self._keywords 	= []
			self._comments 	= []
			self._strings	= []
			
			# load the keywords
			kwds = root.findChild( 'keywords' )
			if ( kwds ):
				for kwd in kwds.children():
					self._keywords.append( kwd.attribute( 'value' ) )
			
			# load the comments
			comments = root.findChild( 'comments' )
			if ( comments ):
				for comment in comments.children():
					self._comments.append( comment.attribute( 'value' ) )
			
			# load the strings
			strings = root.findChild( 'strings' )
			if ( strings ):
				for string in strings.children():
					self._strings.append( string.attribute( 'value' ) )
			
			return True
		return False
	
	def stringFormat( self ):
		""" returns the keywords QTextCharFormat for this highligter """
		from PyQt4.QtGui import QTextCharFormat, QColor
		
		format 	= QTextCharFormat()
		format.setForeground( QColor( 255, 128, 0 ) )
		
		return format