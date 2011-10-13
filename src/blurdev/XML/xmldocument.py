##
#	\namespace	blurapi.libs.XML.xmldocument
#
#	\remarks	Defines the way to parse XML library information
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		04/09/10
#

import os
import xml.dom.minidom

from xmlelement import XMLElement

class XMLDocument( XMLElement ):
	""" class to ease the handling of XML documents """
	def __init__( self, object = None ):
		if ( not object ):
			object = xml.dom.minidom.Document()
			
		XMLElement.__init__( self, object )
		
		self.__file__ = ''
	
	def findElementById( self, childId ):
		split 		= child.split( '::' )
		
		outTemplate = None
		if ( split ):
			outTemplate = self.root().findChildById( split[0] )
			index 		= 1
			
			while ( index < len( split ) and outTemplate ):
				outTemplate = outTemplate.findChildById( split[index] )
				index += 1
		return outTemplate
	
	def load( self, fileName ):
		"""
		#-------------------------------------------------------------------------------------------------------------
		#	\remarks
		#				Loads the given xml file by calling xml.dom.minidom.parse, setting this instances object to the
		#				resulting value.
		#
		#	\param		fileName		<string>
		#
		#	\return
		#				<boolean> success
		#-------------------------------------------------------------------------------------------------------------
		"""
		success 	= False
		fileName 	= unicode( fileName )
		if ( os.path.exists( fileName ) ):
			try:
				newObject	 	= xml.dom.minidom.parse( fileName )
			except:
				return False
				
			if ( newObject ):
				self.__file__	= fileName
				self._object 	= newObject
				success			= True
		return success
	
	def parse( self, xmlString ):
		success 	= False
		xmlString 	= unicode( xmlString ).encode( 'utf-8' )
		if ( xmlString ):
			tempObject = xml.dom.minidom.parseString( xmlString )
			if ( tempObject ):
				self._object = tempObject
				success = True
		return success
		
	def root( self ):
		"""
		#-------------------------------------------------------------------------------------------------------------
		#	\remarks
		#				Returns the root xml node for this document
		#
		#	\return
		#				<XML.XMLElement> || None
		#-------------------------------------------------------------------------------------------------------------
		"""
		if ( self._object and self._object.childNodes ):
			return XMLElement( self._object.childNodes[0], self.__file__ )
		return None
	
	def save( self, fileName, pretty = True, showDialog = False ):
		"""
		#-------------------------------------------------------------------------------------------------------------
		#	\remarks
		#				Saves the xml document to the given file, converting it to a pretty XML document if so desired
		#
		#	\param		fileName		<string>
		#	\param		pretty			<boolean>		Pretty will format spaces and line breaks. Default: True
		#	\param		showDialog		<boolean>		If a error occurs while saving, show dialog boxes explaining the problem. Default: False
		#
		#	\return
		#				<boolean> success
		#-------------------------------------------------------------------------------------------------------------
		"""
		if ( os.path.exists( os.path.split( fileName )[0] ) ):
			self.__file__ = fileName
			try:
				if ( pretty ):
					text = self.formatXml( self.toxml() ).encode( 'utf-8' )
				else:
					text = unicode( self.toxml() ).encode( 'utf-8' )
			except:
				print 'Encoding error while saving XML'
				if showDialog:
					from PyQt4.QtGui	import QMessageBox
					QMessageBox.critical( None, 'Encoding Error', 'Unable to save xml data, please check for unsupported characters.' )
				return False
			f = open( fileName, 'w' )
			f.write( text )
			f.close()
			return True
		if showDialog:
			from PyQt4.QtGui	import QMessageBox
			QMessageBox.warning( None, 'Unable to Save', 'Unable to save xml data, please verify you have the correct privileges.' )
		return False
	
	def toxml( self ):
		return self._object.toxml()
	
	@staticmethod
	def formatXml( xmltext, indented = 4 ):
		from PyQt4.QtCore import QString
		from PyQt4.QtXml import QDomDocument
		doc = QDomDocument()
		doc.setContent( QString( xmltext ) )
		return unicode( doc.toString( indented ) )