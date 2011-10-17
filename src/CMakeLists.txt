cmake_minimum_required ( VERSION 2.6 )

project ( PyQtForSoftimage )

set ( CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${PROJECT_SOURCE_DIR}/CMake/Modules )

find_package( Softimage )
find_package( Qt4 REQUIRED QtCore QtGui)

add_subdirectory( QtSoftimage )