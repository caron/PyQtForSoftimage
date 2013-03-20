#==========================================================================
# This CMake module assists in creating Softimage plugins and shaders
# on both linux and windows.

#------------------------------------------------------------------------------------------------
# 	Author: Alan Jones - Email: skyphyr@gmail.com
# 	Copyright (C) 2010  Troublemaker Studios
# 
# 	This program is free software: you can redistribute it and/or modify
# 	it under the terms of the GNU Affero General Public License as
# 	published by the Free Software Foundation, either version 3 of the
# 	License, or (at your option) any later version.
# 
# 	This program is distributed in the hope that it will be useful,
# 	but WITHOUT ANY WARRANTY; without even the implied warranty of
# 	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# 	GNU Affero General Public License for more details.
# 
# 	You should have received a copy of the GNU Affero General Public License
# 	along with this program.  If not, see <http://www.gnu.org/licenses/>.
#------------------------------------------------------------------------------------------------
    
# It provides a preprocessor definiton SOFTIMAGE_<MAJORVERSION>_<MINORVERSION>
# So for 2011 Subscription Advantage Pack this would be SOFTIMAGE_9_5
# If you need to have version specific code in your plugins use #ifdef SOFTIMAGE_9_5

# While it sets some variables (such as Softimage_INCLUDE_DIR, Softimage_LIBRARIES,
# and Softimage_LIBRARY_DIR), you should not need to use these. Instead use the
# convenience functions provided by this module

# functions provided by this module are
# add_softimage_plugin(<NAME> <SOURCE FILES>)
# add_mentalray_shader(<NAME> <SOURCE FILES>)
# add_softimage_spdls(<SPDL FILES>)
# add_softimage_scripted_plugins(<SCRIPTED PLUGIN FILES>)
# add_softimage_compounds(<CATEGORY> <COMPOUND FILES>)
# add_softimage_rtcompounds(<CATEGORY> <RTCOMPOUND FILES>)

# The category for compounds and rtcompounds can contain multiple levels
# use forwardslashes to separate them. e.g. Deformation/Effects

# Recommended workflow when building:
# This module supports compilation and installation.
# CMAKE_INSTALL_PREFIX should be set to an Addons subdirectory
# If the initial configuration is made from a Softimage environment
# then it will automatically set it to the Addons/<PROJECT_NAME>
# subdirectory of your user preferences directory
# Note: if the environment is for a different version than the
# one you are building against this may be undesirable
#==========================================================================

#Choose directories to search based on version
set (SOFTPATHS_12_0
    "c:/Program Files/Autodesk/Softimage 2014/XSISDK/include/"
    /usr/Softimage/Softimage_2014/XSISDK/include/
    /usr/local/Softimage/Softimage_2014/XSISDK/include/
)

set (SOFTPATHS_11_0
    "c:/Program Files/Autodesk/Softimage 2013/XSISDK/include/"
    /usr/Softimage/Softimage_2013/XSISDK/include/
    /usr/local/Softimage/Softimage_2013/XSISDK/include/
)

set (SOFTPATHS_10_5
    "c:/Program Files/Autodesk/Softimage 2012 Subscription Advantage Pack/XSISDK/include/"
    "c:/Program Files/Autodesk/Softimage 2012.SAP/XSISDK/include/"
    "c:/Program Files/Autodesk/Softimage 2012.5/XSISDK/include/"
    /usr/Softimage/Softimage_2012.5/XSISDK/include/
    /usr/local/Softimage/Softimage_2012.5/XSISDK/include/
)

set (SOFTPATHS_10_0
    "c:/Program Files/Autodesk/Softimage 2012/XSISDK/include/"
    /usr/Softimage/Softimage_2012/XSISDK/include/
    /usr/local/Softimage/Softimage_2012/XSISDK/include/
)

set (SOFTPATHS_9_5
	"c:/Program Files/Autodesk/Softimage 2011 Subscription Advantage Pack/XSISDK/include/"
	/usr/Softimage/Softimage_2011_Subscription_Advantage_Pack/XSISDK/include/
	/opt/Softimage/Softimage_2011_Subscription_Advantage_Pack/XSISDK/include/
	/usr/local/Softimage/Softimage_2011_Subscription_Advantage_Pack/XSISDK/include/
)

#need to add linux paths
set (SOFTPATHS_9_2
    "c:/Program Files/Autodesk/Softimage 2011 SP2/XSISDK/include/"
)

set (SOFTPATHS_9_0
	"c:/Program Files/Autodesk/Softimage 2011 SP1/XSISDK/include/"
	"c:/Program Files/Autodesk/Softimage 2011/XSISDK/include/"
	/usr/Softimage/Softimage_2011_SP1/XSISDK/include/
	/opt/Softimage/Softimage_2011_SP1/XSISDK/include/
	/usr/local/Softimage/Softimage_2011_SP1/XSISDK/include/
	/usr/Softimage/Softimage_2011/XSISDK/include/
	/opt/Softimage/Softimage_2011/XSISDK/include/
	/usr/local/Softimage/Softimage_2011/XSISDK/include/
)

set (SOFTPATHS_8_0
	"c:/Program Files/Autodesk/Softimage 2010 SP1/XSISDK/include/"
	"c:/Program Files/Autodesk/Softimage 2010/XSISDK/include/"
	"c:/Softimage/Softimage_2010_SP1_x64/XSISDK/include/"
	/usr/Softimage/Softimage_2010_SP1/XSISDK/include/
	/opt/Softimage/Softimage_2010_SP1/XSISDK/include/
	/usr/local/Softimage/Softimage_2010_SP1/XSISDK/include/
	/usr/Softimage/Softimage_2010/XSISDK/include/
	/opt/Softimage/Softimage_2010/XSISDK/include/
	/usr/local/Softimage/Softimage_2010/XSISDK/include/
)

set (SOFTPATHS_7_5
	c:/Softimage/XSI_7.5/XSISDK/include/
	/usr/Softimage/XSI_7.5/XSISDK/include/
	/opt/Softimage/XSI_7.5/XSISDK/include/
	/usr/local/Softimage/XSI_7.5/XSISDK/include/
)

set (SOFTPATHS_7_0
	c:/Softimage/XSI_7.01/XSISDK/include/
	/usr/Softimage/XSI_7.01/XSISDK/include/
	/opt/Softimage/XSI_7.01/XSISDK/include/
	/usr/local/Softimage/XSI_7.01/XSISDK/include/
)

if (${Softimage_FIND_VERSION})
	#We need the exact version
	if (${Softimage_FIND_VERSION_EXACT})
		 if (${Softimage_FIND_VERSION_MAJOR} EQUAL 12)
		 		set(Softimage_SEARCH_INCLUDE_PATH "${Softimage_SEARCH_INCLUDE_PATH}"
			${SOFTPATHS_11_0}
            )

		 endif()
	    if (${Softimage_FIND_VERSION_MAJOR} EQUAL 11)
            set(Softimage_SEARCH_INCLUDE_PATH "${Softimage_SEARCH_INCLUDE_PATH}"
			${SOFTPATHS_11_0}
            )
        endif()
        if (${Softimage_FIND_VERSION_MAJOR} EQUAL 10)
            if (${Softimage_FIND_VERSION_MINOR} EQUAL 5)
                set(Softimage_SEARCH_INCLUDE_PATH "${Softimage_SEARCH_INCLUDE_PATH}"
				${SOFTPATHS_10_5}
                )
            elseif (${Softimage_FIND_VERSION_MINOR} EQUAL 0)
                set(Softimage_SEARCH_INCLUDE_PATH "${Softimage_SEARCH_INCLUDE_PATH}"
				${SOFTPATHS_10_0}
                )
            endif()
        endif()
		if (${Softimage_FIND_VERSION_MAJOR} EQUAL 9)
		    message(STATUS ${Softimage_FIND_VERSION_MAJOR} )
			if (${Softimage_FIND_VERSION_MINOR} EQUAL 5)
				set(Softimage_SEARCH_INCLUDE_PATH "${Softimage_SEARCH_INCLUDE_PATH}"
				
				${SOFTPATHS_9_5}
				)
			elseif (${Softimage_FIND_VERSION_MINOR} EQUAL 2)
			    set(Softimage_SEARCH_INCLUDE_PATH "${Softimage_SEARCH_INCLUDE_PATH}"
                ${SOFTPATHS_9_2}
                )
			elseif (${Softimage_FIND_VERSION_MINOR} EQUAL 0)
				set(Softimage_SEARCH_INCLUDE_PATH "${Softimage_SEARCH_INCLUDE_PATH}"
				${SOFTPATHS_9_0}
				)
			endif()
		endif()
		if (${Softimage_FIND_VERSION_MAJOR} EQUAL 8)
			set(Softimage_SEARCH_INCLUDE_PATH "${Softimage_SEARCH_INCLUDE_PATH}"
				${SOFTPATHS_8_0}
			)
		endif()
		if (${Softimage_FIND_VERSION_MAJOR} EQUAL 7)
			if (${Softimage_FIND_VERSION_MINOR} EQUAL 5)
				set(Softimage_SEARCH_INCLUDE_PATH "${Softimage_SEARCH_INCLUDE_PATH}"
					${SOFTPATHS_7_5}
					)
			elseif (${Softimage_FIND_VERSION_MINOR} EQUAL 0)
				set(Softimage_SEARCH_INCLUDE_PATH "${Softimage_SEARCH_INCLUDE_PATH}"
					${SOFTPATHS_7_0}
					)
			endif()
		endif()
	#We need at least this version
	else()
	    if (${Softimage_FIND_VERSION_MAJOR} LESS 12)
	    		set(Softimage_SEARCH_INCLUDE_PATH "${Softimage_SEARCH_INCLUDE_PATH}"
				${SOFTPATHS_10_0}
            )
       endif()
	    if (${Softimage_FIND_VERSION_MAJOR} LESS 11)
	        if (${Softimage_FIND_VERSION_MINOR} LESS 6)
                set(Softimage_SEARCH_INCLUDE_PATH "${Softimage_SEARCH_INCLUDE_PATH}"
				${SOFTPATHS_10_5}
                )
            elseif (${Softimage_FIND_VERSION_MINOR} LESS 1)
                set(Softimage_SEARCH_INCLUDE_PATH "${Softimage_SEARCH_INCLUDE_PATH}"
				${SOFTPATHS_10_0}
                )
            endif()
	    endif()
		if (${Softimage_FIND_VERSION_MAJOR} LESS 10)
			if (${Softimage_FIND_VERSION_MINOR} LESS 6)
				set(Softimage_SEARCH_INCLUDE_PATH "${Softimage_SEARCH_INCLUDE_PATH}"
				${SOFTPATHS_9_5}
				)
			elseif (${Softimage_FIND_VERSION_MINOR} LESS 1)
				set(Softimage_SEARCH_INCLUDE_PATH "${Softimage_SEARCH_INCLUDE_PATH}"
				${SOFTPATHS_9_0}
				)
			endif()
		endif()
		if (${Softimage_FIND_VERSION_MAJOR} LESS 9)
			set(Softimage_SEARCH_INCLUDE_PATH "${Softimage_SEARCH_INCLUDE_PATH}"
				${SOFTPATHS_8_0}
			)
		endif()
		if (${Softimage_FIND_VERSION_MAJOR} LESS 8)
			if (${Softimage_FIND_VERSION_MINOR} LESS 6)
				set(Softimage_SEARCH_INCLUDE_PATH "${Softimage_SEARCH_INCLUDE_PATH}"
					${SOFTPATHS_7_5}
					)
			elseif (${Softimage_FIND_VERSION_MINOR} LESS 1)
				set(Softimage_SEARCH_INCLUDE_PATH "${Softimage_SEARCH_INCLUDE_PATH}"
					${SOFTPATHS_7_0}
					)
			endif()
		endif()
	endif()
#No version checking has been requested - grab the newest
else()
	set(Softimage_SEARCH_INCLUDE_PATH "${Softimage_SEARCH_INCLUDE_PATH}"
		${SOFTPATHS_12_0}
		${SOFTPATHS_11_0}
		${SOFTPATHS_10_5}
		${SOFTPATHS_10_0}
		${SOFTPATHS_9_5}
		${SOFTPATHS_9_2}
		${SOFTPATHS_9_0}
		${SOFTPATHS_8_0}
		${SOFTPATHS_7_5}
		${SOFTPATHS_7_0}
		)
endif ()

# Softimage includes
find_path( Softimage_INCLUDE_DIR xsi_application.h
	${Softimage_SEARCH_INCLUDE_PATH}
	$ENV{XSISDK_ROOT}/include/
	)

# Softimage library

#We're on windows
if (WIN32)
	if ("${CMAKE_SHARED_LINKER_FLAGS}" MATCHES "x64")
		find_library( Softimage_CORESDK_LIBRARY sicoresdk
			"${Softimage_INCLUDE_DIR}/../lib/nt-x86-64"
			)
		find_library( Softimage_CPPSDK_LIBRARY sicppsdk
			"${Softimage_INCLUDE_DIR}/../lib/nt-x86-64"
			)
		find_library( Softimage_MENTALRAY_LIBRARIES shader
			"${Softimage_INCLUDE_DIR}/../lib/nt-x86-64"
			)
	else()
		find_library( Softimage_CORESDK_LIBRARY sicoresdk
			"${Softimage_INCLUDE_DIR}/../lib/nt-x86"
			)
		find_library( Softimage_CPPSDK_LIBRARY sicppsdk
			"${Softimage_INCLUDE_DIR}/../lib/nt-x86"
			)
		find_library( Softimage_MENTALRAY_LIBRARIES shader
		"${Softimage_INCLUDE_DIR}/../lib/nt-x86"
		)
	endif()
#We're on linux
else()
find_library( Softimage_CORESDK_LIBRARY sicoresdk
	"${Softimage_INCLUDE_DIR}/../../Application/bin/"
	)

find_library( Softimage_CPPSDK_LIBRARY sicppsdk
	"${Softimage_INCLUDE_DIR}/../../Application/bin/"
	)
endif ()

set( Softimage_LIBRARIES ${Softimage_CORESDK_LIBRARY} ${Softimage_CPPSDK_LIBRARY} )

# Softimage library path
get_filename_component( Softimage_LIBRARY_DIR ${Softimage_CORESDK_LIBRARY} PATH )

#Check which version we wound up with
set(Softimage_MAJOR_VERSION 0)
set(Softimage_MINOR_VERSION 0)
if (${Softimage_INCLUDE_DIR} MATCHES "Softimage.2014")
    set(Softimage_MAJOR_VERSION 12)
    set(Softimage_MINOR_VERSION 0)
elseif (${Softimage_INCLUDE_DIR} MATCHES "Softimage.2013")
    set(Softimage_MAJOR_VERSION 11)
    set(Softimage_MINOR_VERSION 0)
elseif (${Softimage_INCLUDE_DIR} MATCHES "Softimage.2012\\5")
    set(Softimage_MAJOR_VERSION 10)
    set(Softimage_MINOR_VERSION 5)
elseif (${Softimage_INCLUDE_DIR} MATCHES "Softimage.2012")
    set(Softimage_MAJOR_VERSION 10)
    set(Softimage_MINOR_VERSION 0)
elseif (${Softimage_INCLUDE_DIR} MATCHES "Softimage.2011.Subscription.Advantage.Pack")
	set(Softimage_MAJOR_VERSION 9)
	set(Softimage_MINOR_VERSION 5)
elseif (${Softimage_INCLUDE_DIR} MATCHES "Softimage.2011")
	set(Softimage_MAJOR_VERSION 9)
	set(Softimage_MINOR_VERSION 0)
elseif (${Softimage_INCLUDE_DIR} MATCHES "Softimage.2010")
	set(Softimage_MAJOR_VERSION 8)
	set(Softimage_MINOR_VERSION 0)
elseif (${Softimage_INCLUDE_DIR} MATCHES "XSI.7\\.5")
	set(Softimage_MAJOR_VERSION 7)
	set(Softimage_MINOR_VERSION 5)
elseif (${Softimage_INCLUDE_DIR} MATCHES "XSI.7")
	set(Softimage_MAJOR_VERSION 7)
	set(Softimage_MINOR_VERSION 0)
endif ()

#Check whether we met the requirements to have found Softimage
set (Softimage_FOUND false)
if (${Softimage_FIND_VERSION})
	if (${Softimage_FIND_VERSION_EXACT})
		if (${Softimage_MAJOR_VERSION} EQUAL ${Softimage_FIND_VERSION_MAJOR})
			if(${Softimage_MINOR_VERSION} EQUAL ${Softimage_FIND_VERSION_MINOR})
				set(Softimage_FOUND true)
			endif()
		endif()
	#Didn't need to be exact, but is it a late enough version?
	else()
		if (${Softimage_MAJOR_VERSION} EQUAL ${Softimage_FIND_VERSION_MAJOR})
			if(${Softimage_MINOR_VERSION} EQUAL ${Softimage_FIND_VERSION_MINOR} OR ${Softimage_MINOR_VERSION} GREATER ${Softimage_FIND_VERSION_MINOR})
				set(Softimage_FOUND true)
			endif()
		elseif(${Softimage_MAJOR_VERSION} GREATER ${Softimage_FIND_VERSION_MAJOR})
			set(Softimage_FOUND true)
		endif()
	endif()
#No particular version was required
else()
	if (NOT ${Softimage_INCLUDE_DIR} STREQUAL "")
		set(Softimage_FOUND true)
	endif()
endif()

#Let's set a define for the softimage version - if it's unknown it'll be SOFTIMAGE00
set_property(DIRECTORY APPEND PROPERTY COMPILE_DEFINITIONS SOFTIMAGE_${Softimage_MAJOR_VERSION}_${Softimage_MINOR_VERSION})

#Where abouts is the current user's Softimage user directory likely to be - check for it and set the installation prefix to be there
if (NOT $ENV{XSI_USERHOME} STREQUAL "")
	if(CMAKE_INSTALL_PREFIX_INITIALIZED_TO_DEFAULT)
		set(CMAKE_INSTALL_PREFIX $ENV{XSI_USERHOME}/Addons/${PROJECT_NAME}/ CACHE PATH "Where to install ${PROJECT_NAME}" FORCE)
	endif()
endif()

# did we find everything?
include( FindPackageHandleStandardArgs )

set (Softimage_STANDARD_ARGS
  Softimage_INCLUDE_DIR
  Softimage_LIBRARIES
  Softimage_LIBRARY_DIR
  Softimage_FOUND
)

if (WIN32)
	set (Softimage_STANDARD_ARGS "${Softimage_STANDARD_ARGS}"
		Softimage_MENTALRAY_LIBRARIES
		)
endif()

find_package_handle_standard_args( "Softimage" DEFAULT_MSG
	${Softimage_STANDARD_ARGS}
	)

set(Softimage_PLUGIN_DESTINATION Application/Plugins/)
set(Softimage_SPDL_DESTINATION Application/spdl/)
set(Softimage_COMPOUND_DESTINATION Data/Compounds/)
set(Softimage_RTCOMPOUND_DESTINATION Data/RTCompounds/)

#The filename for plugins and destination for shaders depends upon the platform and architecture
if (WIN32)
	set_property(DIRECTORY APPEND PROPERTY COMPILE_DEFINITIONS WINDOWS WIN32)
	#64bit
	if ("${CMAKE_SHARED_LINKER_FLAGS}" MATCHES "x64")
		set(Softimage_MENTALRAY_DESTINATION Application/bin/nt-x86-64)
		set(Softimage_PLUGIN_SUFFIX .64.dll)
	#32bit
	else()
		set(Softimage_MENTALRAY_DESTINATION Application/bin/nt-x86)
		set(Softimage_PLUGIN_SUFFIX .32.dll)
	endif()
#And if it's linux
else()
	set_property(DIRECTORY APPEND PROPERTY COMPILE_DEFINITIONS LINUX=1 unix UNIX)
	if (${CMAKE_SYSTEM_PROCESSOR} STREQUAL "x86_64")
		set(Softimage_MENTALRAY_DESTINATION Application/bin/linux-x86-64)
		set(Softimage_PLUGIN_SUFFIX .64.so)
	#32bit
	else()
		set(Softimage_MENTALRAY_DESTINATION Application/bin/linux-x86)
		set(Softimage_PLUGIN_SUFFIX .32.so)
	endif()
endif()

function (add_softimage_plugin name)
	include_directories(
	${Softimage_INCLUDE_DIR}
	)

	set(sources "${ARGV}")
	LIST(REMOVE_AT sources 0)
	
	add_library(${name} SHARED ${sources})

	target_link_libraries(${name} ${Softimage_LIBRARIES})

	set_target_properties(${name} PROPERTIES SUFFIX "${Softimage_PLUGIN_SUFFIX}")
	set_target_properties(${name} PROPERTIES PREFIX "")

	install(TARGETS ${name}
			RUNTIME DESTINATION ${Softimage_PLUGIN_DESTINATION}
			LIBRARY DESTINATION ${Softimage_PLUGIN_DESTINATION}
		)
endfunction(add_softimage_plugin)

function (add_mentalray_shader name)
	include_directories(
	${Softimage_INCLUDE_DIR}
	)

	set(sources "${ARGV}")
	LIST(REMOVE_AT sources 0)

	add_library(${name} SHARED ${sources})

	if (WIN32)
		target_link_libraries(${name} ${Softimage_MENTALRAY_LIBRARIES})
	endif()

	set_target_properties(${name} PROPERTIES PREFIX "")

	install(TARGETS ${name} 
			RUNTIME DESTINATION ${Softimage_MENTALRAY_DESTINATION}
			LIBRARY DESTINATION ${Softimage_MENTALRAY_DESTINATION}
		)
endfunction(add_mentalray_shader)

function (add_softimage_spdls)
	install(FILES ${ARGV} DESTINATION ${Softimage_SPDL_DESTINATION})
endfunction(add_softimage_spdls)

function (add_softimage_scripted_plugins)
	install(FILES ${ARGV} DESTINATION ${Softimage_PLUGIN_DESTINATION})
endfunction(add_softimage_scripted_plugins)

function (add_softimage_compounds CATEGORY)
	set(compounds "${ARGV}")
	LIST(REMOVE_AT compounds 0)
	install(FILES ${compounds} DESTINATION "${Softimage_COMPOUND_DESTINATION}${CATEGORY}")
endfunction(add_softimage_compounds)

function (add_softimage_rtcompounds CATEGORY)
	set(rtcompounds "${ARGV}")
	LIST(REMOVE_AT rtcompounds 0)
	install(FILES ${rtcompounds} DESTINATION "${Softimage_RTCOMPOUND_DESTINATION}${CATEGORY}")
endfunction(add_softimage_rtcompounds)
