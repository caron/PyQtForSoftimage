##
#	\namespace	python.blurdev.ide.wizards.windowwizard.windowoptions
#
#	\remarks	Defines the Options Wizard page for the WindowWizard template system
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		11/05/10
#

from PyQt4.QtGui import QWizardPage

DIALOG_DESC = """<b>Dialog</b>
<hr>
<small>
	Dialogs are usually going to be the base class when creating a floating window.  
	They are good for asking for user input as they can be run modally unilke a Window class,
	but they have no native menu bar support.
</small>
"""

WINDOW_DESC = """<b>Window</b>
<hr>
<small>
	Windows are generally going to be used as a base for a Tool or Application, not as much as popups
	or children of other windows, however it is possible to do so.  Windows cannot be run modally, so
	you will not be able to create a window and wait for a response.
	<br>
	The advantage for a Window over a Dialog is its native menu bar support.  If you want to display options
	to a user inside of a top menu, then you should choose a Window class.
</small>
"""

WIZARD_DESC = """<b>Wizard</b>
<hr>
<small>
	Wizards are used when you want to step a user through a process.  They break up information into manegable chunks
	for a user to easily be guided through the application.  The advantage of a Wizard over a Dialog is when you need to change
	the information displayed on one page based on the choices a user makes in pages before it.
	<br>
	For wizards, the bulk of the logic will actually live within sub-widgets called WizardPage's, the Wizard itself is really just
	a container.
</small>
"""

DESC_MAP = {
	'Dialog': DIALOG_DESC,
	'Window': WINDOW_DESC,
	'Wizard': WIZARD_DESC
}

class WindowOptions( QWizardPage ):
	def __init__( self, parent ):
		QWizardPage.__init__( self, parent )
		
		# load the ui
		import blurdev.gui
		blurdev.gui.loadUi( __file__, self )
		
		# register the options field to this widget
		self.registerField( 'options', self )
		
		# load the ui
		keys = DESC_MAP.keys()
		keys.sort()
		self.uiBaseClassDDL.addItems( keys )
		
		self.uiClassNameTXT.textChanged.connect( self.refreshUi )
		self.uiBaseClassDDL.currentIndexChanged.connect( self.refreshUi )
		
		self.refreshUi()
	
	def classname( self ):
		return '%s%s' % (self.uiClassNameTXT.text(),str(self.uiBaseClassDDL.currentText()))
	
	def refreshUi( self ):
		classname	= self.classname()
		modulename	= classname.lower()
		
		self.uiBaseClassDDL.setToolTip( DESC_MAP[ str(self.uiBaseClassDDL.currentText()) ] )
		self.uiClassModuleTXT.setText( 'from %s import %s' % (modulename,classname) )
		
		if ( self.uiBaseClassDDL.currentText() == 'Wizard' ):
			self.uiCreateUiFileCHK.setChecked( False )
			self.uiCreateUiFileCHK.setEnabled( False )
		else:
			self.uiCreateUiFileCHK.setEnabled( True )
	
	def validatePage( self ):
		"""
			\remarks	[virtual]	overloaded method from the QWizardPage designed to control whether or not this
									page can be accepted before continuing on with the rest of the wizard
			\return		<bool> success
		"""
		
 		# check to see if the user has entered all required information before continuing
		if ( not self.uiClassNameTXT.text() ):
			from PyQt4.QtGui import QMessageBox
			QMessageBox.critical( None, 'Missing Required Fields', 'You need to at least set the class name for this widget.' )
			return False
		
		
		# define the options dictionary of terms for the template files
		options = {}
		
		# define the option key/value pairings
		
		options[ 'class' ] 			= self.classname()
		options[ 'module' ] 		= self.classname().lower()
		options[ 'super' ]			= self.uiBaseClassDDL.currentText()
		options[ 'desc' ]			= self.uiDescriptionTXT.toPlainText()
		
		# determine the components file to use based on the structure
		compnames = []
		if ( self.uiPackagedCHK.isChecked() ):
			compnames.append( 'packaged' )
		if ( self.uiCreateUiFileCHK.isChecked() ):
			compnames.append( 'ui' )
		if ( self.uiRecordSettingsCHK.isChecked() ):
			compnames.append( 'settings' )
		
		if ( not compnames ):
			self.setField( 'components', 'default' )
		else:
			self.setField( 'components', 'default_%s' % '_'.join( compnames ) )
		
		# store the template options for the wizard and let the system move on
		self.setField( 'options', options )
		
		return True