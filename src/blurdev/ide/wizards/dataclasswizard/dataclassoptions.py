##
#	\namespace	python.blurdev.ide.wizards.dataclasswizard.dataclassoptions
#
#	\remarks	Defines the Options Wizard page for the DataClassWizard wizard system
#	
#	\author		beta@blur.com
#	\author		Blur Studio
#	\date		01/25/11
#

from PyQt4.QtGui import QWizardPage

class DataClassOptions( QWizardPage ):
	def __init__( self, parent ):
		QWizardPage.__init__( self, parent )
		
		# load the ui
		import blurdev.gui
		blurdev.gui.loadUi( __file__, self )
		
		# register the options field to this widget
		self.registerField( 'options', self )
		
		self.uiClassTypeDDL.currentIndexChanged.connect( 	self.refresh )
		self.uiComponentTXT.textChanged.connect( 			self.refresh )
		self.uiEventTXT.textChanged.connect( 				self.refresh )
		self.uiBaseTXT.textChanged.connect( 				self.refresh )
		self.refresh()
	
	def refresh( self ):
		iscustom 		= self.uiClassTypeDDL.currentText() == 'Custom'
		isnotification 	= self.uiClassTypeDDL.currentText() == 'Notification'
		
		self.uiClassTXT.setEnabled( iscustom )
		self.uiBaseTXT.setVisible( not isnotification )
		self.uiBaseLBL.setVisible( not isnotification )
		self.uiComponentTXT.setVisible( isnotification )
		self.uiComponentLBL.setVisible( isnotification )
		self.uiEventTXT.setVisible( isnotification )
		self.uiEventLBL.setVisible( isnotification )
		
		if ( isnotification ):
			import re
			clsname = ''.join( re.findall( '[a-zA-Z0-9]*', str(self.uiComponentTXT.text()) ) ) + ''.join( re.findall( '[a-zA-Z0-9]*', str(self.uiEventTXT.text()) ) )
			self.uiBaseTXT.setText( 'NotificationEventDef' )
			self.uiClassTXT.setText( clsname + 'Event' )
		else:
			self.uiClassTXT.setText( self.uiBaseTXT.text() + self.uiClassTypeDDL.currentText() )
	
	def validatePage( self ):
		"""
			\remarks	[virtual]	overloaded method from the QWizardPage designed to control whether or not this
									page can be accepted before continuing on with the rest of the wizard
			\return		<bool> success
		"""
		
 		# check to see if the user has entered all required information before continuing
		if ( not (self.uiBaseTXT.text() and self.uiClassTXT.text()) ):
			from PyQt4.QtGui import QMessageBox
			QMessageBox.critical( None, 'Missing Required Fields', 'Not all the required fields have been met.' )
			return False
		
		# define the options dictionary of terms for the template files
		options = {}
		
		# define the option key/value pairings
		import re
		options[ 'baseclass' ]	= ''.join( re.findall( '[a-zA-Z0-9]*', str(self.uiBaseTXT.text()) ) )
		options[ 'classname' ] 	= ''.join( re.findall( '[a-zA-Z0-9]*', str(self.uiClassTXT.text()) ) )
		options[ 'component' ] 	= self.uiComponentTXT.text()
		options[ 'event' ]		= self.uiEventTXT.text()
		options[ 'desc' ]		= unicode( self.uiDescriptionTXT.toPlainText() )
		
		if ( self.uiClassTypeDDL.currentText() == 'Notification' ):
			self.setField( 'components', 'notification' )
			
		if ( self.uiClassTypeDDL.currentText() in ('Custom','Notification') ):
			options[ 'module' ] 	= options[ 'classname' ].lower()
			options[ 'register' ] 	= options[ 'classname' ]
		else:
			options[ 'module' ] 	= options[ 'baseclass' ].lower()
			options[ 'register' ] 	= options[ 'baseclass' ].lower()
		
		# store the template options for the wizard and let the system move on
		self.setField( 'options', options )
		
		return True