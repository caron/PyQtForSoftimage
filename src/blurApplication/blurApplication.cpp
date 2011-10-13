//*****************************************************************************
/*
	\file BlurApplication.cpp

	[TITLE]
	Commands to access hidden values (HWND & HINSTANCE) from Python

	[CREATION INFO]
	Author:Eric Hulser
	E-mail:eric@blur.com
	Company:Blur Studio
	Created:July 21, 2009
	Last Updated:July 21, 2009

	Copyright (c) 2009, Blur Studio Inc.
All rights reserved.

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions 
are met:

    * Redistributions of source code must retain the above copyright 
	notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above 
	copyright notice, this list of conditions and the following 
	disclaimer in the documentation and/or other materials provided 
	with the distribution.
    * Neither the name of the Blur Studio Inc. nor the names of its 
	contributors may be used to endorse or promote products derived 
	from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS 
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT 
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS 
FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE 
COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, 
INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, 
BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; 
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT 
LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN 
ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE 
POSSIBILITY OF SUCH DAMAGE.

*/
//*****************************************************************************

#include <windows.h>
#include <stdio.h>

#include <xsi_application.h>
#include <xsi_desktop.h>
#include <xsi_pluginregistrar.h>
#include <xsi_context.h>
#include <xsi_command.h>
#include <xsi_argument.h>
#include <xsi_status.h>

using namespace XSI;

// ----------------------------------------------------------------------------------------------------------------------------------------------------------
// register commands and menus
// ----------------------------------------------------------------------------------------------------------------------------------------------------------
XSIPLUGINCALLBACK CStatus XSILoadPlugin( PluginRegistrar& in_reg )
{
	in_reg.PutAuthor(L"Eric Hulser");
	in_reg.PutName(L"BlurApplication");
	in_reg.PutEmail(L"eric@blur.com");
	in_reg.PutURL(L"http://www.blur.com");
	in_reg.PutVersion(1,0);

	// External command, to write a pointcache file from the selected object
	in_reg.RegisterCommand( L"GetWindowHandle",			L"GetWindowHandle" );
	in_reg.RegisterCommand( L"GetPluginInstance",		L"GetPluginInstance" );

	return CStatus::OK;
}

// ----------------------------------------------------------------------------------------------------------------------------------------------------------
// BlurApplication GetWindowHandle
// ----------------------------------------------------------------------------------------------------------------------------------------------------------

XSIPLUGINCALLBACK XSI::CStatus GetWindowHandle_Init( const XSI::CRef& in_context )
{
	Context ctx(in_context);
	return CStatus::OK;
}

XSIPLUGINCALLBACK XSI::CStatus GetWindowHandle_Execute( XSI::CRef& in_context )
{
	// Get the Window Handle for the Application
	Application app;

	HWND hwnd = (HWND)app.GetDesktop().GetApplicationWindowHandle();
	XSI::CValue handle = XSI::CValue( (LONG) hwnd );

	Context ctxt(in_context);
	ctxt.PutAttribute( L"ReturnValue", handle );

	return CStatus::OK;
}

// ----------------------------------------------------------------------------------------------------------------------------------------------------------
// BlurApplication GetPluginInstance
// ----------------------------------------------------------------------------------------------------------------------------------------------------------

XSIPLUGINCALLBACK XSI::CStatus GetPluginInstance_Init( const XSI::CRef& in_context )
{
	Context ctx(in_context);
	return CStatus::OK;
}

XSIPLUGINCALLBACK XSI::CStatus GetPluginInstance_Execute( XSI::CRef& in_context )
{
	// Get the Window Handle for the Application
	Application app;

	HWND hwnd = (HWND)app.GetDesktop().GetApplicationWindowHandle();

// support 32 and 64 bit compilation
#if _WIN64
	XSI::CValue handle = XSI::CValue( GetWindowLongPtr( hwnd, GWLP_HINSTANCE ) );
#else
	XSI::CValue handle = XSI::CValue( GetWindowLong( hwnd, GWL_HINSTANCE ) );
#endif

	Context ctxt(in_context);
	ctxt.PutAttribute( L"ReturnValue", handle );

	return CStatus::OK;
}
