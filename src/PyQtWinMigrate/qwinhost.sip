/*
 * This file is part of PyQtWinMigrate.
 * 
 * PyQtWinMigrate is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

class QWinHost : QWidget
{

%TypeHeaderCode
#include "qwinhost.h"
%End

public:
    QWinHost(QWidget *parent /TransferThis/= 0, Qt::WFlags f = 0);
    ~QWinHost();

    void setWindow(HWND);
    HWND window() const;

protected:
    //virtual HWND createWindow(HWND parent, HINSTANCE instance);

    bool event(QEvent *e);
    void showEvent(QShowEvent *);
    void focusInEvent(QFocusEvent*);
    void resizeEvent(QResizeEvent*);

    bool winEvent(MSG *msg, long *result);

};
