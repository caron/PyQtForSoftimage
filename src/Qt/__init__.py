# -*- coding: utf-8 -*-

# Copyright (c) 2009-2011 Christopher S. Case and David H. Bronke
# Licensed under the MIT license; see the LICENSE file for details.

# Modified by Steven Caron for PyQtForSoftimage

"""Qt compatibility wrapper

Detects either PySide or PyQt.

"""
import sys
import __builtin__

from win32com.client import Dispatch as disp
from win32com.client import constants as C
si = disp("XSI.Application")

__all__ = [
        'QtCore', 'QtGui', 'QtNetwork', 'QtWebKit', 'QtUiTools', 'Signal',
        'Slot', 'loadUi', 'wrapinstance'
        ]

QtCore = None
QtGui = None
QtNetwork = None
QtWebKit = None
QtUiTools = None
Signal = None
Slot = None
loadUi = None

binding = ""


# Internal: UI loader instance for PySide
_uiLoader = None

QT_BINDING_MODULES = {}


def _register_binding_module(module_name, module):
    # register module using only its own name (TODO: legacy compatibility, remove when possible)
    sys.modules[module_name] = module
    # add module to the binding modules
    QT_BINDING_MODULES[module_name] = module

def _named_import(name):
    parts = name.split('.')
    assert(len(parts) >= 2)
    module = __builtin__.__import__(name)
    for m in parts[1:]:
        module = module.__dict__[m]
    module_name = parts[-1]
    _register_binding_module(module_name, module)

def initialize(prefer=None, args=[]):
    if prefer is not None:
        prefer = prefer.lower()

    remainingArgs = list()
    for arg in args:
        if arg in ["--use-pyqt", "--use-pyqt4"]:
            prefer = "pyqt"
        elif arg == "--use-pyside":
            prefer = "pyside"
        else:
            remainingArgs.append(arg)

    if prefer in ["pyqt", "pyqt4"]:
        if not importPyQt():
            if prefer is not None:
                #logger.warn("PyQt4 requested, but not installed.")
                si.LogMessage("PyQt4 requested, but not installed.", C.siWarning)

            if not importPySide():
                #logger.error("Couldn't import PySide or PyQt4! You must have "
                #        + "one or the other to run this app.")
                si.LogMessage("Couldn't import PySide or PyQt4! You must have "
                    + "one or the other to run this app.", C.siError)
                sys.exit(1)
    else:
        if not importPySide():
            if prefer is not None:
                #logger.warn("PySide requested, but not installed.")
                si.LogMessage("PySide requested, but not installed.", C.siWarning)

            if not importPyQt():
                # logger.error("Couldn't import PySide or PyQt4! You must have "
                #         + "one or the other to run this app.")
                si.LogMessage("Couldn't import PySide or PyQt4! You must have "
                    + "one or the other to run this app.", C.siError)
                sys.exit(1)

    for module_name, module in QT_BINDING_MODULES.items():
        sys.modules[__name__ + '.' + module_name] = module
        setattr(sys.modules[__name__], module_name, module)

    if len(remainingArgs) > 0:
        return remainingArgs


def importPySide():
    try:
        if "PySide" in sys.modules:
            return True

        required_modules = ["QtCore", "QtGui", "QtNetwork", "QtWebKit", "QtUiTools"]
        
        for module_name in required_modules:
            _named_import('PySide.%s' % module_name)

        from PySide import QtCore, QtGui, QtNetwork, QtWebKit, QtUiTools
        from PySide.QtCore import Signal, Slot, Property

        class UiLoader(QtUiTools.QUiLoader):
            def __init__(self):
                super(UiLoader, self).__init__()
                self._rootWidget = None

            def createWidget(self, className, parent=None, name=''):
                widget = super(UiLoader, self).createWidget(
                        className, parent, name)

                if name:
                    if self._rootWidget is None:
                        self._rootWidget = widget
                    elif not hasattr(self._rootWidget, name):
                        setattr(self._rootWidget, name, widget)
                    else:
                        # logger.error("Name collision! Ignoring second "
                        #         "occurrance of %r.", name)
                        si.LogMessage("Name collision! Ignoring second "
                                + "occurrance of %r." % name, C.siError)

                    if parent is not None:
                        setattr(parent, name, widget)
                    else:
                        # Sadly, we can't reparent it to self, since QUiLoader
                        # isn't a QWidget.
                        # logger.error("No parent specified! This will probably "
                        #         "crash due to C++ object deletion.")
                        si.LogMessage("No parent specified! This will probably "
                                + "crash due to C++ object deletion.", C.siError)

                return widget

            def load(self, fileOrName, parentWidget=None):
                if self._rootWidget is not None:
                    raise Exception("UiLoader is already started loading UI!")

                widget = super(UiLoader, self).load(fileOrName, parentWidget)

                if widget != self._rootWidget:
                    # logger.error("Returned widget isn't the root widget... "
                    #         "LOLWUT?")
                    si.LogMessage("Returned widget isn't the root widget... "
                        + "LOLWUT?", C.siError)

                self._rootWidget = None
                return widget

        def loadUi(uiFilename, parent=None):
            global _uiLoader
            if _uiLoader is None:
                _uiLoader = UiLoader()

            uiFile = QtCore.QFile(uiFilename, parent)
            if not uiFile.open(QtCore.QIODevice.ReadOnly):
                # logger.error("Couldn't open file %r!", uiFilename)
                si.LogMessage("Couldn't open file %r!" % uiFilename, C.siError)
                return None

            try:
                return _uiLoader.load(uiFile, parent)

            except:
                # logger.exception("Exception loading UI from %r!", uiFilename)
                si.LogMessage("Exception loading UI from %r!" % uiFilename, C.siError)

            finally:
                uiFile.close()
                uiFile.deleteLater()

            return None

        # logger.info("Successfully initialized PySide.")
        si.LogMessage("Successfully initialized PySide.", C.siInfo)

        globals().update(
                QtCore=QtCore,
                QtGui=QtGui,
                QtNetwork=QtNetwork,
                QtWebKit=QtWebKit,
                QtUiTools=QtUiTools,
                Signal=Signal,
                Slot=Slot,
                Property=Property,
                loadUi=loadUi,
                binding="PySide",
                )

        return True

    except ImportError:
        return False


def importPyQt():
    try:
        if "PyQt4" in sys.modules:
            return True

        import sip
        sip.setapi('QString', 2)
        sip.setapi('QVariant', 2)

        required_modules = ["QtCore", "QtGui", "QtNetwork", "QtWebKit", "uic"]

        for module_name in required_modules:
            _named_import('PyQt4.%s' % module_name)

        from PyQt4.QtCore import pyqtSignal as Signal
        from PyQt4.QtCore import pyqtSlot as Slot
        from PyQt4.QtCore import pyqtProperty as Property
        QtUiTools = object()

        def loadUi(uiFilename, parent=None):
            newWidget = uic.loadUi(uiFilename, parent)
            return newWidget

        # logger.info("Successfully initialized PyQt4.")
        si.LogMessage("Successfully initialized PyQt4.", C.siInfo)

        globals().update(
                QtCore=QtCore,
                QtGui=QtGui,
                QtNetwork=QtNetwork,
                QtWebKit=QtWebKit,
                QtUiTools=QtUiTools,
                Signal=Signal,
                Slot=Slot,
                Property=Property,
                loadUi=loadUi,
                binding="PyQt4",
                )

        return True

    except ImportError:
        return False


def isPySide():
    if binding == "PySide":
        return True

    return False


def isPyQt4():
    if binding == "PyQt4":
        return True

    return False

# thank you nathan horne
def wrapinstance(ptr, base=None):
    """convert a pointer to a Qt class instance (PySide/PyQt compatible)"""

    if ptr is None:
        return None
    ptr = long(ptr) #Ensure type
    if isPySide():
        if base is None:
            import shiboken
            qObj = shiboken.wrapInstance(long(ptr), QtCore.QObject)
            metaObj = qObj.metaObject()
            cls = metaObj.className()
            superCls = metaObj.superClass().className()
            if hasattr(QtGui, cls):
                base = getattr(QtGui, cls)
            elif hasattr(QtGui, superCls):
                base = getattr(QtGui, superCls)
            else:
                base = QtGui.QWidget
        return shiboken.wrapInstance(long(ptr), base)
    elif isPyQt4():
        import sip
        #base = QtCore.QObject
        return sip.wrapinstance(long(ptr), base)
    else:
        return None