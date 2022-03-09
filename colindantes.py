# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Colindantes
                                 A QGIS plugin
 This plugin gets information about
                              -------------------
        begin                : 2018-03-30
        git sha              : $Format:%H$
        copyright            : (C) 2018 by 20171094013 / 20171094014
        email                : jppullidov@correo.udistrital.edu.co
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
from PyQt4 import QtGui
from PyQt4.QtGui import *
from PyQt4.QtGui import QAction, QIcon
from PyQt4.QtCore import *
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from qgis.gui import QgsMapToolEmitPoint
from qgis.core import QgsGeometry, QgsMapLayer, QgsVectorLayer, QgsMapLayerRegistry, QgsFeature, QgsField, QgsDistanceArea, QgsPalLayerSettings
from qgis.utils import iface
import processing
import os.path
import numpy as np
import qgis.utils
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from colindantes_dialog import ColindantesDialog


class Colindantes:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgisInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        self.map = self.iface.mapCanvas()
        self.clickTool = QgsMapToolEmitPoint(self.map)
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'Colindantes_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)


        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Colindantes')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'Colindantes')
        self.toolbar.setObjectName(u'Colindantes')


    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('Colindantes', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        # Create the dialog (after translation) and keep reference
        self.dlg = ColindantesDialog()
        self.tblColindante = self.dlg.tblColindante
        self.btnSalir =self.dlg.btnSalir
        self.btnLimpiar = self.dlg.btnLimpiar

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/Colindantes/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u''),
            callback=self.run,
            parent=self.iface.mainWindow())
        self.clickTool.canvasClicked.connect(self.calcularColindantes)
        self.btnSalir.clicked.connect(self.btnSalir_clicked)
        self.btnLimpiar.clicked.connect(self.btnLimpiar_clicked)


    def calcularColindantes(self, point, button):
        try:
            self.base_layers = QgsMapLayerRegistry.instance().mapLayers()
            #Selección del predio con un clic (punto)
            pntGeom = QgsGeometry.fromPoint(point)
            pntBuff = pntGeom.buffer((self.map.mapUnitsPerPixel() * 2),0)
            rect = pntBuff.boundingBox()
        	#Guarda la capa que esta activa
            cLayer = self.map.currentLayer()
        	#Remueve selecciones antiguas
            cLayer.removeSelection()
        	#Selecciona el predio que se cruza con el punto
            cLayer.select(rect, True)
        	#Guarda el predio en una variable
            selFeatures = cLayer.selectedFeatures()
        	#Asigna la geometria a la variable guardada
            geom = selFeatures[0].geometry()
        	#Limpia la seleccion del predio de la capa creada inicialmente
            cLayer.removeSelection()
        	#Buscar el sistema de referencia de la capa
            crs = cLayer.crs().authid()
        	#Crea Layer temporal para guardar los predios vecinos
            tmpLyr = QgsVectorLayer("MultiPolygon?crs="+str(crs),u"Predios Colindantes","memory")
            tmpData = tmpLyr.dataProvider()
        	#Crea Layer temporal para guardar el predio Seleccionado
            tmpSel = QgsVectorLayer("MultiPolygon?crs="+str(crs),u"Predio Seleccionado","memory")
            tmpDataS= tmpSel.dataProvider()
            cAttribute = cLayer.dataProvider().fields().toList()
        	#Crea lista de las columnas de los atributos de la nueva capa
            tmpAttribute = []
            for attribute in cAttribute:
                if tmpLyr.fieldNameIndex(attribute.name())==-1:
                    tmpAttribute.append(QgsField(attribute.name(),attribute.type()))
            tmpData.addAttributes(tmpAttribute)
            tmpLyr.updateFields()
            tmpDataS.addAttributes(tmpAttribute)
            tmpSel.updateFields()
        	#Guarda los atributos de la capa original a la capa temporal de vecinos
            for f in cLayer.getFeatures():
                if geom.touches(f.geometry()) == True:
                    cLayer.select(f.id())
                    tmpLyr.startEditing()
                    ftr = QgsFeature()
                    ftr.setGeometry(f.geometry())
                    ftrAttribute = []
                    ftrAttribute.extend(f.attributes())
                    ftr.setAttributes(ftrAttribute)
                    tmpLyr.addFeature(ftr, True)
                    tmpLyr.commitChanges()
            self.map.zoomToSelected()
        	#Añade al mapa los predios vecinos en geometria poligono
            seleccionados = QgsMapLayerRegistry.instance().addMapLayer(tmpLyr)
        	#Convierte a linea la capa de poligono de los vecinos
            linea = processing.runalg("qgis:polygonstolines",tmpLyr,None)
        	#Añade al mapa la capa de linea de los vecinos
            tmpLine = processing.getObject(linea['OUTPUT'])
            seleccionadosLinea = QgsMapLayerRegistry.instance().addMapLayer(tmpLine)
        	#Guarda los atributos de la capa original a la capa temporal del predio
            for f in cLayer.getFeatures():
                if geom.contains(f.geometry()) == True:
                    cLayer.select(f.id())
                    tmpSel.startEditing()
                    ftrs = QgsFeature()
                    ftrs.setGeometry(f.geometry())
                    ftrsAttribute = []
                    ftrsAttribute.extend(f.attributes())
                    ftrs.setAttributes(ftrsAttribute)
                    tmpSel.addFeature(ftrs, True)
                    tmpSel.commitChanges()
                    #Mostrar cedula catastral del predio seleccionado
                    self.dlg.lineEdit.setText(str(f[10]))
        	#Limpia la seleccion del predio de la capa creada inicialmente
            cLayer.removeSelection()
        	#Añade al mapa los predios vecinos en geometria poligono
            seleccionado = QgsMapLayerRegistry.instance().addMapLayer(tmpSel)
        	#Intersecta el predio seleccionado con los vecinos en geometria linea
            lineaPredio = processing.runalg("qgis:intersection", seleccionadosLinea, seleccionado, False, None)
            tmpLinePredio = processing.getObject(lineaPredio['OUTPUT'])
            colindanteLinea = QgsMapLayerRegistry.instance().addMapLayer(tmpLinePredio)
            #Polilineas y Multipolilineas son tomados de colindanteLinea
            # Cada feature es un track
            multipolylines_features = [x for x in colindanteLinea.getFeatures() if x.geometry().asMultiPolyline()!=[]]
            multipolylines = [x.geometry().asMultiPolyline() for x in multipolylines_features]
            polylines_features = [x for x in colindanteLinea.getFeatures() if x.geometry().asPolyline()!=[]]
            polylines = [x.geometry().asPolyline() for x in polylines_features]
            #Polilineas de multipolilineas
            new_polylines = [[multipolyline[0][0],multipolyline[-1][1]] for multipolyline in multipolylines]
            for x in new_polylines:
                polylines.append(x)
            polylines_keys = [str(key) for key in polylines]
            #Ordenar polilineas
            length = len(polylines)
            ordered_polylines = []
            line = polylines.pop(0)
            ordered_polylines.append(line)
            for i in range(length-1):
                starts = np.array([x[0] for x in polylines])
                index = starts==line[1]
                n = np.arange(len(starts))[index[:,0]][0]
                line = polylines.pop(n)
                ordered_polylines.append(line)
            # Diccionario de Features dictionarycon lienas como llave:
            for feature in multipolylines_features:
                polylines_features.append(feature)
            geo_dictionary = dict(zip(polylines_keys, polylines_features))
            ordered_features = [[key, geo_dictionary[str(key)]] for key in ordered_polylines]
            # Intersecta las lineas de los predios vecinos con el seleccionado
            # Se generan los vertices
            vertice = processing.runalg("qgis:lineintersections", seleccionadosLinea, colindanteLinea, None, None, None)
            tmpvertice = processing.getObject(vertice['OUTPUT'])
            vertices = QgsMapLayerRegistry.instance().addMapLayer(tmpvertice)
            #Adicionar campo id en la capa de vertice
            vertices.dataProvider().addAttributes([QgsField("id", QVariant.Double)])
            vertices.updateFields()
            i=1
            vertices.startEditing()
            for f in vertices.getFeatures():
                if f.id()%2 == 0:
                    f[2]= int(i)
                    vertices.updateFeature(f)
                    i=i+1
            vertices.commitChanges()
            #Mostrar Label
            label = QgsPalLayerSettings()
            label.readFromLayer(seleccionados)
            label.enabled = True
            label.fieldName = 'PROPIETARI'
            label.placement= QgsPalLayerSettings.AboveLine
            label.setDataDefinedProperty(QgsPalLayerSettings.Size,True,True,'7',"")
            label.writeToLayer(seleccionados)
            QgsMapLayerRegistry.instance().addMapLayers([seleccionados])
            #Mostrar puntos en la tabla
            self.tblColindante.setRowCount(length)
            for i in range(length):
                coord = ordered_features[i][0][0]
                features = ordered_features[i][1]
                self.tblColindante.setItem(i,0, QTableWidgetItem("{}-{}".format(i+1,(i+2)%(length+1)+(i+2)/(length+1))))
                self.tblColindante.setItem(i,1, QTableWidgetItem(str(coord[0])))
                self.tblColindante.setItem(i,2, QTableWidgetItem(str(coord[1])))
                self.tblColindante.setItem(i,3, QTableWidgetItem(str(features.geometry().length())))
                self.tblColindante.setItem(i,4, QTableWidgetItem(features.attribute('NOMBRE_PRE')))
                self.tblColindante.setItem(i,5, QTableWidgetItem(features.attribute('PROPIETARI')))
            self.tblColindante.show()

        except:
            canvas = qgis.utils.iface.legendInterface()
            layers = QgsMapLayerRegistry.instance().mapLayers()
            count = 0
            for capa in canvas.layers():
                #Anexo a la validacion del formato vector, incluyo la constante 100
                #que corresponde a la constante donde la capa no tiene geometria y
                #solo es de lectura. p.e. un csv
                if (capa.type() == QgsMapLayer.VectorLayer and capa.wkbType() != 100) :
                    count +=1
            for name, layer in layers.iteritems():
                if layer.name() == ('OUTPUT.shp'):
                    count = 1
                else:
                    count = 2

            if (count == 0):
                QtGui.QMessageBox.information(None,"Error","Adicione la capa de Base Predial")

            if (count == 1):
                QtGui.QMessageBox.information(None,"Error","Oprima el boton Limpiar")

            if (count == 2):
                QtGui.QMessageBox.information(None,"Error","Seleccione un predio")


    def btnSalir_clicked(self):
        self.dlg.close()

    def btnLimpiar_clicked(self):
        # Limpia lineas de la tabla
        while (self.tblColindante.rowCount() > 0):
            self.tblColindante.removeRow(0)
        # Limpia referencia de predio
        self.dlg.lineEdit.clear()
        # Elimina capas no base
        layers = QgsMapLayerRegistry.instance().mapLayers()
        layers_to_remove = [layer for layer in layers if layer not in self.base_layers]
        QgsMapLayerRegistry.instance().removeMapLayers(layers_to_remove)

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Colindantes'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def run(self):
        """Run method that performs all the real work"""
        self.map.setMapTool(self.clickTool)
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass

