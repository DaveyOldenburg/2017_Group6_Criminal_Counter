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


        self.selectLayerCombo.activated.connect(self.setSelectedLayer)
        # tab case input
        self.iface.projectRead.connect(self.loadLayers)
        self.iface.newProjectCreated.connect(self.loadLayers)
        self.iface.legendInterface().itemRemoved.connect(self.loadLayers)
        self.iface.legendInterface().itemAdded.connect(self.loadLayers)
        self.comboBox_Rank.activated.connect(self.setSelectedObject)
        self.comboBox_Time.activated.connect(self.setSelectedObject)

<<<<<<< HEAD
        self.button_NodeSelect.clicked.connect(self.buildNetwork)
=======
>>>>>>> 4657de90cd6eaea8b1281af0182c90507ac48735

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
        tp_sorted = sorted(zip(attribute,ids))
        lst_sorted_id = []
        for item in tp_sorted:
            lst_sorted_id.append(item[1])
        incidents_info = []
        for ids in lst_sorted_id:
            for feat in layer.getFeatures():
                if ids == feat.id():
                    incidents_info.append(feat.attributes()[6])
        return incidents_info

    def setSelectedObject(self):
        pass


<<<<<<< HEAD

    def calculateBuffer(self):
        #takes incident as input
        origins = incident
        layer = self.getSelectedLayer()
        if origins > 0:
            cutoff_distance = 0.05
            buffers = {}
            for point in origins:
                geom = point.geometry()
                buffers[point.id()] = geom.buffer(cutoff_distance,12).asPolygon()
            # store the buffer results in temporary layer called "Buffers"
            buffer_layer = uf.getLegendLayerByName(self.iface, "Buffers")
            # create one if it doesn't exist
            if not buffer_layer:
                attribs = ['id', 'distance']
                types = [QtCore.QVariant.String, QtCore.QVariant.Double]
                buffer_layer = uf.createTempLayer('Buffers','POLYGON',layer.crs().postgisSrid(), attribs, types)
                uf.loadTempLayer(buffer_layer)
                buffer_layer.setLayerName('Buffers')
            # insert buffer polygons
            geoms = []
            values = []
            for buffer in buffers.iteritems():
                # each buffer has an id and a geometry
                geoms.append(buffer[1])
                # in the case of values, it expects a list of multiple values in each item - list of lists
                values.append([buffer[0],cutoff_distance])
            uf.insertTempFeatures(buffer_layer, geoms, values)
            self.refreshCanvas(buffer_layer)

    def getSelectedLayer(self):
        layer_name = self.selectLayerCombo.currentText()
        layer = uf.getLegendLayerByName(self.iface,layer_name)
        return layer


    def getNetwork(self):
        roads_layer = self.getSelectedLayer()
        if roads_layer:
            # see if there is an obstacles layer to subtract roads from the network
            obstacles_layer = uf.getLegendLayerByName(self.iface, "Roads_Rotterdamcut")
            if obstacles_layer:
                # retrieve roads outside obstacles (inside = False)
                features = uf.getFeaturesByIntersection(roads_layer, obstacles_layer, False)
                # add these roads to a new temporary layer
                road_network = uf.createTempLayer('Temp_Network','LINESTRING',roads_layer.crs().postgisSrid(),[],[])
                road_network.dataProvider().addFeatures(features)
            else:
                road_network = roads_layer
            return road_network
        else:
            return

    def buildNetwork(self):
        self.network_layer = self.getNetwork()
        if self.network_layer:
            # get the points to be used as origin and destination
            # in this case gets the centroid of the selected features
            selected_sources = self.getSelectedLayer().selectedFeatures()
            source_points = [feature.geometry().centroid().asPoint() for feature in selected_sources]
            # build the graph including these points
            if len(source_points) > 1:
                self.graph, self.tied_points = uf.makeUndirectedGraph(self.network_layer, source_points)
                # the tied points are the new source_points on the graph
                if self.graph and self.tied_points:
                    text = "network is built for %s points" % len(self.tied_points)
                    self.insertReport(text)
        return
=======
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
>>>>>>> 4657de90cd6eaea8b1281af0182c90507ac48735
