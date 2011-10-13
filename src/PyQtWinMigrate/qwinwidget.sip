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

class QWinWidget : QWidget
{

%TypeHeaderCode
#include "qwinwidget.h"
%End

public:
    QWinWidget( HWND hParentWnd, QObject *parent /TransferThis/= 0, Qt::WFlags f = 0 );
    ~QWinWidget();

    void show();
    void center();
    void showCentered();

    HWND parentWindow() const;

protected:
    void childEvent( QChildEvent *e );
    bool eventFilter( QObject *o, QEvent *e );

    bool focusNextPrevChild(bool next);
    void focusInEvent(QFocusEvent *e);

    bool winEvent(MSG *msg, long *result);
    
};
