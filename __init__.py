# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Colindantes
                                 A QGIS plugin
 This plugin gets information about 
                             -------------------
        begin                : 2018-03-30
        copyright            : (C) 2018 by 20171094013 / 20171094014
        email                : jppullidov@correo.udistrital.edu.co
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
    """Load Colindantes class from file Colindantes.

    :param iface: A QGIS interface instance.
    :type iface: QgisInterface
    """
    #
    from .colindantes import Colindantes
    return Colindantes(iface)
