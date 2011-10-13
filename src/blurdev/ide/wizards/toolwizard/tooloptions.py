##
#	\namespace	blurdev.ide.wizards.toolwizard.tooloptions
#
#	\remarks	The Tool system allows a developer to create an application and register it for users via the Treegrunt system.
#
#This will work in conjunction with the Tools Environment framework by registering the code to the Environment's index.
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		11/04/10
#

from PyQt4.QtGui import QWizardPage

class MaxscriptToolOptions( QWizardPage ):
	def __init__( self, parent ):
		QWizardPage.__init__( self, parent )
		
		# load the ui
		import blurdev.gui
		blurdev.gui.loadUi( __file__, self, 'maxscripttooloptions' )
		
		# \todo 	finish loading maxscript properties
	
	
	def validatePage( self ):
		"""
			\remarks	[virtual]	overloaded method from the QWizardPage designed to control whether or not this
									page can be accepted before continuing on with the rest of the wizard
			\return		<bool> success
		"""
		
		# \todo		check to see if the user has entered all required information before continuing
		# if ( not finished ):
		#	return False
		
		# define the options dictionary of terms for the wizard files
		options = {}
		
		# \todo		define the option key/value pairings
		
		# store the wizard options for the wizard and let the system move on
		self.setField( 'options', options )
		self.setField( 'components', 'maxscript' )
		return True
		
class PythonToolOptions( QWizardPage ):
	def __init__( self, parent ):
		QWizardPage.__init__( self, parent )
		
		# load the ui
		import blurdev.gui
		blurdev.gui.loadUi( __file__, self, 'pythontooloptions' )
		
		# register the fields
		self.registerField( 'options', self )
		
		# create a regular expression validator
		from PyQt4.QtCore import QRegExp
		from PyQt4.QtGui import QRegExpValidator
		self.uiNameTXT.setValidator( QRegExpValidator( QRegExp( '[A-Z][A-Za-z0-9]+' ), self.uiNameTXT ) )
		
		# load the drop down options
		self.uiSuperDDL.addItems( [ 'Dialog', 'Window', 'Wizard' ] )	# these are the allowable root classes for a Python tool
		
		# load the tool type options
		from blurdev import tools
		from PyQt4.QtCore import Qt
		from PyQt4.QtGui import QTreeWidgetItem
		for ttype in tools.ToolType.values():
			label = tools.ToolType.labelByValue(ttype)
			if ( label != 'All Tools' ):
				item = QTreeWidgetItem( [ label ] )
				item.setData( 0, Qt.UserRole, ttype )
				item.setCheckState( 0, Qt.Unchecked )
				self.uiToolTypeTREE.addTopLevelItem( item )
	
		self._iconFile = ''
		self.uiIconBTN.clicked.connect( self.pickIcon )
	
	def pickIcon( self ):
		from PyQt4.QtGui import QFileDialog
		filename = QFileDialog.getOpenFileName( self, 'Select Tool Icon' )
		if ( filename ):
			from PyQt4.QtGui import QIcon
			self._iconFile = str(filename)
			self.uiIconBTN.setIcon( QIcon(self._iconFile) )
		
	def validatePage( self ):
		"""
			\remarks	[virtual]	overloaded method from the QWizardPage designed to control whether or not this
									page can be accepted before continuing on with the rest of the wizard
			\return		<bool> success
		"""
		# determine the tool type string
		from PyQt4.QtCore import Qt
		value = 0
		for i in range( self.uiToolTypeTREE.topLevelItemCount() ):
			item = self.uiToolTypeTREE.topLevelItem(i)
			if ( item.checkState(0) == Qt.Checked ):
				value |= item.data( 0, Qt.UserRole ).toInt()[0]
		
		# make sure we at least have a name and some text
		if ( not (self.uiNameTXT.text() and value) ):
			from PyQt4.QtGui import QMessageBox
			QMessageBox.critical( None, 'Missing Required Fields', 'You need to supply at least a valid name and a tool type for your tool.' )
			return False
		
		# define the options dictionary of terms for the wizard files
		from blurdev import tools
		
		options = {}
		
		supercls = str(self.uiSuperDDL.currentText())
		options[ 'super' ] 		= supercls
		options[ 'name' ] 		= self.uiNameTXT.text()
		options[ 'desc' ] 		= self.uiDescriptionTXT.toPlainText()
		options[ 'icon' ]		= self._iconFile
		options[ 'toolTypes' ] 	= tools.ToolType.toString( value )
		
		# create the classname
		cls = '%s%s' % (self.uiNameTXT.text(),supercls)
		options[ 'class' ] 		= cls
		options[ 'module' ]		= cls.lower()
		
		# determine the components based on if we have a ui file or not
		if ( self.uiSimpleCHK.isChecked() ):
			self.setField( 'components', 'python_simple' )
			
		elif ( supercls == 'Wizard' ):
			self.setField( 'components', 'python_noui' )
			options[ 'source' ] = 'wizard'
			
		elif ( self.uiUiFileCHK.isChecked() ):
			self.setField( 'components', 'python' )
			options[ 'source' ] 	= 'tool'
			options[ 'ui_logic' ] 	= """# load the ui
		import blurdev
		blurdev.gui.loadUi( __file__, self )"""
		
		else:
			self.setField( 'components', 'python_noui' )
			options[ 'source' ] 	= 'tool'
			options[ 'ui_logic' ] 	= "# \todo	define your ui controls"
		
		# store the wizard options for the wizard and let the system move on
		self.setField( 'options', options )
		
		return True