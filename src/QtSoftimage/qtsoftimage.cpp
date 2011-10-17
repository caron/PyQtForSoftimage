//  Qt for Softimage - Copyright (C)2011 - Jo Benayoun <jobenayoun.com>
//

//  LICENCE : This program is free software: you can redistribute it and/or modify
//            it under the terms of the GNU General Public License as published by
//            the Free Software Foundation, either version 3 of the License, or
//            (at your option) any later version.
//            
//            This program is distributed in the hope that it will be useful,
//            but WITHOUT ANY WARRANTY; without even the implied warranty of
//            MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//            GNU General Public License for more details.
//            
//            You should have received a copy of the GNU General Public License
//            along with this program.  If not, see <http://www.gnu.org/licenses/>.


//  NOTES : Get the Softimage anchor from xsi with the getQtSoftimageAnchor() command
//          or from the API with the same method.
//          The instance should be killed when the last child is closed, or the plugin
//          unloaded from Softimage, but for completeness a killQtSoftimageAnchor() is
//          provided.
//          We map key events with a hook which propagate them to the children of the
//          anchor.


#include <Windows.h>

#include <xsi_application.h>
#include <xsi_pluginregistrar.h>
#include <xsi_context.h>
#include <xsi_command.h>
#include <xsi_desktop.h>

#include <QWidget>
#include <QApplication>
#include <QEvent>
#include <QKeyEvent>
#include <Qt>


namespace QtSoftimage
{
	int Q_KEY_UP = 0x01000013;
	int Q_KEY_DOWN = 0x01000015;

	HHOOK hook;
	HWND xsihandle;
	QWidget *sianchor;

	LRESULT CALLBACK 
	listener(int ncode, WPARAM wparam, LPARAM lparam)
	{
		if (sianchor) {
			switch (wparam)
			{
			case (VK_UP):
				{
					QKeyEvent e = QKeyEvent(QEvent::KeyPress, Q_KEY_UP, 0);
					for (int i=0; i<sianchor->children().count(); ++i) {
						QApplication::sendEvent(sianchor->children().at(i), &e);
					}
				}
			case (VK_DOWN):
				{
					QKeyEvent e = QKeyEvent(QEvent::KeyPress, Q_KEY_DOWN, 0);
					for (int i=0; i<sianchor->children().count(); ++i) {
						QApplication::sendEvent(sianchor->children()[i], &e);
					}
				}
			}
		}
		return CallNextHookEx(hook, ncode, wparam, lparam);
	}

	void 
	deregisterHook()
	{
		if (! hook)
			return;
		UnhookWindowsHookEx(hook);
	}

	QWidget *
	getQtSoftimageAnchor()
	{
		if (! qApp) {
			xsihandle = (HWND)XSI::Application().GetDesktop().GetApplicationWindowHandle();
			if (! hook)
				hook = SetWindowsHookExW(WH_KEYBOARD, listener, 0, GetCurrentThreadId());
			int argc = 0;
			new QApplication(argc, 0);
		}

		if (! sianchor) {
			sianchor = new QWidget;
			sianchor->setObjectName("QtSoftimageAnchor");
			SetWindowLong((HWND)sianchor->winId(), GWL_STYLE, WS_CHILD);
			SetParent((HWND)sianchor->winId(), xsihandle);
			sianchor->setAttribute(Qt::WA_DeleteOnClose);
		}
		return sianchor;
	}

	void 
	killQtSoftimageAnchor()
	{
		QtSoftimage::deregisterHook();
		if (QtSoftimage::sianchor) {
			delete QtSoftimage::sianchor;
			QtSoftimage::sianchor = 0;
		}
		if (qApp) {
			QApplication *app = (QApplication *)QApplication::instance();
			delete app;
			app = 0;
		}
	}

};


using namespace XSI;


SICALLBACK 
XSILoadPlugin(PluginRegistrar &reg)
{
	reg.PutName("QtSoftimage");
	reg.PutVersion(0,2);
	reg.PutAuthor("Jonathan Benayoun");
	reg.PutURL("www.jobenayoun.com");
	reg.RegisterCommand("getQtSoftimageAnchor");
	reg.RegisterCommand("killQtSoftimageAnchor");
	return CStatus::OK;
}

SICALLBACK 
XSIUnloadPlugin(PluginRegistrar &reg)
{
	QtSoftimage::killQtSoftimageAnchor();
	return CStatus::OK;
}

SICALLBACK 
getQtSoftimageAnchor_Init(const CRef &ref)
{
	Command cmd = Context(ref).GetSource();
	cmd.EnableReturnValue(true);
	return CStatus::OK;
}

SICALLBACK 
getQtSoftimageAnchor_Execute(const CRef &ref)
{
	Context ctxt = Context(ref);
	QWidget *anchor = QtSoftimage::getQtSoftimageAnchor();
	ctxt.PutAttribute("ReturnValue", CValue(ULONG(anchor)));
	return CStatus::OK;
}

SICALLBACK 
killQtSoftimageAnchor_Execute(CRef &ref)
{
	QtSoftimage::killQtSoftimageAnchor();
	return CStatus::OK;
}

