**PyQtForSoftimage** is a plugin for hosting PyQt applications inside Softimage's interface.

## License:
The PyQtForSoftimage plugin source code contains work contributed by other open
source projects, specifically the work done by Jo Benayoun which is released
under GPLv3. The CMake system and the python events plugin are released under
the "New BSD" license. The FindSoftimage CMake module was contributed by Alan
Jones and released under AGPL. The copyright notices can be found in files named
LICENSE in the respective source directories. 

## Installation:
This is for users who are just installing the provided addon. These instructions describe how to use the plugin with system installed version of Python. All requirements needed to use system Python inside Softimage must be met first. These instructions are listed below...

1. Install [Python](https://www.python.org/downloads/). This plugin was tested with version 2.7.x but can work with older versions.
2. Install [pywin32 217](http://sourceforge.net/projects/pywin32/files/pywin32/Build%20217/)
3. Install [PyQt4](http://sourceforge.net/projects/pyqt/files/PyQt4/) OR [PySide](https://download.qt.io/official_releases/pyside)
4. In Softimage, uncheck "Use Python Installed with Softimage (Windows Only)" from Preferences/Scripting.
5. Install [PyQtForSoftimage](http://www.steven-caron.com/downloads/tools/PyQtForSoftimage_beta6.xsiaddon) addon.
6. Run example scripts...

If you want to use native Python installed with Softimage, you must install PyQt4/PySide into a location which Softimage can import from. Either you install PyQt4/PySide directly into Softimage's Python install "Softimage Version\Application\python\Lib\site-packages" or make sure you put the PyQt4/PySide installation directory on the [module search path](http://docs.python.org/2/tutorial/modules.html#the-module-search-path).
   
## Build Instructions:
**These instructions are not complete yet!**

This section is only for users wishing to customize PyQtForSoftimage.

PyQtForSoftimage has been developed under Windows, support for Linux is untested.

PyQtForSoftimage has been built and tested with the following dependencies...

* CMake 3.1.3     http://www.cmake.org/download/
* Qt 4.8.5        http://download.qt.io/archive/qt/

Compling Qt from source can be quite an involved process, its advised to obtain
the precompiled binaries.

Once you have installed all the dependencies get the source code either by
downloading the source archive directly from github or obtaining a distributed
version control system like git or mecurial (with hg-git plugin). Information on
setting up git is available from http://help.github.com/.

Now you can run CMake on the source directory and it will generate the necessary
project files for compiling.

At this time you will need to move the plugin files to a plugin/addon directory
by hand. Copy QtSoftimage.dll, qtevents.py, sisignals.py, pyqt_example.py and the Qt module directory to a plugins directory and Restart Softimage.

## PySide support:
PySide support is availble now. The Qt module which is now in the source tree handles the switch between PyQt or PySide. You should call Qt.initialize() at the top of your files... it currently favors PySide over PyQt so if you have both installed but want to use one or the other you can pass in "PySide" or "PyQt4".

```python
# favors PySide
import Qt
Qt.initialize()
```

```python
# forces PyQt4
import Qt
Qt.initialize("PyQt4")
```

When using .ui files with PySide you need to do a few things to get it to load like PyQt. There is a function in the Qt module ```Qt.loadUi``` which will return the loaded QWidgets but has trouble with layouts. The proper way to handle this is illustrated in the pyqt_examples.py file and illustrated below...

```python
class ExampleUIFile( QDialog ):
   def __init__( self, parent, uifilepath ):
      QDialog.__init__( self, parent )

      # load ui file
      self.ui = loadUi( uifilepath, self )

      # this is for PySide only
      # create a layout, add the loaded ui
      # this is to make sure the widget doesn't
      # get garbaged collected
      self.centralLayout = QGridLayout( self )
      self.centralLayout.setContentsMargins( 9, 9, 9, 9 )
      self.centralLayout.addWidget( self.ui )

      # since PySide doesn't load the ui like PyQt
      # lets get some properties from the ui file that are still relevant...
      # the size of the dialog set in QtDesigner
      self.resize( self.ui.size() )
      # the window title set in QtDesigner
      self.setWindowTitle( self.ui.windowTitle() )
```
