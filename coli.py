# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'colindantes_dialog_base.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_CalculoLinderosDialogBase(object):
    def setupUi(self, CalculoLinderosDialogBase):
        CalculoLinderosDialogBase.setObjectName(_fromUtf8("CalculoLinderosDialogBase"))
        CalculoLinderosDialogBase.resize(843, 477)
        self.gridLayout = QtGui.QGridLayout(CalculoLinderosDialogBase)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblNumeroC = QtGui.QLabel(CalculoLinderosDialogBase)
        self.lblNumeroC.setObjectName(_fromUtf8("lblNumeroC"))
        self.gridLayout.addWidget(self.lblNumeroC, 0, 0, 1, 1)
        self.tblColindante = QtGui.QTableWidget(CalculoLinderosDialogBase)
        self.tblColindante.setEnabled(True)
        self.tblColindante.setObjectName(_fromUtf8("tblColindante"))
        self.tblColindante.setColumnCount(6)
        self.tblColindante.setRowCount(1)
        item = QtGui.QTableWidgetItem()
        self.tblColindante.setVerticalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tblColindante.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tblColindante.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tblColindante.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tblColindante.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.tblColindante.setHorizontalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.tblColindante.setHorizontalHeaderItem(5, item)
        item = QtGui.QTableWidgetItem()
        self.tblColindante.setItem(0, 0, item)
        item = QtGui.QTableWidgetItem()
        self.tblColindante.setItem(0, 1, item)
        item = QtGui.QTableWidgetItem()
        self.tblColindante.setItem(0, 2, item)
        item = QtGui.QTableWidgetItem()
        self.tblColindante.setItem(0, 3, item)
        item = QtGui.QTableWidgetItem()
        self.tblColindante.setItem(0, 4, item)
        item = QtGui.QTableWidgetItem()
        self.tblColindante.setItem(0, 5, item)
        self.gridLayout.addWidget(self.tblColindante, 1, 0, 1, 4)
        self.btnLimpiar = QtGui.QPushButton(CalculoLinderosDialogBase)
        self.btnLimpiar.setObjectName(_fromUtf8("btnLimpiar"))
        self.gridLayout.addWidget(self.btnLimpiar, 2, 2, 1, 1)
        self.btnSalir = QtGui.QPushButton(CalculoLinderosDialogBase)
        self.btnSalir.setObjectName(_fromUtf8("btnSalir"))
        self.gridLayout.addWidget(self.btnSalir, 2, 3, 1, 1)
        self.lineEdit = QtGui.QLineEdit(CalculoLinderosDialogBase)
        self.lineEdit.setEnabled(False)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 3)

        self.retranslateUi(CalculoLinderosDialogBase)
        QtCore.QMetaObject.connectSlotsByName(CalculoLinderosDialogBase)

    def retranslateUi(self, CalculoLinderosDialogBase):
        CalculoLinderosDialogBase.setWindowTitle(_translate("CalculoLinderosDialogBase", "Calculo Linderos", None))
        self.lblNumeroC.setText(_translate("CalculoLinderosDialogBase", "Número Catastral del Predio Seleccionado", None))
        item = self.tblColindante.verticalHeaderItem(0)
        item.setText(_translate("CalculoLinderosDialogBase", "1", None))
        item = self.tblColindante.horizontalHeaderItem(0)
        item.setText(_translate("CalculoLinderosDialogBase", "Vértice", None))
        item = self.tblColindante.horizontalHeaderItem(1)
        item.setText(_translate("CalculoLinderosDialogBase", "Coordenada Este", None))
        item = self.tblColindante.horizontalHeaderItem(2)
        item.setText(_translate("CalculoLinderosDialogBase", "Coordenada Norte", None))
        item = self.tblColindante.horizontalHeaderItem(3)
        item.setText(_translate("CalculoLinderosDialogBase", "Colindancia", None))
        item = self.tblColindante.horizontalHeaderItem(4)
        item.setText(_translate("CalculoLinderosDialogBase", "Distancia", None))
        item = self.tblColindante.horizontalHeaderItem(5)
        item.setText(_translate("CalculoLinderosDialogBase", "Nombre Colindante", None))
        __sortingEnabled = self.tblColindante.isSortingEnabled()
        self.tblColindante.setSortingEnabled(False)
        item = self.tblColindante.item(0, 0)
        item.setText(_translate("CalculoLinderosDialogBase", "aaaa", None))
        item = self.tblColindante.item(0, 1)
        item.setText(_translate("CalculoLinderosDialogBase", "eeee", None))
        item = self.tblColindante.item(0, 2)
        item.setText(_translate("CalculoLinderosDialogBase", "uuu", None))
        item = self.tblColindante.item(0, 3)
        item.setText(_translate("CalculoLinderosDialogBase", "iiii", None))
        item = self.tblColindante.item(0, 4)
        item.setText(_translate("CalculoLinderosDialogBase", ",,,,", None))
        item = self.tblColindante.item(0, 5)
        item.setText(_translate("CalculoLinderosDialogBase", "....", None))
        self.tblColindante.setSortingEnabled(__sortingEnabled)
        self.btnLimpiar.setText(_translate("CalculoLinderosDialogBase", "Limpiar", None))
        self.btnSalir.setText(_translate("CalculoLinderosDialogBase", "Cerrar", None))

