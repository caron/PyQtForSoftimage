##
#	\namespace	[FILENAME]
#
#	\remarks	[ADD REMARKS]
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		09/27/10
#

from PyQt4.QtWinMigrate import QWinWidget

# have to wrap in a python class or the memory management will not work properly for QWinWidgets
class WinWidget( QWinWidget ):
	cache = []
	
	@staticmethod
	def newInstance( hwnd ):
		import blurdev
		out = WinWidget( hwnd )
		out.showCentered()
		
		palette = blurdev.core.defaultPalette()
		if ( palette ):
			out.setPalette( palette )
		
		import sip
		sip.transferback(out)
		
		WinWidget.cache.append(out)
		
		return out
	
	@staticmethod
	def uncache( widget ):
		if ( widget in WinWidget.cache ):
			WinWidget.cache.remove(widget)