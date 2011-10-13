##
#	\namespace	blurdev.tools.toolheader
#
#	\remarks	Creates the ToolHeader class parses a tool file for header information
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		06/11/10
#

import os.path

HEADER_HTML = """
<html>
	<header>
		<style>
			body { 
				font-family: verdana; 
				font-size: 10px; 
				background: #cccccc;
				color: black;
			}
			h1 { 
				font-weight: bold;
				font-size: 1.1em;
				color: blue;
			}
		</style>
	</header>
	<body>
		%(body)s
	</body>
</html>
"""

from PyQt4.QtCore 		import QObject

class ToolHeader( QObject ):
	def __init__( self, tool ):
		QObject.__init__( self, tool )
	
	def html( self ):
		filename 	= self.parent().sourcefile()
		
		if ( not os.path.exists( filename ) ):
			return self.blankHeader()
		
		# load the code
		f = open( filename )
		filecode = f.readlines()
		f.close()
		
		# determine how to parse the code
		ext 		= os.path.splitext( filename )[1]
		
		# parse a maxscript header file
		if ( ext.startswith( '.ms' ) ):
			return self.parseMaxscript( filecode )
			
		# parse a python header file
		elif ( ext.startswith( '.py' ) ):
			return self.parsePython( filecode )
		
		return self.blankHeader()
	
	@staticmethod
	def blankHeader():
		return HEADER_HTML % { 'body': '' }
	
	@staticmethod
	def parseMaxscript( lines ):
		import re
		
		header 			= [ '<p>' ]
		open_comment 	= False
		
		paragraph		= re.compile( r'[- \t]*$' )
		boldOld         = re.compile( r'[- \t]*\[([^\]]+)*\](.*)$' )
		bold			= re.compile( r'[- \t]*\\([a-zA-Z0-9]+)(.*)$' )
		lastTitle		= ''
		
		for line in lines:
			# check for open comment lines
			if ( '/*' in line ):
				open_comment = True
				line = line.lstrip( '/*!' ).lstrip( '/*' )
			
			# exit out of the header parsing when comments are done
			elif ( '*/' in line or not ( open_comment or line.startswith( '--' ) ) ):
				break
				
			results = paragraph.match( line )
			
			line = line.lstrip( '-' ).strip()
			
			if ( line and not line.isspace() and not '__MXSDOC__' in line ):
				# strip out the bold comments
				title = ''
				text  = ''
				results = boldOld.match( line )
				
				if ( results ):
					title, text = results.groups()
				
				else:
					results = bold.match( line )
					
					if ( results ):
						title, text = results.groups()
					
					else:
						text = line
						
				# create a new title
				if ( title ):
					title = title.capitalize()
					if ( title != lastTitle ):
						header.append( '</p><p><h1>%s</h1><hr>' % title )
						lastTitle = title
			
				header.append( '<br>%s' % text.lstrip( '-' ).strip().replace( '\t', '...' ) )
		
		header.append( '</p>' )
		
		return HEADER_HTML % { 'body': ''.join( header ) }

	
	@staticmethod
	def parsePython( lines ):
		import re
		
		header 			= [ '<p>' ]
		open_comment 	= False
		
		paragraph		= re.compile( r'[# \t]*$' )
		boldOld         = re.compile( r'[# \t]*\[([^\]]+)*\](.*)$' )
		bold			= re.compile( r'[# \t]*\\([a-zA-Z0-9]+)(.*)$' )
		lastTitle		= ''
		
		for line in lines:
			# exit out of the header parsing when comments are done
			if ( not line.startswith( '#' ) ):
				break
				
			results = paragraph.match( line )
			
			line = line.lstrip( '#!' ).lstrip( '#' ).strip()
			
			if ( line and not line.isspace() and not '__PYDOC__' in line ):
				# strip out the bold comments
				title = ''
				text  = ''
				results = boldOld.match( line )
				
				if ( results ):
					title, text = results.groups()
				
				else:
					results = bold.match( line )
					
					if ( results ):
						title, text = results.groups()
					
					else:
						text = line
						
				# create a new title
				if ( title ):
					title = title.capitalize()
					if ( title != lastTitle ):
						header.append( '</p><p><h1>%s</h1><hr>' % title )
						lastTitle = title
			
				header.append( '<br>%s' % text.lstrip( '-' ).strip().replace( '\t', '...' ) )
		
		header.append( '</p>' )
		
		return HEADER_HTML % { 'body': ''.join( header ) }