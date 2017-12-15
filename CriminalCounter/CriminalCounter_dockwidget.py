# -*- coding: utf-8 -*-
"""
/***************************************************************************
 CriminalCounterDockWidget
                                 A QGIS plugin
 This plugin helps the policeman in duty to catch criminals
                             -------------------
        begin                : 2017-12-15
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Group6_Geomatics_TUDelft
        email                : dushenglan940128@163.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os

from PyQt4 import QtGui, uic
from PyQt4.QtCore import pyqtSignal

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'CriminalCounter_dockwidget_base.ui'))


class CriminalCounterDockWidget(QtGui.QDockWidget, FORM_CLASS):

    closingPlugin = pyqtSignal()

    def __init__(self, parent=None):
        """Constructor."""
        super(CriminalCounterDockWidget, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()

