# -*- coding: utf-8 -*-

# Copyright (c) 2011 Christopher S. Case, David H. Bronke

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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
                si.LogMessage("[PyQtForSoftimage] PyQt4 requested, but not installed.", C.siWarning)

            if not importPySide():
                si.LogMessage("[PyQtForSoftimage] Couldn't import PySide or PyQt4! You must have "
                    + "one or the other to run this app.", C.siError)
    else:
        if not importPySide():
            if prefer is not None:
                si.LogMessage("[PyQtForSoftimage] PySide requested, but not installed.", C.siWarning)

            if not importPyQt():
                si.LogMessage("[PyQtForSoftimage] Couldn't import PySide or PyQt4! You must have "
                    + "one or the other to run this app.", C.siError)

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
            def __init__(self, baseinstance):
                super(UiLoader, self).__init__()
                self.baseinstance = baseinstance

            def createWidget(self, className, parent=None, name=""):
                widget = super(UiLoader, self).createWidget(
                    className, parent, name)

                if parent is None:
                    return self.baseinstance
                else:
                    setattr(self.baseinstance, name, widget)
                    return widget

        def loadUi(uifile, parent=None):
            loader = UiLoader(parent)
            ui = loader.load(uifile)
            QtCore.QMetaObject.connectSlotsByName(ui)
            return ui

        si.LogMessage("[PyQtForSoftimage] Successfully initialized PySide.", C.siInfo)

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

        si.LogMessage("[PyQtForSoftimage] Successfully initialized PyQt4.", C.siInfo)

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
        from PySide import shiboken
        if base is None:
            qObj = shiboken.wrapInstance(ptr, QtCore.QObject)
            metaObj = qObj.metaObject()
            cls = metaObj.className()
            superCls = metaObj.superClass().className()
            if hasattr(QtGui, cls):
                base = getattr(QtGui, cls)
            elif hasattr(QtGui, superCls):
                base = getattr(QtGui, superCls)
            else:
                base = QtGui.QWidget
        return shiboken.wrapInstance(ptr, base)
    elif isPyQt4():
        import sip
        return sip.wrapinstance(ptr, base)
    else:
        return None
