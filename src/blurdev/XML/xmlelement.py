##
#	\namespace	blurapi.libs.XML.xmlelement
#
#	\remarks	defines the XML Element wrapper instance for the blurapi system
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		04/09/10
#

import xml.dom.minidom

class XMLElement:
	""" Ease of use wrapper class for <xml.dom.minidom.Element> """
	def __eq__( self, other ):
		""" checks to see if the wrapper <xml.dom.minidom.Element> instance is the same """
		result = False
		if ( isinstance( other, XMLElement ) ):
			result = ( self._object == other._object )
		return result
		
	def __getattr__( self, key ):
		""" pass along all unknown attributes to the <xml.dom.minidom.Element> class instance """
		return getattr( self._object, key )
		
	def __init__( self, object, filename = '' ):
		""" initialize the class with an <xml.dom.minidom.Element> instance """
		if ( object == None ):
			object = xml.dom.minidom.Element(None)
		self._object 	= object
		self.__file__	= filename
	
	def _document( self ):
		""" recursese up the hierarchy to find the parent who is a <xml.dom.minidom.Document> class """
		out = self._object
		while ( out and not isinstance( out, xml.dom.minidom.Document ) ):
			out = out.parentNode
		return out
	
	def _children( self ):
		""" collects the minidom child nodes which are <xml.dom.minidom.Element> types """
		if ( self._object ):
			return [ child for child in self._object.childNodes if isinstance( child, xml.dom.minidom.Element ) ]
		return []
	
	def _findRect( self, name, cls, method ):
		rect 	= cls()
		child 	= self.findChild( name )
		if ( child ):
			x = method( child.attribute( 'x', 0 ) )
			y = method( child.attribute( 'y', 0 ) )
			w = method( child.attribute( 'width', 0 ) )
			h = method( child.attribute( 'height', 0 ) )
		
			rect = cls( x, y, w, h )
			
		return rect
	
	def clear( self ):
		children = list( self._object.childNodes )
		for child in children:
			self._object.removeChild( child )
	
	def recordValue( self, value ):
		# Qt properties
		from PyQt4.QtCore	import QRect, QRectF, QPoint, QPointF, QSize, QDate, QDateTime, QString
		from PyQt4.QtGui	import QColor
		
		# Convert Qt basics to python basics where possible
		if ( type( value ) == QString ):
			value = unicode( value ).encode( 'utf-8' )
			
		valtype = type( value )
		
		# Record a list of properties
		if ( valtype in (list,tuple) ):
			self.setAttribute( 'type', 'list' )
			
			for val in value:
				entry = self.addNode( 'entry' )
				entry.recordValue( val )
		
		# Record a dictionary of properties
		elif ( valtype == dict ):
			self.setAttribute( 'type', 'dict' )
			
			for key, val in value.items():
				entry = self.addNode( 'entry' )
				entry.setAttribute( 'key', key )
				entry.recordValue( val )
			
		# Record a qdatetime
		elif ( valtype == QDateTime ):
			self.setAttribute( 'type', 'QDateTime' )
			self.setAttribute( 'value', value.toString( 'yyyy-MM-dd hh:mm:ss' ) )	
			
		# Record a qdate
		elif ( valtype == QDate ):
			self.setAttribute( 'type', 'QDate' )
			self.setAttribute( 'value', value.toString( 'yyyy-MM-dd' ) )
		
		# Record a qrect
		elif ( valtype in (QRect,QRectF) ):
			self.setAttribute( 'type', valtype.__name__ )
			self.setRect( 'rect', value )
		
		# Record a point
		elif ( valtype in (QPoint,QPointF) ):
			self.setAttribute( 'type', valtype.__name__ )
			self.setPoint( 'point', value )
		
		# Record a size
		elif ( valtype == QSize ):
			self.setAttribute( 'type', QSize )
			self.setSize( 'size', value )
		
		# Record a qcolor
		elif ( valtype == QColor ):
			self.setAttribute( 'type', 'QColor' )
			self.setColor( 'color', value )
		
		# Record a basic property
		else:
			self.setAttribute( 'value', value )
			typ = type( value ).__name__
			if ( typ == 'unicode' ):
				typ = 'str'
			self.setAttribute( 'type', typ )
	
	def restoreValue( self, fail = None ):
		from PyQt4.QtCore	import QRect, QRectF, QPoint, QPointF, QSize, QDate, QDateTime
		from PyQt4.QtGui	import QColor
		
		valtype = self.attribute( 'type' )
		value	= None
			
		# Restore a list item
		if ( valtype == 'list' ):
			value = []
			for child in self.children():
				value.append( child.restoreValue() )
		
		# Restore a dictionary item
		elif ( valtype == 'dict' ):
			value = {}
			for child in self.children():
				value[ child.attribute( 'key' ) ] = child.restoreValue()
		
		# Record a qdatetime
		elif ( valtype == 'QDateTime' ):
			value = QDateTime.fromString( self.attribute( 'value' ), 'yyyy-MM-dd hh:mm:ss' )
			
		# Record a qdate
		elif ( valtype == 'QDate' ):
			value = QDate.fromString( self.attribute( 'value' ), 'yyyy-MM-dd' )
		
		# Restore a QRect
		elif ( valtype == 'QRect' ):
			value = self.findRect( 'rect' )
		
		# Restore a QRectF
		elif ( valtype == 'QRectF' ):
			value = self.findRectF( 'rect' )
		
		# Restore a QSize
		elif ( valtype == 'QSize' ):
			value = self.findSize( 'size' )
		
		# Restore a QPoint
		elif ( valtype == 'QPoint' ):
			value = self.findPoint( 'point' )
		
		# Restore a QPointF
		elif ( valtype == 'QPointF' ):
			value = self.findPoint( 'point' )
		
		# Restore a QColor
		elif ( valtype == 'QColor' ):
			value = self.findColor( 'color' )
		
		# Restore a string
		elif ( valtype in ('str','unicode','QString') ):
			value = unicode(self.attribute( 'value' ))
		
		# Restore a basic value
		else:
			try:
				value = eval( '%s(%s)' % (valtype,self.attribute('value')) )
			except:
				value = fail
			
		return value
		
	def addComment( self, comment ):
		d = self._document()
		if ( d ):
			out = d.createComment( comment )
			self._object.appendChild( out )
			return True
		return False
	
	def addNode( self, nodeName ):
		"""
		#-------------------------------------------------------------------------------------------------------------
		#	\remarks
		#				Adds a new node child to the current element with the given node name.
		#
		#	\param		nodeName		<string>
		#
		#	\return
		#				<XML.XMLElement> || None
		#-------------------------------------------------------------------------------------------------------------
		"""
		d = self._document()
		if ( d ):
			out = d.createElement( nodeName )
			self._object.appendChild( out )
			return XMLElement( out, self.__file__ )
		return None
	
	def addChild( self, child, clone = True, deep = True ):
		if ( isinstance( child, XMLElement ) ):
			child = child._object
		
		if ( clone ):
			self._object.appendChild( child.cloneNode( deep ) )
		else:
			self._object.appendChild( child )
	
	def attribute( self, attr, fail = '' ):
		"""
		#-------------------------------------------------------------------------------------------------------------
		#	\remarks
		#				Gets the attribute value of the element by the given attribute id
		#
		#	\param		attr			<string>
		#
		#	\return
		#				<string>
		#-------------------------------------------------------------------------------------------------------------
		"""
		out = unicode( self._object.getAttribute( attr ) )
		if ( out ):
			return out
		return fail
	
	def childAt( self, index ):
		"""
		#-------------------------------------------------------------------------------------------------------------
		#	\remarks
		#				Finds the child at the given index, provided the index is within the child range
		#
		#	\param		index		<int>
		#
		#	\return
		#				<XML.XMLElement> || None
		#-------------------------------------------------------------------------------------------------------------
		"""
		childList = self._children()
		if ( 0 <= index and index < len( childList ) ):
			return XMLElement( childList[index], self.__file__ )
		return None
	
	def childNames( self ):
		"""
		#-------------------------------------------------------------------------------------------------------------
		#	\remarks
		#				Collects all the names of the children of this element whose child type is an 
		#				<xml.dom.minidom.Element>
		#
		#	\return
		#				<array> [ <string>, .. ]
		#-------------------------------------------------------------------------------------------------------------
		"""
		if ( self._object ):
			return [ child.nodeName for child in self._object.childNodes if isinstance( child, xml.dom.minidom.Element ) ]
		return []
		
	def children( self ):
		"""
		#-------------------------------------------------------------------------------------------------------------
		#	\remarks
		#				Collects all the child nodes of this element whose child type is an
		#				<xml.dom.minidom.Element>, wrapping each child as an <XML.XMLElement> class
		#
		#	\return
		#				<array> [ <XML.`>, .. ]
		#-------------------------------------------------------------------------------------------------------------
		"""
		if ( self._object ):
			return [ XMLElement( child, self.__file__ ) for child in self._object.childNodes if isinstance( child, xml.dom.minidom.Element ) ]
		return []
		
	def index( self, object ):
		"""
		#-------------------------------------------------------------------------------------------------------------
		#	\remarks
		#				Finds the index of the inputed child object in this instance's XMLElement children, returning
		#				-1 if it cannot be found
		#
		#	\param		object		<XML.XMLElement> || <xml.dom.minidom.Element>
		#
		#	\return
		#				<int>	(-1 for failure)
		#-------------------------------------------------------------------------------------------------------------
		"""
		if ( self._object ):
			if ( isinstance( object, XMLElement ) ):
				if ( object._object in self._object.childNodes ):
					return self._object.childNodes.index( object._object )
			elif ( isinstance( object, xml.dom.minidom.Element ) ):
				if ( object in self._object.childNodes ):
					return self._object.childNodes.index( object )
		return -1
	
	def findChild( self, childName, recursive = False, autoCreate = False ):
		"""
		#-------------------------------------------------------------------------------------------------------------
		#	\remarks
		#				Finds the first instance of the child of this instance whose nodeName is the given child name
		#
		#	\param		childName		<string>
		#
		#	\return
		#				<XML.XMLElement> || None
		#-------------------------------------------------------------------------------------------------------------
		"""
		if ( self._object ):
			childList = self._object.getElementsByTagName( childName )
			if ( childList ):
				if ( not recursive ):
					for child in childList:
						if child.parentNode == self._object:
						 	return XMLElement( child, self.__file__ )
				else:
					return XMLElement( childList[0], self.__file__ )
		
		if ( autoCreate ):
			return self.addNode( childName )
		
		return None
	
	def findChildById( self, key ):
		import re
		key = '_'.join( re.findall( '[a-zA-Z0-9]*', key ) ).lower()
		for child in self.children():
			if ( key == child.getId() or key == '_'.join( re.findall( '[a-zA-Z0-9]*', child.nodeName ) ).lower() ):
				return child
		return None
	
	def findChildren( self, childName, recursive = False ):
		"""
		#-------------------------------------------------------------------------------------------------------------
		#	\remarks
		#				Finds all the children of this instance whose nodeName is the given child name
		#
		#	\param		childName		<string>
		#
		#	\return
		#				<array> [ <XML.XMLElement>, .. ]
		#-------------------------------------------------------------------------------------------------------------
		"""
		if ( self._object ):
			if ( recursive ):
				return [ XMLElement( child, self.__file__ ) for child in self._object.getElementsByTagName( childName ) ]
			else:
				return [ XMLElement( child, self.__file__ ) for child in self._object.childNodes if child.nodeName == childName ]
		return []
	
	def findColor( self, name, fail = None ):
		from PyQt4.QtGui	import QColor
		
		element = self.findChild( name )
		if ( element ):
			return QColor( float( element.attribute( 'red' ) ), float( element.attribute( 'green' ) ), float( element.attribute( 'blue' ) ), float( element.attribute( 'alpha' ) ) )
		elif ( fail ):
			return fail
		else:
			return QColor()
	
	def findFont( self, name, fail = None ):
		from PyQt4.QtGui import QFont
		
		element = self.findChild( name )
		if ( element ):
			font = QFont()
			font.fromString( element.attribute( 'value' ) )
			return font
		elif ( fail ):
			return fail
		else:
			return QFont()
	
	def findProperty( self, propName, fail = '' ):
		child = self.findChild( propName )
		if ( child ):
			return child.value()
		return fail
	
	def findRect( self, name ):
		from PyQt4.QtCore import QRect
		return self._findRect( name, QRect, int )
	
	def findRectF( self, name ):
		from PyQt4.QtCore import QRectF
		return self._findRect( name, QRectF, float )
	
	def getId( self ):
		out = self.attribute( 'id' )
		if ( not out ):
			import re
			out = '_'.join( re.findall( '[a-zA-Z0-9]*', self.attribute( 'name' ) ) ).lower()
		return out
	
	def parent( self ):
		if ( self.parentNode and isinstance( self.parentNode, xml.dom.minidom.Element ) ):
			return XMLElement(self.parentNode, self.__file__)
		return None
	
	def recordProperty( self, name, value ):
		element = self.findChild( name )
		if ( element ):
			element.remove()
			
		element = self.addNode( name )
		element.recordValue( value )
	
	def restoreProperty( self, name, fail = None ):
		element = self.findChild( name )
		if ( element ):
			return element.restoreValue( fail )
		return fail
	
	def remove( self ):
		if ( self._object.parentNode ):
			self._object.parentNode.removeChild( self._object )
		return True
			
	def setAttribute( self, attr, val ):
		"""
		#-------------------------------------------------------------------------------------------------------------
		#	\remarks
		#				Sets the attribute of this instance to the inputed value, automatically converting the value
		#				to a string to avoid errors on the <xml.dom.minidom.Element> object
		#
		#	\param		attr			<string>
		#	\param		val				<variant>
		#
		#	\return
		#				<boolean> success
		#-------------------------------------------------------------------------------------------------------------
		"""
		if ( val != '' and self._object ):
			self._object.setAttribute( attr, unicode( val ).encode( 'utf-8' ) )
			return True
		return False
	
	def setColor( self, name, color ):
		element = self.addNode( name )
		if ( element ):
			element.setAttribute( 'red', 	color.red() )
			element.setAttribute( 'green', 	color.green() )
			element.setAttribute( 'blue', 	color.blue() )
			element.setAttribute( 'alpha',	color.alpha() )
	
	def setProperty( self, propName, val ):
		prop = self.findChild( propName )
		if ( not prop ):
			prop = self.addNode( propName )
		prop.setValue( val )
	
	def setFont( self, name, font ):
		element = self.addNode( name )
		element.setAttribute( 'value', font.toString() )
		return element
	
	def setPoint( self, name, point ):
		element = self.addNode( name )
		element.setAttribute( 'x', point.x() )
		element.setAttribute( 'y', point.y() )
		return element
	
	def setRect( self, name, rect ):
		element = self.addNode( name )
		element.setAttribute( 'x', 		rect.x() )
		element.setAttribute( 'y', 		rect.y() )
		element.setAttribute( 'width', 	rect.width() )
		element.setAttribute( 'height',	rect.height() )
		return element
	
	def setSize( self, name, size ):
		element = self.addNode( name )
		element.setAttribute( 'width', 	size.width() )
		element.setAttribute( 'height', size.height() )
		return element
	
	def setValue( self, val ):
		"""
		#-------------------------------------------------------------------------------------------------------------
		#	\remarks
		#				Sets the text value for this instance.  If it doesn't already have a child who is of
		#				<xml.dom.minidom.Text> type, then it will add one and set the data of it to the inputed value.
		#				The inputed value will automatically be converted to a string value to avoid errors as well.
		#
		#	\param		val				<variant>
		#
		#	\return
		#				<boolean> success
		#-------------------------------------------------------------------------------------------------------------
		"""
		if ( self._object ):
			# find existing text node & update
			for child in self._object.childNodes:
				if ( isinstance( child, xml.dom.minidom.Text ) ):
					child.data = unicode( val ).encode( 'utf-8' )
					return True
			
			# create new text node
			text = self._document().createTextNode( unicode( val ).encode( 'utf-8' ) )
			self._object.appendChild( text )
			return True
		return False
	
	def uri( self ):
		out 	= []
		temp 	= self
		while ( temp ):
			name = temp.getId()
			if ( not name ):
				name = temp.nodeName
			out.insert(0,name)
			temp = temp.parent()
		
		return '::'.join( out )
		
	def value( self ):
		"""
		#-------------------------------------------------------------------------------------------------------------
		#	\remarks
		#				Returns the string value of the text node of this instance, provided it has a child node of
		#				<xml.dom.minidom.Text> type.  If no text node is found, a blank string is returned.
		#
		#	\return
		#				<string>
		#-------------------------------------------------------------------------------------------------------------
		"""
		if ( self._object ):
			for child in self._object.childNodes:
				if ( isinstance( child, xml.dom.minidom.Text ) ):
					return child.data
		return ''
