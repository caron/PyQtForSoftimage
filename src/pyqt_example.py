from PyQt4.QtCore import Qt
from PyQt4.QtCore import pyqtSignal
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QLineEdit
from PyQt4.QtGui import QVBoxLayout

class ExampleDialog( QDialog ):
    def __init__( self, parent ):
        QDialog.__init__( self, parent )
        
        self.setGeometry( 100, 100, 200, 100 )
        self.setWindowTitle( "Hello World" )
        self.setToolTip( "This is a <b>QWidget</b> widget" )
        
        self.btn = QPushButton( "Log Text", self )
        self.btn.setToolTip( "This is a <b>QPushButton</b> widget" )
        self.btn.resize( self.btn.sizeHint() )
        self.btn.clicked.connect( self.logText )

        self.lineedit = QLineEdit( "Hello World", self )
        self.lineedit.setToolTip( "Type Something" )
        
        layout = QVBoxLayout( self )
        layout.addWidget( self.lineedit )
        layout.addWidget( self.btn )
        
    def logText( self ):
        Application.LogMessage( self.lineedit.text() )

class ExampleSignalSlot( ExampleDialog ):
    def __init__( self, parent ):
        ExampleDialog.__init__( self,parent )
        self.setWindowTitle( "Signal/Slot Example" )
        self.lineedit.setText( "" )

        # module containing sievents mapped to pyqtsignals
        from sisignals import signals, muteSIEvent
        
        # connect the siActivate signal to the activate slot
        signals.siActivate.connect( self.activate )
        muteSIEvent( "siActivate", False )
        
        # connect the siPassChange signal to the passChanged slot
        signals.siPassChange.connect( self.passChanged )
        muteSIEvent( "siPassChange", False )

    def activate( self, state = None ):
        if state is not None:
            if state:
                self.lineedit.setText( "Welcome Back!" )
            else:
                self.lineedit.setText( "Good Bye!")
                    
    def passChanged( self, targetPass = "" ):
        self.lineedit.setText( targetPass )
    
    def closeEvent( self, event ):
        # be a good person and mute your events after the dialog closes
        # this isn't a good idea if another pyqt app is running that uses
        # the same events. maybe there is a way to check if other widgets use
        # certain signals?
        from sisignals import muteSIEvent
        muteSIEvent( "siActivate", True )
        muteSIEvent( "siPassChange", True )  
    
def XSILoadPlugin( in_reg ):
    in_reg.Name = "PyQt_Example"
    in_reg.Author = "Steven Caron"
    in_reg.RegisterCommand( "ExampleDialog" )
    in_reg.RegisterCommand( "ExampleSignalSlot")

def ExampleDialog_Execute():
    """a simple example dialog showing basic functionality of the pyqt for softimage plugin"""
    import sip

    sianchor = Application.getQtSoftimageAnchor()
    sianchor = sip.wrapinstance( long(sianchor), QWidget )
    dialog = ExampleDialog( sianchor )
    dialog.show()
    
def ExampleSignalSlot_Execute():
    """a simple example showing softimage events triggering pyqt signals"""
    import sip

    sianchor = Application.getQtSoftimageAnchor()
    sianchor = sip.wrapinstance( long(sianchor), QWidget )
    dialog = ExampleSignalSlot( sianchor )
    dialog.show()