##
#	\namespace	blurdev.ide.wizards.widgetwizard.widgetoptions
#
#	\remarks	This wizard will create the base code required for generating a reusable Qt widget.
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		11/04/10
#

from PyQt4.QtGui import QWizardPage

class WidgetOptions( QWizardPage ):
	def __init__( self, parent ):
		QWizardPage.__init__( self, parent )
		
		# load the ui
		import blurdev.gui
		blurdev.gui.loadUi( __file__, self )
		
		# register the options field to this widget
		self.registerField( 'options', self )
		
		# define default base class/import module mappings
		self._bases = {}
		self._bases[ 'QWidget' ] 		= 'PyQt4.QtGui'
		self._bases[ 'QFrame' ]			= 'PyQt4.QtGui'
		self._bases[ 'QScrollArea' ]	= 'PyQt4.QtGui'
		self._bases[ 'QGraphicsView' ]	= 'PyQt4.QtGui'
		
		keys = self._bases.keys()
		keys.sort()
		self.uiBaseClassDDL.addItems( keys )
		self.uiBaseClassDDL.setCurrentIndex( keys.index('QWidget') )
		
		self.uiClassNameTXT.textChanged.connect( self.refreshUi )
		self.uiBaseClassDDL.editTextChanged.connect( self.refreshUi )
		self.refreshUi()
	
	def classname( self ):
		return '%s%s' % (self.uiClassNameTXT.text(),str(self.uiBaseClassDDL.currentText()).lstrip( 'Q' ))
	
	def refreshUi( self ):
		classname	= self.classname()
		modulename	= classname.lower()
		
		self.uiClassModuleTXT.setText( 'from %s import %s' % (modulename,classname) )
		
		basemodule 	= self._bases.get( str(self.uiBaseClassDDL.currentText()) )
		self.uiBaseModuleTXT.setEnabled( basemodule == None )
		if ( basemodule ):
			self.uiBaseModuleTXT.setText( basemodule )
	
	def validatePage( self ):
		"""
			\remarks	[virtual]	overloaded method from the QWizardPage designed to control whether or not this
									page can be accepted before continuing on with the rest of the wizard
			\return		<bool> success
		"""
		if ( not self.uiClassNameTXT.text() ):
			from PyQt4.QtGui import QMessageBox
			QMessageBox.critical( None, 'Missing Required Fields', 'You need to at least set the class name for this widget.' )
			return False
		
		# define the options dictionary of terms for the wizard files
		options = {}
		
		options[ 'class' ] 			= self.classname()
		options[ 'module' ] 		= self.classname().lower()
		options[ 'super' ]			= self.uiBaseClassDDL.currentText()
		options[ 'super_module' ]	= self.uiBaseModuleTXT.text()
		options[ 'desc' ]			= self.uiDescriptionTXT.toPlainText()
		
		# determine the components file to use based on the structure
		if ( self.uiPackagedCHK.isChecked() and self.uiCreateUiFileCHK.isChecked() ):
			self.setField( 'components', 'packaged' )
		elif ( self.uiPackagedCHK.isChecked() ):
			self.setField( 'components', 'packaged_no_ui' )
		elif ( self.uiCreateUiFileCHK.isChecked() ):
			self.setField( 'components', 'default' )
		else:
			self.setField( 'components', 'no_ui' )
		
		# store the wizard options for the wizard and let the system move on
		self.setField( 'options', options )
		
		return True