##
#	\namespace	blurdev.gui.windows.sdkwindow.document
#
#	\remarks	Class for generating documentation about python modules or packages
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		07/08/10
#

from PyQt4.QtCore import QObject
from blurdev.decorators import abstractmethod

class DocumentData:
	def __init__( self, name, object, dataType, public ):
		self.name 		= name
		self.object		= object
		self.dataType	= dataType
		self.public		= public
	
	def dataTypeGroup( self ):
		if ( self.public ):
			return 'public %s' % self.dataType
		else:
			return 'protected %s' % self.dataType

class Document( QObject ):
	cache 				= {}		# store all the document instances (module/class level information)
	aliases				= {}
	reverseAliases		= {}
	
	def __init__( self ):
		QObject.__init__( self )
		
		self._object 			= None
		self._html				= ''
		self._allMembersHtml	= ''
		self._data				= {}
		self._sourceHtml		= {}
		self._title				= ''
	
	def allMembersHtml( self ):
		if ( self.isNull() or self._allMembersHtml ):
			return self._allMembersHtml
		
		html = [ '<div class="header" align="center">List of All Members for %s</div>' % (self.title()) ]
		html.append( '<div class="title" align="center">[from %s]</div>' % self.breadcrumbs( self.object() ) )
		html.append( '<hr>' )
		html.append( 'This is the complete list of members for %s, including inherited members' % self.toLink(self.object(), scopeFullName = self.objectName()) )
		html.append( '<br><br><table width="100%" height="100%"><tr>' )
		
		import inspect
		attrs = inspect.classify_class_attrs(self._object)
		attrs.sort( lambda x,y: cmp(x[0],y[0]) )
		
		if ( attrs ):
			center		= int(len(attrs)/2.0)
			firsthalf 	= attrs[:center]
			secondhalf	= attrs[center+1:]
			
			for section in (firsthalf,secondhalf):
				html.append( '<td><ul>' )
				for key, datatype, mclass, value in section:
					# grab the abstractmethods
					if ( isinstance( value, abstractmethod ) ):
						value = value.basemethod()
						
					if ( inspect.isfunction( value ) or inspect.isbuiltin( value ) or inspect.ismethod( value ) or inspect.ismethoddescriptor( value ) ):
						if ( mclass ):
							html.append( '<li>%s::<a class="simple_link" href="%s.%s#%s">%s</a>%s</li>' % (mclass.__name__,mclass.__module__,mclass.__name__,key,key,self.generateArguments(value)) )
						else:
							html.append( '<li>Unknown::%s%s, from unknown</li>' % (key,self.generateArguments(value)) )
					else:
						html.append( '<li>%s</li>' % key )
				html.append( '</ul></td>' )
				
		html.append( '</tr></table>' )
		
		self._allMembersHtml = ''.join(html)
		return self._allMembersHtml
	
	def bases( self, cls, recursive = False ):
		out = list( cls.__bases__ )
		if ( recursive ):
			for basecls in out:
				for base in self.bases( basecls, True ):
					if ( not base in out ):
						out.append( base )
		return out
	
	def defaultValueType( self, value, default = 'data' ):
		import inspect
		
		# return a module type
		if ( inspect.ismodule( value ) ):
			return 'module'
		
		# return a class type
		elif ( inspect.isclass( value ) ):
			return 'class'
		
		# return a method type
		elif ( inspect.ismethod( value ) or inspect.ismethoddescriptor( value ) ):
			return 'method'
			
		# return a built-in method
		elif ( inspect.isbuiltin( value ) ):
			return 'built-in'
		
		# return a function type
		elif ( inspect.isfunction( value )   ):
			return 'function'
		
		# return custom types
		
		# check for enums
		from blurdev.enum import enum
		if ( isinstance( value, enum ) ):
			return 'enum'
			
		# check for signals
		from PyQt4.QtCore import pyqtSignal
		if ( isinstance( value, pyqtSignal ) ):
			return 'signal'
		
		# check for abstract methods
		if ( isinstance( value, abstractmethod ) ):
			return 'abstract method'
			
		# return the default type
		return default
	
	def filename( self ):
		import inspect
		try:
			result = inspect.getsourcefile(self._object)
		except:
			result = ''
		
		if ( not type(result) == str ):
			result = str(result)
		return result
	
	def findData( self, dataType, public = None ):
		self.loadData()
		return [ item for item in self._data.values() if ( dataType in item.dataType and (public == None or item.public == public) ) ]
	
	def formatTitle( self, title ):
		title = ' '.join( [ text.capitalize() for text in title.split( ' ' ) ] )
		
		# fix proper endings
		if ( title.endswith( 'y' ) ):
			title = title[:-1] + 'ies'
		elif ( title.endswith( 's' ) ):
			title += 'es'
		else:
			title += 's'
		
		return title
		
	def loadData( self ):
		if ( self.isNull() or self._data ):
			return
			
		import inspect
		from blurdev.enum import enum
		
		class_attrs = []
		if ( inspect.isclass( self.object() ) ):
			contents = inspect.classify_class_attrs(self.object())
			for key, valuetype, defclass, value in contents:
				if ( defclass == self.object() ):
					class_attrs.append( key )
		
		from PyQt4.QtCore import pyqtSignal
		
		# try to load all items
		members = {}
		loaded = False
		try:
			members = dict(inspect.getmembers(self._object))
			for key in self._object.__dict__.keys():
				if ( not key in members ):
					members[key] = self._object.__dict__[key]
			loaded = True
		except:
			pass
		
		if ( not loaded ):
			try:
				members = dict(inspect.getmembers(self._object))
				loaded = True
			except:
				pass
		
		if ( not loaded ):
			try:
				members = self._object.__dict__
			except:
				pass
				
		for key, value in members.items():
			# ignore built-ins & 'private' variables
			if ( key.startswith( '__' ) ):
				continue
			
			# ignore inherited items
			if ( class_attrs and not key in class_attrs ):
				continue
				
			public 		= not key.startswith( '_' )
			dataType	= self.defaultValueType( value, 'variable' )
			self._data[ key ] = DocumentData( key, value, dataType, public )
		
	def isNull( self ):
		return self._object == None
	
	def object( self ):
		return self._object
		
	def generateDocs( self, item ):
		import re, inspect
		
		# use the base method for abstractmethods
		warning = ''
		if ( isinstance( item, abstractmethod ) ):
			item = item.basemethod()
			warning = 'This method is abstract and should be redefined in a sub-class'
		
		# get the documentation
		try:
			docs = inspect.getdoc(item)
		except:
			docs = ''
		
		# get the comments
		if ( not docs ):
			docs = inspect.getcomments( item )
			
		if ( not docs ):
			return ''
		
		lines 			= docs.replace( '\r', '\\r' ).split( '\n' )
		lastHeader		= ''
		
		html			= [ '<p><div class="docblock">' ]
		
		if ( warning ):
			html.insert( 0, '<p><div class="warning">%s</div></p>' % warning )
		
		headermap				= {}
		headermap[ 'param' ] 	= 'Parameters'
		headermap[ 'sa' ]		= 'See Also'
		headermap[ 'shortcuts' ]	= 'Keyboard Shortcuts'
		
		tabled_headers = {}
		tabled_headers[ 'Parameters' ] = 3
		tabled_headers[ 'Keyboard Shortcuts' ] = 2
		
		# store whether or not we're in code
		code					= False
		linkRE					= re.compile( '&lt;([^\&]+)&gt;' )			# link regular expression
		saRE					= re.compile( '([a-zA-Z0-9\._]+)' )	# see also regular expression
		
		for line in lines:
			line = line.replace( '\r', '\\r' ).strip().strip( '#' ).strip( '-' ).replace( '\b', '\\b' ).replace( '<', '&lt;' ).replace( '>', '&gt;' ).strip()
			
			if ( line and not line.isspace() ):
				results = re.match( '\\\([A-Za-z]+)(.*)', line )
				
				# update the header information
				if ( results and results.groups() ):
					header 	= headermap.get( results.groups()[0], results.groups()[0].capitalize() )
					line 	= results.groups()[1]
					
					if ( header != lastHeader ):
						# end parameters
						if ( lastHeader in tabled_headers ):
							html.append( '</table><br>' )
						elif ( lastHeader == 'Warning' ):
							html.append( '</div></td></tr></table><br>' )
						
						if ( header != 'Warning' ):
							html.append( '</div><div class="docheader">%s</div><div class="docblock">' % header )
						else:
							html.append( '</div><table width="100%" border="1"><tr><td color="green" align="center">Note</td></tr><tr><td><div class="docblock">' )
						
						# start parameters
						if ( header in tabled_headers ):
							html.append( '<table width="100%">' )
						
						lastHeader = header
				
				IS_CODE = line.strip().startswith( '|' )
				
				# update the line linkings
				link_results = []
				if ( not IS_CODE ):
					link_results = linkRE.findall( line )
					if ( lastHeader == 'See Also' ):
						link_results += saRE.findall(line)
					
				for link_result in link_results:
					link_search = link_result.replace('&lt;','').replace('&rt;','')
					title		= link_search
					found 		= False
					
					if ( link_search in Document.aliases ):
						link_search = Document.aliases[link_search]
					
					if ( link_search in Document.cache ):
						line = line.replace( link_result, '<a class="simple_link" href="%s">%s</a>' % (link_search,title) )
					elif ( link_search.split('.')[-1] in Document.cache ):
						line = line.replace( link_result, '<a class="simple_link" href="%s">%s</a>' % (link_search.split('.')[-1],title) )
					else:
						try:
							members = dict(inspect.getmembers(self._object))
						except:
							members = {}
						
						if ( link_search in members ):
							line = line.replace( link_result, self.toLink(members[link_result]) )
					
				# collect parameters
				if ( lastHeader in tabled_headers ):
					cellcount = tabled_headers[lastHeader]
					split = [ entry for entry in line.strip().replace( '\t', '    ' ).split( '    ' ) if entry and not entry.isspace() ]
					while ( len( split ) < cellcount ):
						split.append( '' )
					
					text = '<tr>'
					for i, entry in enumerate( split ):
						if ( i == (cellcount - 1) ):
							text += '<td>%s</td>' % ' '.join( split[i:] )
						else:
							text += '<td>%s</td>' % entry
							
					text += '</tr>'
					html.append( text )
					
				# add items
				else:
					# show code items
					if ( IS_CODE ):
						if ( not code ):
							html.append( '<br><pre language="Python">' )
							code = True
							
						html.append( line[1:] )
						continue
					
					# end code items
					elif ( code ):
						code = False
						html.append( '</pre><br>' )
					
					html.append( line + '<br>' )
					
		if ( lastHeader in tabled_headers ):
			html.append( '</table><br>' )
			
		html.append( '</div></p>' )
			
		return '\n'.join( html )
	
	def generateHtml( self ):
		if ( self.isNull() or self._html ):
			return self._html
	
		from blurdev.enum import enum
		import inspect
		if ( inspect.ismodule( self.object() ) ):
			return self.generateModuleDocs()
		elif ( inspect.isclass( self.object() ) ):
			return self.generateClassDocs()
		elif ( isinstance( self.object(), enum ) ):
			return self.generateEnumDocs()
		else:
			return ''
	
	def generateClassDocs( self ):
		html = [ '<div class="header" align="center">%s Class Reference</div>' % self.title() ]
		html.append( '<div class="title" align="center">[from %s]</div>' % self.breadcrumbs( self.object() ) )
		html.append( '<hr>' )
		
		# generate the contents
		html.append( '<ul><li><a class="simple_link" href="%s#allmembers">List of all members, including inherited members</a></li>' % self.objectName() )
		html.append( '<li><a class="simple_link" href="%s#source_0">View Source Code</a></li></ul>' % self.objectName() )
		
		# generate inheritance graph
		if ( self.object().__bases__ ):
			html.append( '<p>Inherits ' )
			links = []
			for base in self.object().__bases__:
				links.append( self.toLink( base ) )
			
			if ( len( links ) == 1 ):
				html.append( links[0] + '</p>' )
			else:
				html.append( ', '.join( links[:-1] ) + ' and ' + links[-1] + '</p>' )
		
		# generate inherited graph
		subclasses = self.subclasses( self.object() )
		if ( subclasses ):
			html.append( '<p>Inherited by ' )
			links = []
			for subclass in subclasses:
				links.append( self.toLink( subclass ) )
			
			if ( len( links ) == 1 ):
				html.append( links[0] + '</p>' )
			else:
				html.append( ', '.join( links[:-1] ) + ' and ' + links[-1] + '</p>' )
		
		html.append( self.generateClassSummary( self.object() ) )
		html.append( '<hr>' )
		
		# generate main documentation
		docs = self.generateDocs( self.object() )
		if ( docs ):
			html.append( '<div class="header">Class Documentation</div>' )
			html.append( docs )
		
		html.append( self.generateMainDocumentation( 'Member Method Documentation', self.findData( 'method' ) + self.findData( 'function' ) ) )
		
		return '\n'.join( html )
	
	def generateClassSummary( self, cls ):
		import inspect
		
		contents 	= inspect.classify_class_attrs(cls)
		contents.sort( lambda x,y: cmp( x[0].lower(), y[0].lower() ) )
			
		groups 		= {}
		inherits 	= {}
		from PyQt4.QtCore import pyqtSignal
		
		for key, valuetype, defclass, value in contents:
			value 	= getattr( cls, key )
			
			# if its an unknown type
			if ( valuetype == 'data' ):
				valuetype = self.defaultValueType( value, 'member' )
			
			# determine if this is protected or public
			if ( key.startswith( '_' ) ):
				valuetype = 'protected %s' % valuetype
			else:
				valuetype = 'public %s' % valuetype
			
			grpname = valuetype
			
			# ignore built-ins
			if ( key.startswith( '__' ) ):
				continue
				
			if ( defclass == cls ):
				if ( 'method' in grpname ):
					summary = '<li>def <a class="simple_link" href="%s.%s#%s">%s</a>%s</li>' % (cls.__module__,cls.__name__,key,key,self.generateArguments(value))
				else:
					summary = '<li>%s</li>' % key
				
				if ( not grpname in groups ):
					groups[ grpname ] = [ summary ]
				else:
					groups[ grpname ].append( summary )
			else:
				if ( grpname in inherits and defclass in inherits[grpname] ):
					inherits[grpname][defclass] += 1
				elif ( grpname in inherits ):
					inherits[grpname][defclass] = 1
				else:
					inherits[grpname] = { defclass: 1 }
			
		grpnames = groups.keys()
		grpnames.sort()
		
		html = []
		for grpname in grpnames:
			title = self.formatTitle(grpname)
			html.append( '<div class="group">%s</div><ul>' % title )
			html.append( '\n'.join( groups[grpname] ) )
			html.append( '</ul>' )
			inherit = inherits.get( grpname )
			if ( inherit ):
				keys = inherit.keys()
				keys.sort( lambda x,y: cmp( x.__name__, y.__name__ ) )
				
				html.append( '<ul>' )
				for key in keys:
					html.append( '<li>%i %s(s) inherited from %s</li>' % (inherit[key],grpname,self.toLink(key)) )
				html.append( '</ul>' )
			
		# create additional includes
		unfound = [ key for key in inherits if not key in groups ]
		if ( unfound ):
			html.append( '<div class="group">Additional Inherited Members</div><ul>' )
			for key in unfound:
				keys = inherits[key].keys()
				keys.sort( lambda x,y: cmp( x.__name__, y.__name__ ) )
				
				for subkey in keys:
					html.append( '<li>%i member(s) inherited from %s</li>' % (inherits[key][subkey],self.toLink(subkey)))
			html.append( '</ul>' )
		
		return '\n'.join( html )
	
	def generateEnumDocs( self ):
		import os.path
		html = []
		
		# create the header
		html.append( '<div class="header" align="center">%s Enum Reference</div>' % (self.title()) )
		html.append( '<div class="title" align="center">[from %s]</div>' % self.breadcrumbs( str(self.objectName()) ) )
		html.append( '<hr><br>' )
		
		# generate the contents
		html.append( '%s is an <a class="simple_link" href="blurdev.enum.enum">enum</a> instance.<br><br>' % self.title() )
		html.append( 'These are the keys that can be used for this type:<br>' )
		html.append( '<table width="100%"><tr><td align="center"><table width="40%">' )
		html.append( '<thead><tr><th>Key</th><th>Value</th></tr></thead>' )
		html.append( '<tbody>' )
		html.append( '<tr><td colspan="2"><hr/></td></tr>' )
		for key in self.object().keys():
			html.append( '<tr><td align="center">%s</td><td align="center">%i</td></tr>' % (key,self.object().value(key)) )
		html.append( '</tbody>' )
		html.append( '</table></td></tr></table>' )
			
		return '\n'.join( html )
		
	def generateMainDocumentation( self, name, data ):
		if ( not data ):
			return ''
			
		import inspect
		
		# collect the bases and subclasses
		bases 		= []
		subclasses 	= []
		if ( inspect.isclass( self.object() ) ):
			bases 		= self.bases( self.object(), recursive = True )
			subclasses 	= self.subclasses( self.object(), recursive = True )
		
		# store this objects module
		if ( inspect.isclass( self.object() ) ):
			omodule = inspect.getmodule( self.object() )
		else:
			omodule = self.object()
		
		# load the data
		html = []
		html.append( '<br><div class="header">%s</div>' % name )
		
		data.sort( lambda x,y: cmp( x.name, y.name ) )	
		for item in data:
			arguments	= self.generateArguments( item.object )
				
			try:
				link = "%s#source_%i" % (self.objectName(),item.object.func_code.co_firstlineno)
			except:
				link = "%s#source_0" % (self.objectName())
			
			html.append( '<div class="function"><a name="%s">def %s%s</a></div>' % (item.name,item.name,arguments) )
			html.append( '<div class="documentation">' )
			
			# Look up reimplimentations
			links 		= [ self.toLink(base, anchor = item.name) for base in bases if item.name in base.__dict__ ]
			if ( links ):
				html.append( '<br>Reimplemented from %s.' % ( ', '.join( links ) ) )
				
			links = [ self.toLink(subcls, anchor = item.name) for subcls in subclasses if item.name in subcls.__dict__ ]
			if ( links ):
				html.append( '<br>Reimplemented by %s.' % ( ', '.join( links ) ) )
			
			html.append( self.generateDocs( item.object ) )
			
			try:
				module = inspect.getmodule( function )
			except:
				module = None
			
			if ( module and module != omodule ):
				html.append( '<br><br><b> imported from </b>' % self.breadcrumbs( module ) )
				
			html.append( '<br><a class="simple_link" href="%s">View Source</a></div><hr>' % link )
		
		return '\n'.join( html )
	
	def generateModuleDocs( self ):
		import os.path
		html = []
		
		doctype = 'Module'
		if ( os.path.basename( self.object().__file__ ).split( '.' )[0] == '__init__' ):
			doctype = 'Package'
		
		# create the header
		html.append( '<div class="header" align="center">%s %s Reference</div>' % (self.title(),doctype) )
		html.append( '<div class="title" align="center">[from %s]</div>' % self.breadcrumbs( self.object() ) )
		html.append( '<hr>' )
		html.append( '<br><a class="simple_link" href="%s#source_0">View Source Code</a>' % self.objectName() )
		
		# generate the contents
		self.loadData()
		
		grouping = {}
		values	= self._data.values()
		values.sort(lambda x,y: cmp(x.name,y.name))
		for data in values:
			dtype = data.dataTypeGroup()
			if ( not dtype in grouping ):
				grouping[dtype] = [data]
			else:
				grouping[dtype].append(data)
		
		keys = grouping.keys()
		keys.sort()
		
		for key in keys:
			html.append( self.generateSummary( key, grouping[key] ) )
		
		html.append( '<hr>' )
		
		# generate main documentation
		docs = self.generateDocs( self.object() )
		if ( docs ):
			html.append( '<div class="header">Module Documentation</div>' )
			html.append( docs )
		
		html.append( self.generateMainDocumentation( 'Module Function Documentation', self.findData( 'function' ) ) )
		
		return '\n'.join( html )
	
	def generateArguments( self, function ):
		import inspect, new
		
		# pull the abstractmethod's function
		if ( isinstance( function, abstractmethod ) ):
			function = function.basemethod()
		
		try:
			return inspect.formatargspec( *inspect.getargspec( function ) )
		except:
			pass
		
		try:
			return self.generateArguments( function.im_func )
		except:
			pass
	
		if ( isinstance( function, new.instancemethod ) and hasattr( function, 'func_args' ) ):
			return function.func_args
		
		return '( ??? )'
	
	def generateSummary( self, title, data, columns = 2 ):
		if ( not data ):
			return ''
		
		title = self.formatTitle(title)
		# split data into columns
		data.sort( lambda x,y: cmp( x.name.lower(), y.name.lower() ) )
		
		coldata		= []
		if ( columns > 1 ):
			colmax		= int( len( data ) / float( columns ) )
			if ( colmax ):
				currlist	= []
				for item in data:
					currlist.append( item )
					if ( len( currlist ) == colmax ):
						coldata.append( currlist )
						currlist = []
			else:
				coldata = [ data ]
		else:
			coldata = [ data ]
		
		# generate the html
		import inspect
		html = [ '<div class="group">%s</div><br><table width="100%%"><tr>' % title ]
		for colitems in coldata:
			html.append( '<td width"45%"><ul>' )
			
			for item in colitems:
				text = '<li class="summary">%s</li>'
				if ( item.dataType == 'function' ):
					text = '<li class="summary">def %s'
					argtext = self.generateArguments( item.object )
					if ( argtext ):
						text += '%s' % argtext
						
					text += '</li>'
				
				link = self.toLink( item.object, item.name, '%s.%s' % (self.objectName(),item.name) )
				if ( not link ):
					link = item.name
				html.append( text % link )
			
			html.append( '</ul></td>' )
		
		html.append( '</tr></table>' )
				
		return '\n'.join( html )
	
	def html( self ):
		if ( not self._html ):
			self._html = self.generateHtml()
		
		return self._html
	
	def search( self, text ):
		import inspect
		
		# see if its in the object's actual name
		oname 		= str(self.objectName())
		raliases	= Document.reverseAliases.get(oname,[])
		names = [ oname.lower().split('.')[-1] ] + [ str(aka).lower().split('.')[-1] for aka in raliases ]
		if ( text in names ):
			return 100
		
		# if its in part of the object's actual name
		for n in names:
			if ( text in n ):
				return int(100 * (len(text) / float(len(n))))
	
		# see if its in the object's name
		names = [ oname.lower() ] + [ str(aka).lower() for aka in raliases ]
		if ( text in names ):
			return 90
			
		# determine the % of letters that match the search
		for n in names:
			if ( text in n ):
				return int(90 * (len(text) / float(len(n))))
		
		# see if its in the object's keys
		try:
			keys = self._object.__dict__.keys()
		except:
			keys = []
		
		for key in keys:
			key = key.lower()
			if ( text == key ):
				return 50
			elif ( text in key ):
				return int(50 * (len(text) / float(len(key))))
			
		# see if its in any of the members
		try:
			keys = dict(inspect.getmembers(self._object)).keys()
		except:
			keys = []
		
		for key in keys:
			key = key.lower()
			if ( text == key ):
				return 25
			elif ( text in key ):
				return int(25 * (len(text) / float(len(key))))
		
		# return no hits
		return 0
	
	def setObject( self, object ):	
		self._object 	= object
		self._html 		= ''
		
		import inspect
		if ( inspect.isclass( object ) ):
			self.setObjectName( '%s.%s' % (object.__module__,object.__name__) )
		else:
			self.setObjectName( object.__name__ )
		self._title = str( object.__name__ )
	
	def setTitle( self, title ):
		self._title = title
	
	def subclasses( self, cls, recursive = False ):
		subclasses = []
		for document in Document.cache.values():
			try:
				if ( self.object() in document.object().__bases__ ):
					subclasses.append( document.object() )
			except:
				pass
		return subclasses
	
	def sourceHtml( self ):
		if ( not self._sourceHtml ):
			import inspect
			module = inspect.getmodule( self.object() )
			lines	= inspect.getsource( module ).split( '\n' )
			
			html = [ '<a class="simple_link" href="%s">Go back to %s</a><br>' % (self.objectName(),self.title()) ]
			html.append( '<table width="100%">' )
			for i in range( len( lines ) ):
				html.append( '<tr><td width="40"><a name="source_%i">%i</a></td><td><pre>%s</pre lang="Python"></td></tr>' % (i+1,i+1,lines[i]) )
			html.append( '</table>' )
			self._sourceHtml = '\n'.join(html)
			
		return self._sourceHtml
	
	def title( self ):
		return self._title
	
	@staticmethod
	def breadcrumbs( object ):
		import inspect
		if ( inspect.ismodule( object ) ):
			link = object.__name__
		elif ( inspect.isclass( object ) ):
			link = '%s.%s' % (object.__module__,object.__name__)
		elif ( type(object) == str ):
			link = object
		else:
			link = ''
		
		import sys
		links 		= []
		sections	= link.split( '.' )
		for i in range( len( sections ) ):
			sectionname = '.'.join( sections[:i+1] )
			if ( sectionname in Document.cache ):
				links.append( '<a class="simple_link" href="%s">%s</a>' % (sectionname,sections[i]) )
			else:
				links.append( sectionname )
				
		return '.'.join( links )
	
	@staticmethod
	def toLink( object, scopeName = '', scopeFullName = '', anchor = '' ):
		import inspect
		
		try:
			name = str( object.__name__ ).split('.')[-1]
		except:
			name = ''
			
		link = ''
		if ( inspect.ismodule( object ) ):
			try:
				link = object.__name__
			except:
				pass
			
		elif ( inspect.isclass( object ) ):
			try:
				link = '%s.%s' % (object.__module__,object.__name__)
			except:
				pass
			
		elif ( inspect.isfunction( object ) ):
			module 	= inspect.getmodule( object )
			try:
				link 	= module.__name__ + '#' + object.__name__
			except:
				pass
			
		elif ( inspect.ismethod( object ) ):
			module 	= inspect.getmodule( object )
			cls		= object.im_class
			try:
				link 	= module.__name__ + '.' + cls.__name__ + '#' + object.__name__
			except:
				pass
		
		else:
			from blurdev.enum import enum
			if ( isinstance( object, enum ) ):
				link = scopeFullName
		
		if ( scopeName and scopeName != name ):
			name = scopeName
		
		if ( link and anchor and not '#' in link ):
			link += '#' + anchor
		
		if ( link and str( link ).split( '#' )[0] in Document.cache ):
			return '<a class="simple_link" href="%s">%s</a>' % (link,name)
		else:
			return name
	
	@staticmethod
	def find( key ):
		return Document.cache.get( str( key ), Document() )
	
	@staticmethod
	def load( filename ):
		import blurdev
		from blurdev.XML import XMLDocument
		from blurdev.tools import ToolsEnvironment
		doc = XMLDocument()
		if ( doc.load( str(filename) ) ):
			# clear the document cache
			Document.cache.clear()
			
			# load the modules
			blurdev.__DOCMODE__ = True
			for child in doc.root().children():
				loc = child.attribute( 'loc' )
				if ( loc ):
					ToolsEnvironment.registerPath( loc )
					
				Document.loadModule( loc, child.attribute( 'name' ) )
			blurdev.__DOCMODE__ = False
			return True
		return False
	
	@staticmethod
	def loadModule( path, name, scope = '' ):
		import sys
		
		from blurdev import debug
		
		if ( scope ):
			modname = '.'.join( [scope, name] )
		else:
			modname = name
		
		object = None
		try:
			__import__( modname )
			object = sys.modules[ modname ]
		except:
			debug.debugObject( Document.loadModule, 'could not load: %s from %s' % (name,path) )
			return False
		
		# load sub-modules and packages
		import os.path
		if ( os.path.basename( object.__file__ ).split( '.' )[0] == '__init__' ):
			import glob
			modpath = os.path.split( object.__file__ )[0]
			modules = glob.glob( modpath + '/*.py' )
			for mod in modules:
				# ignore the __init__ file since it is our package
				if ( not '__init__.py' in os.path.basename( mod ) ):
					Document.loadModule( modpath, os.path.basename( mod ).split( '.' )[0], scope = modname )
			
			packages = glob.glob( modpath + '/*/__init__.py' )
			for package in packages:
				Document.loadModule( modpath, os.path.normpath( package ).split( os.path.sep )[-2], scope = modname )
				
		# load the module
		newdoc = Document()
		newdoc.setObject( object )
		Document.cache[ str( newdoc.objectName() ) ] = newdoc
		
		# load the class documentation
		newdoc.loadData()
		for data in newdoc.findData( 'class' ):
			Document.loadClass( data.object, aka = ('%s.%s' % (modname,data.name))  )
		
		# load the enum documentation
		for data in newdoc.findData( 'enum' ):
			Document.loadEnum( data.object, ('%s.%s' % (modname,data.name)) )
		
		return True
	
	@staticmethod
	def loadClass( cls, aka = '' ):
		objectName = '%s.%s' % (cls.__module__,cls.__name__)
		classdoc = None
		
		# load the object into the cache
		if ( not objectName in Document.cache ):
			classdoc = Document()
			classdoc.setObject( cls )
			Document.cache[ str( classdoc.objectName() ) ] = classdoc
			
			# make sure the bases are documented
			bases = cls.__bases__
			if ( bases ):
				for base in bases:
					Document.loadClass( base )
		
		# include aliases
		if ( aka and aka != objectName ):
			Document.aliases[ aka ] = objectName
			if ( not objectName in Document.reverseAliases ):
				Document.reverseAliases[objectName] = [aka]
			else:
				Document.reverseAliases[objectName].append(aka)
	
	@staticmethod
	def loadEnum( en, objectName ):
		# load the object into the cache
		if ( not objectName in Document.cache ):
			enumdoc = Document()
			enumdoc.setObject( en )
			enumdoc.setObjectName(objectName)
			enumdoc.setTitle(objectName.split('.')[-1])
			Document.cache[ str(objectName) ] = enumdoc
	
	@staticmethod
	def parse( xml ):
		import blurdev
		from blurdev.XML import XMLDocument
		from blurdev.tools import ToolsEnvironment
		doc = XMLDocument()
		if ( doc.parse( str(xml) ) ):
			# load the modules
			blurdev.__DOCMODE__ = True
			for child in doc.root().children():
				loc = child.attribute( 'loc' )
				if ( loc ):
					ToolsEnvironment.registerPath( loc )
					
				Document.loadModule( loc, child.attribute( 'name' ) )
			blurdev.__DOCMODE__ = False
			return True
		return False
	
	@staticmethod
	def moduleHierarchy():
		docs = Document.cache.values()
		docs.sort( lambda x,y: cmp( x.title(), y.title() ) )
		
		output = { '__main__': [] }
			
		for doc in docs:
			if ( doc.objectName() == doc.title() ):
				split = doc.title().split( '.' )
				if ( len( split ) == 1 ):
					output[ '__main__' ].append( doc )
				else:
					modname = '.'.join( split[:-1] )
					if ( not modname in output ):
						output[modname] = [ doc ]
					else:
						output[modname].append( doc )
		
		return output
	
	@staticmethod
	def classHierarchy():
		docs = Document.cache.values()
		docs.sort( lambda x,y: cmp( x.title(), y.title() ) )
		
		output = { '__main__': [] }
		import inspect
			
		for doc in docs:
			if ( inspect.isclass( doc.object() ) ):
				bases = doc.object().__bases__
				if ( not bases ):
					output[ '__main__' ].append( doc )
				else:
					for base in bases:
						objectName = '%s.%s' % (base.__module__,base.__name__)
						if ( not objectName in output ):
							output[ objectName ] = [ doc ]
						else:
							output[ objectName ].append( doc )
		
		return output