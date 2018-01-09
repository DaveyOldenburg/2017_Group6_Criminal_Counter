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
from PyQt4.QtCore import pyqtSignal, QVariant

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

        # define globals
        self.iface = iface
        self.canvas = self.iface.mapCanvas()

        # tab case input
        self.iface.projectRead.connect(self.loadLayers)
        self.iface.newProjectCreated.connect(self.loadLayers)
        self.iface.legendInterface().itemRemoved.connect(self.loadLayers)
        self.iface.legendInterface().itemAdded.connect(self.loadLayers)
        self.comboBox_Rank.activated.connect(self.setCasebyRank)
        self.comboBox_Time.activated.connect(self.setCasebyTime)


        # tab analysis
        self.button_NodeSelect.clicked.connect(self.createnodes)
        self.button_add.clicked.connect(self.addnode)



        self.emitPoint = QgsMapToolEmitPoint(self.canvas)
        self.emitPoint.canvasClicked.connect(self.getPoint)
        # tab report

        # initialisation
        self.loadLayers()


    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()

###
#Incidents input
###
    def loadLayers(self):

        self.comboBox_Rank.clear()
        self.comboBox_Time.clear()

        # load incidents layer and initialize two combobox

        incident_layernm = "Incidents"
        incident_layer = uf.getLegendLayerByName(self.iface, incident_layernm)
        self.setOriginalCombox(incident_layer)

    def setOriginalCombox(self, layer):

        # initialize comboboxes based on order of rank or time
        rank_fieldnm = "Urgency_R"
        time_fieldnm = "Time"

        if uf.fieldExists(layer, rank_fieldnm) and uf.fieldExists(layer, time_fieldnm):
            sorted_rank = self.orderbyAttribute(layer, rank_fieldnm)
            sorted_time = self.orderbyAttribute(layer, time_fieldnm)
            self.comboBox_Rank.addItems(sorted_rank)
            self.comboBox_Time.addItems(sorted_time)
        else:
            return

    def orderbyAttribute(self, layer, attributenm):
        # order the incidents according to one attribute
        # return the sorted list of case info
        attribute, ids = uf.getFieldValues(layer, attributenm)
        tp_sorted = sorted(zip(attribute,ids), reverse = True)
        lst_sorted_id = []
        for item in tp_sorted:
            lst_sorted_id.append(item[1])
        incidents_info = []
        for ids in lst_sorted_id:
            for feat in layer.getFeatures():
                if ids == feat.id():
                    incidents_info.append(feat.attributes()[6])
        return incidents_info

    def setCasebyRank(self):
        case_no = self.comboBox_Rank.currentText()
        self.writeCaseList(case_no)

    def setCasebyTime(self):
        case_no = self.comboBox_Time.currentText()
        self.writeCaseList(case_no)

    def writeCaseList(self, caseno):
        self.list_case.clear()
        layer = uf.getLegendLayerByName(self.iface,"Incidents")
        case_info = []
        for feat in layer.getFeatures():
            att = feat.attributes()[6]
            if att == caseno:
                case_info.append("rank: " + str(feat.attributes()[0]))
                case_info.append("criminal id: " + str(feat.attributes()[1]))
                case_info.append("criminal information: " + feat.attributes()[2])
                case_info.append("case information: " + feat.attributes()[3])
                case_info.append("case name: " + feat.attributes()[4])
                case_info.append("time: " + feat.attributes()[5])
                case_info.append("case number: " + feat.attributes()[6])
                self.list_case.addItems(case_info)
                break


###
# Node Input
###
    def createnodes(self):
        #Create temp layer "Nodes"
        layer=uf.getLegendLayerByName(self.iface,"Policemen")

        nodes=uf.getLegendLayerByName(self.iface, 'Nodes')
        if not nodes:
            attribs = ["id"]
            types = [QtCore.QVariant.String]
            nodes=QgsVectorLayer('Point?crs=epsg:28992', 'Nodes', 'memory')
            uf.addFields(nodes, ['id'], [QVariant.String])
            uf.loadTempLayer(nodes)
            nodes.setLayerName('Nodes')
        nodes.startEditing()


    def addnode(self):
        # remember currently selected tool
        self.userTool = self.canvas.mapTool()
        # activate coordinate capture tool
        self.canvas.setMapTool(self.emitPoint)


    def getPoint(self, mapPoint, mouseButton):
        # change tool so you don't get more than one POI
        self.canvas.unsetMapTool(self.emitPoint)
        self.canvas.setMapTool(self.userTool)
        #Get the click
        if mapPoint:
            # here do something with the point
            nodes = uf.getLegendLayerByName(self.iface, "Nodes")
            pr=nodes.dataProvider()


            fet=QgsFeature()
            fet.setGeometry(QgsGeometry.fromPoint(mapPoint))
            #fet.setAttributes(['1']), no setting attributes for now
            pr.addFeatures([fet])

            nodes.commitChanges()
            self.refreshCanvas(nodes)


    #refresh canvas after changes
    def refreshCanvas(self, layer):
        if self.canvas.isCachingEnabled():
            layer.setCacheImage(None)
        else:
            self.canvas.refresh()
