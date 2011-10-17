message ( STATUS "---configuring QtSoftimage plugin---" )

add_softimage_plugin( QtSoftimage qtsoftimage.cpp )

include_directories ( ${QT_INCLUDE_DIR} ${QT_QTCORE_INCLUDE_DIR} ${QT_QTGUI_INCLUDE_DIR} )

link_directories ( ${QT_LIBRARY_DIR} )

target_link_libraries ( QtSoftimage ${QT_QTCORE_LIBRARY} ${QT_QTGUI_LIBRARY} )
