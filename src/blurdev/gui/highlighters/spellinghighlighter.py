##
#	\namespace	blurdev.gui.highlighters.spellinghighlighter
#
#	\remarks	Uses the enchant spell checking system to highlight incorrectly spelled words
#
#	\sa			http://www.rfk.id.au/software/pyenchant/download.html
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		11/12/08
#

from PyQt4.QtGui import QSyntaxHighlighter

# import the enchant library
enchant = None
try:
	import enchant
except:
	from blurdev import debug
	debug.debugMsg( '[blurdev.gui.highlighters.spellinghighlighter] - pyenchant library could not be found' )

class SpellingHighlighter( QSyntaxHighlighter ):
	def __init__( self, widget, language = 'en_US' ):
		QSyntaxHighlighter.__init__( self, widget )
		
		# define custom properties
		self._active		= False
		self._dictionary 	= None
		
		# set the dictionary language
		self.setLanguage( language )
		
	def isActive( self ):
		""" checks to see if this highlighter is in console mode """
		return self._active
	
	def isValid( self ):
		return enchant != None
	
	def highlightBlock( self, text ):
		""" highlights the inputed text block based on the rules of this code highlighter """
		if ( self.isActive() and self._dictionary ):
			from PyQt4.QtCore 	import QRegExp, Qt
			from PyQt4.QtGui 	import QTextCharFormat, QColor
			
			# create the format
			format = QTextCharFormat()
			format.setUnderlineColor( QColor( Qt.red ) )
			format.setUnderlineStyle( QTextCharFormat.WaveUnderline )
			format.setFontUnderline( True )
			
			# create the regexp
			expr = QRegExp( r'\S+' )
			pos = expr.indexIn( text, 0 )
		
			# highlight all the given matches to the expression in the text
			while ( pos != -1 ):
				pos 	= expr.pos()
				length	= expr.cap().length()
				
				# extract the text chunk for highlighting
				chunk = text[pos:pos+length]
				
				if ( not self._dictionary.check( chunk ) ):
					# set the formatting
					self.setFormat( pos, length, format )
				
				# update the expression location
				matched = expr.matchedLength()
				pos = expr.indexIn( text, pos + matched )
			
	def setActive( self, state = True ):
		""" sets the highlighter to only apply to console strings (lines starting with >>>) """
		self._active = state
		self.rehighlight()
	
	def setLanguage( self, lang ):
		""" sets the language of the highlighter by loading """
		if ( enchant ):
			self._dictionary = enchant.Dict( lang )
			return True
		else:
			self._dictionary = None
			return False
		
	@staticmethod
	def test():
		from blurdev.gui import Dialog
		from PyQt4.QtGui import QTextEdit, QVBoxLayout
		dlg = Dialog()
		dlg.setWindowTitle( 'Spell Check Test' )
		
		edit = QTextEdit(dlg)
		h = SpellingHighlighter(edit)
		h.setActive(True)
		
		layout = QVBoxLayout()
		layout.addWidget(edit)
		dlg.setLayout(layout)
		
		dlg.show()