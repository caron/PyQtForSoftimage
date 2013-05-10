import os
import sys
# Add this plug-in path to python path
if __sipath__ not in sys.path:
    sys.path.append( __sipath__ )

import Qt
Qt.initialize()

from Qt.QtGui import QDialog
from Qt.QtGui import QWidget
from Qt.QtGui import QPushButton
from Qt.QtGui import QLineEdit
from Qt.QtGui import QVBoxLayout
from Qt.QtGui import QMenu
from Qt.QtGui import QCursor

from Qt import loadUi

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
        ExampleDialog.__init__( self, parent )
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
        # disconnect signals from slots when you close the widget
        # muteSIEvent() can be used to mute the signals softimage events send
        # but be careful if another widget exists and is using them
        from sisignals import signals, muteSIEvent
        signals.siActivate.disconnect( self.activate )
        signals.siPassChange.disconnect( self.passChanged )  
        #muteSIEvent( "siActivate", True )
        #muteSIEvent( "siPassChange", True )

class ExampleMenu( QMenu ):
    def __init__( self, parent ):
        QMenu.__init__( self, parent )
        
        # add actions and a separator
        hello = self.addAction("Print 'Hello!'")
        self.addSeparator()	
        world = self.addAction("Print 'World!'")
        
        # connect to the individual action's signal
        hello.triggered.connect( self.hello )
        world.triggered.connect( self.world )
        
        # connect to the menu level signal
        self.triggered.connect( self.menuTrigger )
        
    def hello( self ):
        Application.LogMessage( "Hello!" )
    
    def world( self ):
        Application.LogMessage( "World!" )
    
    def menuTrigger( self, action ):
        if action.text() == "Print 'Hello!'":
            Application.LogMessage( "You clicked, Print 'Hello!'" )
        elif action.text() == "Print 'World!'":
            Application.LogMessage( "You clicked, Print 'World!'" )

class ExampleUIFile( QDialog ):
    def __init__( self, parent, uifilepath ):
        QDialog.__init__( self, parent )
        
        # load ui file
        self.ui = Qt.loadUi( uifilepath, self )
        
        # connect to the createCube function
        self.ui.uiCreateCube.clicked.connect( self.createCube )
        
    def createCube( self ):
        cube = Application.CreatePrim("Cube", "MeshSurface", self.ui.uiCubeName.text(), "")
        cube.Length.Value = self.ui.uiCubeLength.value()
 
def XSILoadPlugin( in_reg ):
    in_reg.Name = "PyQt_Example"
    in_reg.Author = "Steven Caron"
    in_reg.RegisterCommand( "ExampleDialog" )
    in_reg.RegisterCommand( "ExampleSignalSlot" )
    in_reg.RegisterCommand( "ExampleMenu" )
    in_reg.RegisterCommand( "ExampleUIFile" )

def ExampleDialog_Execute():
    """a simple example dialog showing basic functionality of the pyqt for softimage plugin"""
    sianchor = Application.getQtSoftimageAnchor()
    sianchor = Qt.wrapinstance( long(sianchor), QWidget )
    dialog = ExampleDialog( sianchor )
    dialog.show()
    
def ExampleSignalSlot_Execute():
    """a simple example showing softimage events triggering pyqt signals"""
    sianchor = Application.getQtSoftimageAnchor()
    sianchor = Qt.wrapinstance( long(sianchor), QWidget )
    dialog = ExampleSignalSlot( sianchor )
    dialog.show()

def ExampleMenu_Execute():
    """a simple example showing the use of a qmenu""" 
    sianchor = Application.getQtSoftimageAnchor()
    sianchor = Qt.wrapinstance( long(sianchor), QWidget )
    menu = ExampleMenu( sianchor )
    
    # notice the use of QCursor and exec_ call
    menu.exec_(QCursor.pos())

def ExampleUIFile_Execute():
    """a simple example showing the use of a .ui file created using QtDesigner"""
    
    # find plugin to get the path to the example ui file
    plugin = Application.Plugins("PyQt_Example")
    if plugin is None:
        return False
        
    sianchor = Application.getQtSoftimageAnchor()
    sianchor = Qt.wrapinstance( long(sianchor), QWidget )
    uifilepath = os.path.join(plugin.OriginPath, "exampleui.ui")
    dialog = ExampleUIFile( sianchor, uifilepath )
    dialog.show()
