##
#	\namespace	blurdev.gui
#
#	\remarks	Contains gui components and interfaces
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		06/15/10
#

from window import Window
from dialog import Dialog
from wizard import Wizard

def loadUi( filename, widget, uiname = '' ):
	"""
		\remarks	use's Qt's uic loader to load dynamic interafces onto the inputed widget
		\param		filename	<str>
		\param		widget		<QWidget>
	"""
	import PyQt4.uic
	import os.path
	
	# first, inherit the palette of the parent
	if ( widget.parent() ):
		widget.setPalette( widget.parent().palette() )
		
	if ( not uiname ):
		uiname = os.path.basename( filename ).split( '.' )[0]
	
	PyQt4.uic.loadUi( os.path.split( filename )[0] + '/ui/%s.ui' % uiname, widget )

def findPixmap( filename, thumbSize = None ):
	"""
		\remarks	looks up a pixmap based on the inputed filename using the QPixmapCache system.  If the autoLoad
					parameter is true, then it will automatically load the pixmap and return it
		\param		filename	<str>
		\param		thumbSize	<QSize>		size to scale the item to if desired (will affect the search key)
	"""
	from PyQt4.QtCore 	import Qt
	from PyQt4.QtGui 	import QPixmapCache, QPixmap
	
	# create the thumbnail size
	if ( thumbSize ):
		w = thumbSize.width()
		h = thumbSize.height()
		
		ratio 		= '_%sx%s' % (w,h)
		
		thumb = QPixmap()
		
		# load the existing cached thumb file
		if ( not QPixmapCache.find( filename + ratio, thumb ) ):
			cache = QPixmap()
			
			# load the existing cached main file
			if ( not QPixmapCache.find( filename, cache ) ):
				cache.load( filename )
				
				# cache the source
				QPixmapCache.insert( filename, cache )
			
			if ( thumbSize.width() < cache.width() or thumbSize.height() < cache.height() ):
				thumb = cache.scaled( thumbSize, Qt.KeepAspectRatio )
			else:
				thumb = QPixmap( cache )
				
			QPixmapCache.insert( filename + ratio, thumb )
		
		return thumb
	
	else:
		# try to load the pixmap
		cache 	= QPixmap()
		
		# pull the pixmap, autoloading it when necessary
		if ( not QPixmapCache.find( filename, cache ) ):
			cache.load( filename )
						
			# cache the source
			QPixmapCache.insert( filename, cache )
		
		return QPixmap(cache)