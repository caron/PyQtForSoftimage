from PyQt4.QtCore import Qt
from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QLineEdit
from PyQt4.QtGui import QVBoxLayout

class Example( QDialog ):
    def __init__( self, parent ):
        QDialog.__init__( self, parent )
        
        self.setGeometry( 100, 100, 200, 100 )
        self.setWindowTitle( "Hello World" )
        self.setToolTip( "This is a <b>QWidget</b> widget" )
        
        btn = QPushButton( "Log Message", self )
        btn.setToolTip( "This is a <b>QPushButton</b> widget" )
        btn.resize( btn.sizeHint() )
        btn.clicked.connect( self.helloWorld )

        lineedit = QLineEdit( "Hello World", self )
        lineedit.setToolTip( "Type Something" )
        
        layout = QVBoxLayout( self )
        layout.addWidget( lineedit )
        layout.addWidget( btn )
    
    def helloWorld( self ):
        Application.LogMessage( "Hello World" )
        
    
def XSILoadPlugin(reg):
    reg.Name = "PyQt_Example"
    reg.Author = "Steven Caron"
    reg.RegisterCommand( "ExampleDialog" )

def ExampleDialog_Execute():
    import sip

    sianchor = Application.getQtSoftimageAnchor()
    sianchor = sip.wrapinstance( long(sianchor), QWidget )
    dialog = Example( sianchor )
    dialog.show()