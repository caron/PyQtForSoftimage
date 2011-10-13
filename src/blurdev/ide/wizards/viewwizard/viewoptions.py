##
#	\namespace	python.blurdev.ide.wizards.viewwizard.viewoptions
#
#	\remarks	Defines the Options Wizard page for the ViewWizard wizard system
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		11/11/10
#

from PyQt4.QtGui import QWizardPage

class ViewOptions( QWizardPage ):
	def __init__( self, parent ):
		QWizardPage.__init__( self, parent )
		
		# load the ui
		import blurdev.gui
		blurdev.gui.loadUi( __file__, self )
		
		# register the options field to this widget
		self.registerField( 'options', self )
		
		# create hint helpers
		from blurdev.gui.helpers.hinthelper import HintHelper
		self._packageHelper 	= HintHelper( self.uiPackageTXT, 'trax.gui.views' )
		self._classHelper		= HintHelper( self.uiClassTXT, 	'View' )
		self._iconFile			= ''
		
		import os
		devpath = os.environ.get( 'TRAXDEVPATH' )
		if ( devpath ):
			from PyQt4.QtCore import QDir
			QDir.setCurrent( os.path.join( devpath, 'trax/gui/views' ) )
			
		# create default created option
		from PyQt4.QtCore import QDate
		self.uiCreatedByTXT.setText( 'Blur Studio | %s' % QDate.currentDate().year() )
		
		# create connections
		self.uiGroupTXT.textChanged.connect( 	self.updateHints )
		self.uiNameTXT.textChanged.connect(		self.updateHints )
		self.uiIconBTN.clicked.connect(			self.pickIcon )
	
	def pickIcon( self ):
		from PyQt4.QtGui import QFileDialog
		filename = QFileDialog.getOpenFileName( self, 'Pick Icon File', '', 'PNG Files (*.png);;All Files (*.*)' )
		if ( filename ):
			self._iconFile = filename
			from PyQt4.QtGui import QIcon
			self.uiIconBTN.setIcon( QIcon( filename ) )
	
	def updateHints( self ):
		group 	= self.uiGroupTXT.text()
		name 	= self.uiNameTXT.text()
		
		import re
		module 		= ''.join( re.findall( '[A-Za-z0-9]*', str(group).replace( 'Views', '' ) ) ).lower()
		cls			= ''.join( re.findall( '[A-Za-z0-9]*', str(name) ) )
		
		if ( cls ):
			module += '_' + cls.lower()
		
		if ( module ):
			self._packageHelper.setHint( 'trax.gui.views.' + module )
		else:
			self._packageHelper.setHint( 'trax.gui.views' )
		
		self._classHelper.setText( cls + 'View' )
	
	def validatePage( self ):
		"""
			\remarks	[virtual]	overloaded method from the QWizardPage designed to control whether or not this
									page can be accepted before continuing on with the rest of the wizard
			\return		<bool> success
		"""
		
 		# check to see if the user has entered all required information before continuing
		finished = not( self.uiGroupTXT.text().isEmpty() or self.uiNameTXT.text().isEmpty() )
		if ( not finished ):
			from PyQt4.QtGui import QMessageBox
			QMessageBox.critical( None, 'Missing Required Fields', 'You need to provide at least a group and name for this view.' )
			return False
		
		# define the options dictionary of terms for the wizard files
		options = {}
		
		package = self.uiPackageTXT.text()
		if ( not package ):
			package = self._packageHelper.hint()
			
		cls = str(self.uiClassTXT.text())
		if ( not cls ):
			cls = str(self._classHelper.hint())
		
		# define the option key/value pairings
		options[ 'group' ] 			= self.uiGroupTXT.text()
		options[ 'name' ] 			= self.uiNameTXT.text()
		options[ 'package' ] 		= package
		options[ 'module' ]			= package.split( '.' )[-1]
		options[ 'icon' ]			= self._iconFile
		options[ 'class' ]			= cls
		options[ 'config' ]			= cls.replace( 'View', 'Config' )
		options[ 'created_by' ]		= self.uiCreatedByTXT.text()
		options[ 'desc' ]			= self.uiDescriptionTXT.toPlainText()
		
		# store the wizard options for the wizard and let the system move on
		self.setField( 'options', options )
		
		# define components location (optional if you want to create more complex wizards)
		components = [ 'default' ]
		if ( self.uiCreateUiFileCHK.isChecked() ):
			components.append( 'ui' )
		if ( self.uiHotkeysCHK.isChecked() ):
			components.append( 'hotkeys' )
		if ( self.uiConfigCHK.isChecked() ):
			components.append( 'config' )
		
		self.setField( 'components', '_'.join( components ) )
		
		return True