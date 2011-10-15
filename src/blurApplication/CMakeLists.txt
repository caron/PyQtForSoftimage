message ( STATUS "---configuring blurApplication plugin---" )

#add_library ( blurApplication blurApplication.cpp )
add_softimage_plugin( blurApplication blurApplication.cpp )