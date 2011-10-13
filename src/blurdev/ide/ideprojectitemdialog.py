##
#	\namespace	[FILENAME]
#
#	\remarks	[ADD REMARKS]
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		11/02/10
#

from blurdev.gui import Dialog

class IdeProjectItemDialog( Dialog ):
	def __init__( self, parent ):
		Dialog.__init__( self, parent )
		
		import blurdev.gui
		blurdev.gui.loadUi( __file__, self )
		
		self._projectItem = None
	
	def accept( self ):
		if ( not self._projectItem ):
			return False
			
		self._projectItem.setText( 0, self.uiNameTXT.text() )
		self._projectItem.setGroup( self.uiGroupCHK.isChecked() )
		self._projectItem.setFileTypes( str( self.uiFileTypesTXT.text() ).split( ';;' ) )
		self._projectItem.setExclude( str( self.uiExcludeTXT.text() ).split( ';;' ) )
		self._projectItem.setFilePath( str( self.uiFilePATH.filePath() ) )
		
		Dialog.accept(self)
		
	def projectItem( self ):
		return self._project
	
	def setProjectItem( self, projectItem ):
		self._projectItem = projectItem
		
		self.uiNameTXT.setText( projectItem.text(0) )
		self.uiGroupCHK.setChecked( projectItem.isGroup() )
		self.uiFileTypesTXT.setText( ';;'.join( projectItem.fileTypes() ) )
		self.uiExcludeTXT.setText( ';;'.join( projectItem.exclude() ) )
		self.uiFilePATH.setFilePath( projectItem._filePath )
		
	@staticmethod
	def edit( projectItem ):
		import blurdev
		dlg = IdeProjectItemDialog(blurdev.core.activeWindow())
		dlg.setProjectItem( projectItem )
		if ( dlg.exec_() ):
			return True
		return False