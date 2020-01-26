from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QDialog, QMessageBox
from getports import get_ports
from ports import *
import os, configparser ,upnpclient, sys

scriptDir = os.path.dirname(os.path.realpath(__file__))

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        icon = QtGui.QIcon(scriptDir + os.path.sep + "icon.png")
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.TableList = QtWidgets.QTableWidget(self.centralwidget)
        self.TableList.setGeometry(QtCore.QRect(10, 260, 781, 311))
        self.TableList.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.TableList.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.TableList.setObjectName("TableList")
        self.TableList.setColumnCount(0)
        self.TableList.setRowCount(0)
        self.TableList.verticalHeader().setVisible(False)
        self.listLable = QtWidgets.QLabel(self.centralwidget)
        self.listLable.setGeometry(QtCore.QRect(290, 220, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.listLable.setFont(font)
        self.listLable.setTextFormat(QtCore.Qt.AutoText)
        self.listLable.setScaledContents(False)
        self.listLable.setAlignment(QtCore.Qt.AlignCenter)
        self.listLable.setObjectName("listLable")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 20, 781, 61))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.op_layout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.op_layout.setContentsMargins(0, 0, 0, 0)
        self.op_layout.setObjectName("op_layout")
        self.oplable = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.oplable.setFont(font)
        self.oplable.setObjectName("oplable")
        self.op_layout.addWidget(self.oplable)
        self.op_name = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.op_name.setMaxLength(20)
        self.op_name.setObjectName("op_name")
        self.op_layout.addWidget(self.op_name)
        self.op_port = QtWidgets.QSpinBox(self.horizontalLayoutWidget)
        self.op_port.setMinimum(0)
        self.op_port.setMaximum(99999)
        self.op_port.setObjectName("op_port")
        self.op_layout.addWidget(self.op_port)
        self.op_drop = QtWidgets.QComboBox(self.horizontalLayoutWidget)
        self.op_drop.setCurrentText("")
        self.op_drop.setObjectName("op_drop")
        self.op_layout.addWidget(self.op_drop)
        self.op_button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.op_button.setObjectName("op_button")
        self.op_layout.addWidget(self.op_button)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(10, 100, 271, 61))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.cp_layout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.cp_layout.setContentsMargins(0, 0, 0, 0)
        self.cp_layout.setObjectName("cp_layout")
        self.cplable = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.cplable.setFont(font)
        self.cplable.setObjectName("cplable")
        self.cp_layout.addWidget(self.cplable)
        self.cpdrop = QtWidgets.QComboBox(self.horizontalLayoutWidget_2)
        self.cpdrop.setObjectName("cpdrop")
        self.cp_layout.addWidget(self.cpdrop)
        self.cp_button = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.cp_button.setObjectName("cp_button")
        self.cp_layout.addWidget(self.cp_button)
        self.button_reload = QtWidgets.QPushButton(self.centralwidget)
        self.button_reload.setGeometry(QtCore.QRect(694, 222, 91, 31))
        self.button_reload.setObjectName("button_reload")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.button_reload.clicked.connect(self.reload)
        self.cp_button.clicked.connect(self.close_port_b)
        self.op_button.clicked.connect(self.port_open)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Port Opener"))
        self.listLable.setText(_translate("MainWindow", "Already Open Ports"))
        self.oplable.setText(_translate("MainWindow", "Open Port:"))
        self.op_name.setPlaceholderText(_translate("MainWindow", "Name"))
        self.op_port.setPrefix(_translate("MainWindow", "Port: "))
        self.op_button.setText(_translate("MainWindow", "Open"))
        self.cplable.setText(_translate("MainWindow", "Close Port:"))
        self.cp_button.setText(_translate("MainWindow", "Close"))
        self.button_reload.setText(_translate("MainWindow", "Reload"))

    def startup(self):
        global port
        global ip

        config = configparser.ConfigParser()
        try:
            config.read(scriptDir + os.path.sep + "config.ini")
            up = config.get("SETTINGS", "ip")
            d = upnpclient.Device(up)
        except:
            Ui_MainWindow.error_message("No IP given please edit configfile")
            exit()

        port = get_ports(d)
        ip = get_ip()

    def error_message(message):
        box = QMessageBox()
        box.setWindowTitle("Error")
        box.setText(message)
        box.setStandardButtons(QMessageBox.Ok)
        returnValue = box.exec()

    def reload(self):
        global port
        global ip
        port = get_ports(d)
        ip = get_ip()
        ui.set_table()
        ui.set_cp_drop()

    def set_table(self):
        self.TableList.setRowCount(port["Count"])
        self.TableList.setColumnCount(4)
        self.TableList.setHorizontalHeaderLabels(["Name", "Port", "Protokoll", "IP"])
        for i in range(port["Count"]):
            a = port[i]
            self.TableList.setItem(i,0, QTableWidgetItem(a['NewPortMappingDescription']))
            self.TableList.setItem(i,1, QTableWidgetItem(str(a['NewExternalPort'])))
            self.TableList.setItem(i,2, QTableWidgetItem(a['NewProtocol']))
            self.TableList.setItem(i,3, QTableWidgetItem(a['NewInternalClient']))
        self.TableList.resizeColumnsToContents()

    def set_cp_drop(self):
        self.cpdrop.clear()
        self.op_drop.clear()
        self.op_drop.addItems(["TCP", "UDP"])
        for i in range(port["Count"]):
            a = port[i]
            self.cpdrop.addItem(str(a['NewExternalPort']) + " " + a["NewProtocol"])

    def close_port_b(self):
        item = self.cpdrop.currentText()
        if item == "":
            Ui_MainWindow.error_message("No item Selected")
            return "error"
        ritem = item[:-4]
        close_port(ritem, item[-3:], d)
        ui.reload()

    def port_open(self):
        name = self.op_name.text()
        ports = self.op_port.value()
        protocol = self.op_drop.currentText()
        if name == "":
            Ui_MainWindow.error_message("No port name given")
            return "name"
        if ports == 0:
            Ui_MainWindow.error_message("No portnumber given")
            return "port"
        open_port(ip, ports, protocol, name, d)
        self.op_name.clear()
        self.op_port.setValue(0)
        ui.reload()



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.startup()
    ui.set_table()
    ui.set_cp_drop()
    MainWindow.show()
    sys.exit(app.exec_())
