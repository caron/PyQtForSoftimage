##
#	\namespace	blurdev.models.objecttreemodel
#
#	\remarks	Creates a QAbstractItemModel for QObject tree hierarchies
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		11/01/10
#

from PyQt4.QtCore import Qt, QAbstractItemModel

class ObjectTreeModel( QAbstractItemModel ):
	def __init__( self, object ):
		QAbstractItemModel.__init__( self )
		
		# store the root object
		self._rootObject = object
	
	def childrenOf( self, parent ):
		"""
			\remarks	returns a list of the children for the inputed object, by default will return the QObject's children
			\param		parent	<QObject>
			\return		<list> [ <QObject>, .. ]
		"""
		return parent.children()
	
	def columnCount( self, index ):
		"""
			\remarks	returns the number of columns the inputed model has
			\param		index	<QModelIndex>
			\return		<int>
		"""
		return 1
	
	def data( self, index, role ):
		"""
			\remarks	returns a variant containing the information for the inputed index and the given role
			\param		index	<QModelIndex>
			\param		role	<Qt::Role>
			\return		<QVariant>
		"""
		from PyQt4.QtCore import QVariant
		
		if ( not index.isValid() ):
			return QVariant()
		
		# return the name of the object
		if ( role == Qt.DisplayRole ):
			return index.internalPointer().objectName()
		
		# for all else, return a blank variant
		else:
			return QVariant()
	
	def object( self, index ):
		"""
			\remarks	returns the object that the index contains
			\param		index	<QModelIndex>
			\return		<QObject>
		"""
		if ( index and index.isValid() ):
			return index.internalPointer()
		return None
	
	def indexOf( self, object, column = 0 ):
		"""
			\remarks	returns a model index representing the inputed object at the given column
			\param		object		<QObject>
			\param		column		<int>
			\return		<QModelIndex>
		"""
		return self.createIndex( self.rowForObject(object), column, object )
	
	def findObjectAtRow( self, parent, row ):
		"""
			\remarks	returns the child object of the inputed parent at the given row
			\param		parent		<QObject>
			\param		column		<int>
			\return		<QModelIndex>
		"""
		return self.childrenOf(parent)[row]
	
	def flags( self, index ):
		"""
			\remarks	returns the item flags for the inputed index
			\param		index		<QModelIndex>
			\return		<QModelIndex>
		"""
		if ( not index.isValid() ):
			return Qt.NoItemFlags
		
		return Qt.ItemIsEnabled | Qt.ItemIsUserCheckable | Qt.ItemIsSelectable
	
	def headerData( self, section, orientation, role = Qt.DisplayRole ):
		from PyQt4.QtCore import QVariant
		if ( orientation == Qt.Horizontal and role == Qt.DisplayRole ):
			return self._rootObject.objectName()
		return QVariant()
	
	def index( self, row, column, parent ):
		
		from PyQt4.QtCore import QModelIndex
		
		if ( not parent ):
			parent = QModelIndex()
		
		if ( not self.hasIndex( row, column, parent ) ):
			return QModelIndex()
		
		# collect children for the root
		if ( not parent.isValid() ):
			root = self._rootObject
		else:
			root = parent.internalPointer()
		
		child = self.findObjectAtRow( root, row )
		if ( child ):
			return self.createIndex( row, column, child )
		return QModelIndex()
	
	def parent( self, index ):
		from PyQt4.QtCore import QModelIndex
		if ( not index.isValid() ):
			return QModelIndex()
		
		object = index.internalPointer()
		try:
			parent = object.parent()
		except:
			parent = None
		
		if ( parent and parent != self._rootObject ):
			return self.createIndex( self.rowForObject( parent ), 0, parent )
		
		return QModelIndex()
	
	def rootObject( self ):
		return self._rootObject
	
	def rowCount( self, parent ):
		from PyQt4.QtCore import QModelIndex
		if ( not parent ):
			parent = QModelIndex()
		
		if ( 0 < parent.column() ):
			return 0
		
		if ( not parent.isValid() ):
			return len(self.childrenOf(self._rootObject))
		else:
			return len(self.childrenOf(parent.internalPointer()))
	
	def rowForObject( self, object ):
		parent = object.parent()
		if ( not parent ):
			return 0
		
		children = self.childrenOf(parent)
		if ( object in children ):
			return children.index(object)
		return 0