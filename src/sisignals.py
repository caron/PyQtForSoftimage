if 'PyQt4' in sys.modules:
    USE_PYSIDE = False
elif 'PySide' in sys.modules:
    USE_PYSIDE = True
else:
    try:
        import PyQt4
        USE_PYSIDE = False
    except ImportError:
        try:
            import PySide
            USE_PYSIDE = True
        except ImportError:
            raise Exception("PyQtForSoftimage requires either PyQt4 or PySide; neither package could be imported.")

if USE_PYSIDE:
    from PySide.QtCore import QObject
    from PySide.QtCore import Signal
except:
    from PyQt4.QtCore import QObject
    from PyQt4.QtCore import pyqtSignal as Signal

from win32com.client import Dispatch as disp
from win32com.client import constants as C
si = disp('XSI.Application')

EVENT_MAPPING = {
    #pyqtsignal : softimage event
    "siActivate" : "QtEvents_Activate",
    "siFileExport" : "QtEvents_FileExport",
    "siFileImport" : "QtEvents_FileImport",
    "siCustomFileExport" : "QtEvents_CustomFileExport",
    "siCustomFileImport" : "QtEvents_CustomFileImport",

    "siRenderFrame" : "QtEvents_RenderFrame",
    "siRenderSequence" : "QtEvents_RenderSequence",
    "siRenderAbort" : "QtEvents_RenderAbort",
    "siPassChange" : "QtEvents_PassChange",

    "siSceneOpen" : "QtEvents_SceneOpen",
    "siSceneSaveAs" : "QtEvents_SceneSaveAs",
    "siSceneSave" : "QtEvents_SceneSave",
    "siChangeProject" : "QtEvents_ChangeProject",

    "siConnectShader" : "QtEvents_ConnectShader",
    "siDisconnectShader" : "QtEvents_DisconnectShader",
    "siCreateShader" : "QtEvents_CreateShader",

    "siDragAndDrop" : "QtEvents_DragAndDrop",

    "siObjectAdded" : "QtEvents_ObjectAdded",
    "siObjectRemoved" : "QtEvents_ObjectRemoved",

    "siSelectionChange" : "QtEvents_SelectionChange",

    "siSourcePathChange" : "QtEvents_SourcePathChange",

    "siValueChange" : "QtEvents_ValueChange",
}

class SISignals( QObject ):
    """
    class for mapping softimage events to pyqt signals
    not all context attributes are passed as signal arguments, add more as needed
    currently all signals are expected to be 'siOnEnd' versions of softimage events
    """

    # add more Signals that map to softimage events here
    siActivate = Signal(bool) # siOnActivate

    siFileExport = Signal(str) # siOnEndFileExport
    siFileImport = Signal(str) # siOnEndFileImport
    siCustomFileExport = Signal(str) # siOnCustomFileExport
    siCustomFileImport = Signal(str) # siOnCustomFileImport

    siRenderFrame = Signal(str,int) # siOnEndFrame
    siRenderSequence = Signal(str,int) # siOnEndSequence
    siRenderAbort = Signal(str,int) # siOnRenderAbort
    siPassChange = Signal(str) # siOnEndPassChange

    siSceneOpen = Signal(str) # siOnEndSceneOpen
    siSceneSaveAs = Signal(str) # siOnEndSceneSaveAs
    siSceneSave = Signal(str) # siOnEndSceneSave2
    siChangeProject = Signal(str) # siOnChangeProject

    siConnectShader = Signal(str,str) # siOnConnectShader
    siDisconnectShader = Signal(str,str) # siOnDisconnectShader
    siCreateShader = Signal(str,str) # siOnCreateShader

    siDragAndDrop = Signal(str) # siOnDragAndDrop

    siObjectAdded = Signal(list) # siOnObjectAdded
    siObjectRemoved = Signal(list) # siOnObjectRemoved

    siSelectionChange = Signal(int) # siOnSelectionChange

    siSourcePathChange = Signal(str) # siOnSourcePathChange

    siValueChange = Signal(str) # siOnValueChange

    def __init__(self):
        QObject.__init__(self)
        self.setObjectName( "siSignals" )

signals = SISignals()

def muteSIEvent( event, state = True ):
    events = si.EventInfos
    event = events( EVENT_MAPPING[event] )
    if si.ClassName( event ) == "EventInfo":
        event.Mute = state
