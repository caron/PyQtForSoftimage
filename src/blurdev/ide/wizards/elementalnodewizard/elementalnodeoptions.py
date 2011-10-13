##
#	\namespace	blurdev.ide.wizards.elementalnodewizard.elementalnodeoptions
#
#	\remarks	Defines the Options Wizard page for the ElementalNodeWizard wizard system
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		11/09/10
#

from PyQt4.QtGui import QWizardPage

class ElementalNodeOptions( QWizardPage ):
	def __init__( self, parent ):
		QWizardPage.__init__( self, parent )
		
		# load the ui
		import blurdev.gui
		blurdev.gui.loadUi( __file__, self )
		
		# register the options field to this widget
		self.registerField( 'options', self )
		
		self._iconFile = ''
		self.uiIconBTN.clicked.connect( self.pickIcon )
	
	def pickIcon( self ):
		from PyQt4.QtGui import QFileDialog
		icon = QFileDialog.getOpenFileName( None, 'Select Icon File', '', 'PNG Files (*.png);;All Files (*.*)' )
		if ( icon ):
			self._iconFile = icon
			from PyQt4.QtGui import QIcon
			self.uiIconBTN.setIcon( QIcon( icon ) )
	
	def validatePage( self ):
		"""
			\remarks	[virtual]	overloaded method from the QWizardPage designed to control whether or not this
									page can be accepted before continuing on with the rest of the wizard
			\return		<bool> success
		"""
		
 		# check to see if the user has entered all required information before continuing
		finished = not (self.uiGroupTXT.text().isEmpty() or self.uiNameTXT.text().isEmpty())
		if ( not finished ):
			from PyQt4.QtGui import QMessageBox
			QMessageBox.critical( None, 'Missing Required Fields', 'You need to provide at least a group and name for your node.' )
			return False
		
		# define the options dictionary of terms for the template files
		options = {}
		
		import re
		classname 	= '%sNode' % (''.join(re.findall( '[A-Za-z0-9]*', str( self.uiNameTXT.text() ) )))
		package		= ''.join(re.findall( '[A-Za-z0-9]*', str( self.uiGroupTXT.text() ) )).lower()
		
		# define the option key/value pairings
		options[ 'group_package' ]	= package
		options[ 'group' ] 			= self.uiGroupTXT.text()
		options[ 'name' ] 			= self.uiNameTXT.text()
		options[ 'class' ] 			= classname
		options[ 'module' ] 		= classname.lower()
		options[ 'desc' ]			= self.uiDescriptionTXT.toPlainText()
		options[ 'icon' ] 			= self._iconFile
		
		# store the template options for the wizard and let the system move on
		self.setField( 'options', options )
		
		# determine the proper components definition
		if ( self.uiPackagedCHK.isChecked() and self.uiCreateUiFileCHK.isChecked() ):
			self.setField( 'components', 'default_packaged_ui' )
		elif ( self.uiPackagedCHK.isChecked() ):
			self.setField( 'components', 'default_packaged' )
		elif ( self.uiCreateUiFileCHK.isChecked() ):
			self.setField( 'components', 'default_ui' )
		else:
			self.setField( 'components', 'default' )
		
		return True