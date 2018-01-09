# -*- coding: utf-8 -*-
"""
/***************************************************************************
 criminal_counterDockWidget
                                 A QGIS plugin
 This plugin helps the policeman on duty to catch criminals
                             -------------------
        begin                : 2018-01-07
        git sha              : $Format:%H$
        copyright            : (C) 2018 by group6
        email                : ^dushenglan940128@163.com
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

from qgis.core import *
from qgis.utils import iface
from PyQt4 import QtGui, uic
from PyQt4.QtCore import pyqtSignal

from qgis.gui import *
import processing
import resources
from . import utility_functions as uf

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'criminal_counter_dockwidget_base.ui'))


class criminal_counterDockWidget(QtGui.QDockWidget, FORM_CLASS):

    closingPlugin = pyqtSignal()

    def __init__(self, parent=None):
        """Constructor."""
        super(criminal_counterDockWidget, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
<<<<<<< HEAD
        # define globals
        self.iface = iface
        self.canvas = self.iface.mapCanvas()


=======
        self.iface = iface
        self.canvas = self.iface.mapCanvas()

        # tab case input
>>>>>>> a5d111247a558ec8894b041745bebf8f5b29c789
        self.iface.projectRead.connect(self.loadLayers)
        self.iface.newProjectCreated.connect(self.loadLayers)
        self.iface.legendInterface().itemRemoved.connect(self.loadLayers)
        self.iface.legendInterface().itemAdded.connect(self.loadLayers)
        self.comboBox_Rank.activated.connect(self.setSelectedObject)
        self.comboBox_Time.activated.connect(self.setSelectedObject)

        # tab analysis


        # tab report


    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()

###
#Incidents input
###
    def loadLayers(self):
<<<<<<< HEAD
        self.comboBox_Rank.clear()
        self.comboBox_Time.clear()
=======
        # load incidents layer and initialize two combobox
>>>>>>> a5d111247a558ec8894b041745bebf8f5b29c789
        incident_layernm = "Incidents"
        incident_layer = uf.getLegendLayerByName(self.iface, incident_layernm)
        self.setOriginalCombox(incident_layer)

    def setOriginalCombox(self, layer):
<<<<<<< HEAD
        if uf.fieldExists(layer, "Urgency_R") and uf.fieldExists(layer, "Time"):
            # get rank items and add them to combobox
            #rank, ids_rank = uf.getFieldValues(layer, "Urgency_R")
            #sorted_rank = self.orderbyAttribute(rank, ids_rank)

            #self.comboBox_Rank.addItems(rank)




            # get time items and add them to combobox
            time, ids_time = uf.getFieldValues(layer, "Time")
            #sorted_time = self.orderbyAttribute(time, ids_time)
            self.comboBox_Time.addItems(time)
=======
        # initialize comboboxes based on order of rank or time
        rank_fieldnm = "Urgency_R"
        time_fieldnm = "Time"
        if uf.fieldExists(layer, rank_fieldnm) and uf.fieldExists(layer, time_fieldnm):
            sorted_rank = self.orderbyAttribute(layer, rank_fieldnm)
            sorted_time = self.orderbyAttribute(layer, time_fieldnm)
            self.comboBox_Rank.addItems(sorted_rank)
            self.comboBox_Time.addItems(sorted_time)
>>>>>>> a5d111247a558ec8894b041745bebf8f5b29c789
        else:
            return

    def orderbyAttribute(self, layer, attributenm):
        # order the incidents according to one attribute
        # return the sorted list of case info
        attribute, ids = uf.getFieldValues(layer, attributenm)
        tp_sorted = sorted(zip(attribute,ids))
        lst_sorted_id = []
        for item in tp_sorted:
            lst_sorted_id.append(item[1])
        incidents_info = []
        for ids in lst_sorted_id:
            for feat in layer.getFeatures():
                if ids == feat.id():
                    incidents_info.append(feat.attributes()[4])
        return incidents_info

    def setSelectedObject(self):
        pass

