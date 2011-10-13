##
#	\namespace	blurdev.enum
#
#	\remarks	Python based enumartion class, create and parse binary classes
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		08/06/08
#

import re
from sys import maxint

class enum:
	INDICES = xrange( maxint ) # indices constant to use for looping
	
	def __call__( self, key ):
		return self.value( key )
	
	def __getattr__( self, key ):
		if ( key == 'All' ):
			out = 0
			for k in self._keys:
				out |= self.__dict__[k]
			return out
		elif ( key == '__name__' ):
			return 'enum'
		else:
			raise AttributeError, key
	
	def __init__( self, *args, **kwds ):
		self._keys 		= list(args) + kwds.keys()
		self._compound 	= kwds.keys()
		self._descr 	= {}
		key = 1
		for i in range( len(args) ):
			self.__dict__[ args[i] ] = key
			key *= 2
		
		for kwd, value in kwds.items():
			self.__dict__[ kwd ] = value
	
	def count( self ):
		return len( self._keys )
	
	def description( self, value ):
		return self._descr.get( value, '' )
	
	def matches( self, a, b ):
		return ( a & b != 0 )
	
	def hasKey( self, key ):
		return key in self._keys
	
	def labels( self ):
		import re
		return [ ' '.join( re.findall( '[A-Z]+[^A-Z]*', key ) ) for key in self.keys() ]
	
	def labelByValue( self, value ):
		import re
		return ' '.join( re.findall( '[A-Z]+[^A-Z]*', self.keyByValue(value) ) )
	
	def isValid( self, value ):
		return self.keyByValue(value) != ''
	
	def keyByIndex( self, index ):
		if ( index in range( self.count() ) ):
			return self._keys[ index ]
		return ''
	
	def keyByValue( self, value ):
		for key in self._keys:
			if ( self.__dict__[ key ] == value ):
				return key
		return ''
	
	def keys( self ):
		return self._keys
	
	def value( self, key, caseSensitive = True ):
		if ( caseSensitive ):
			return self.__dict__.get( str(key), 0 )
		else:
			key = str(key).lower()
			for k in self.__dict__.keys():
				if ( k.lower() == key ):
					return self.__dict__[k]
			return 0
	
	def values( self ):
		return [ self.__dict__[ key ] for key in self.keys() ]
	
	def valueByLabel( self, label, caseSensitive = True ):
		return self.value( ''.join( str( label ).split( ' ' ) ), caseSensitive = caseSensitive )
	
	def valueByIndex( self, index ):
		return self.value( self.keyByIndex( index ) )
	
	def index( self, key ):
		if ( key in self._keys ):
			return self._keys.index(key)
		return -1
	
	def indexByValue( self, value ):
		for index in range( len( self._keys ) ):
			if ( self.__dict__[ self._keys[index] ] == value ):
				return index
		return -1
	
	def toString( self, value, default = 'None' ):
		parts = []
		for key in self._keys:
			if ( not key in self._compound and value & self.value(key) ):
				parts.append( key )
		
		if ( parts ):
			return ' '.join( parts )
		return default
	
	def fromString( self, labels ):
		parts = str( labels ).split( ' ' )
		
		value = 0
		for part in parts:
			value |= self.value( part )
		
		return value
	
	def setDescription( self, value, descr ):
		self._descr[ value ] = descr
	
	matches = classmethod(matches)