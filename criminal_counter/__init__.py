# -*- coding: utf-8 -*-
"""
/***************************************************************************
 criminal_counter
                                 A QGIS plugin
 This plugin helps the policeman on duty to catch criminals
                             -------------------
        begin                : 2018-01-07
        copyright            : (C) 2018 by group6
        email                : ^dushenglan940128@163.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load criminal_counter class from file criminal_counter.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .criminal_counter import criminal_counter
    return criminal_counter(iface)
