#!/usr/bin/python

import re
import sys
import ip_helper
from PyQt4 import QtGui

class GUI(QtGui.QWidget):
    
    def __init__(self):
        super(GUI, self).__init__()

        self.ip_edit = QtGui.QLineEdit()
        self.prefix_edit = QtGui.QLineEdit()
        self.grid = QtGui.QGridLayout()
        self.error_box = QtGui.QVBoxLayout()
        self.result_box = QtGui.QVBoxLayout()

        self.ip_error = QtGui.QLabel('')
        self.prefix_error = QtGui.QLabel('')
        
        self.error_box.addWidget(self.ip_error)
        self.error_box.addWidget(self.prefix_error)

        for i in reversed (range(self.error_box.count())): 
            self.error_box.itemAt(i).widget().setStyleSheet('QLabel {color: red}')

        self.subnet = QtGui.QLabel('')
        self.first_host = QtGui.QLabel('')
        self.last_host = QtGui.QLabel('')
        self.broadcast = QtGui.QLabel('')
        self.subnet_mask = QtGui.QLabel('')
    
        self.result_box.addWidget(self.subnet)
        self.result_box.addWidget(self.first_host)
        self.result_box.addWidget(self.last_host)
        self.result_box.addWidget(self.broadcast)
        self.result_box.addWidget(self.subnet_mask)

        for i in reversed (range(self.result_box.count())): 
            self.result_box.itemAt(i).widget().setStyleSheet('QLabel {color: blue}')

        self.grid.setSpacing(6)

        self.initUI()

    def initUI(self):
        ip = QtGui.QLabel('IP')
        prefix = QtGui.QLabel('Prefix')

        self.grid.addWidget(ip, 0, 0)
        self.grid.addWidget(self.ip_edit, 0, 1)

        self.grid.addWidget(prefix, 1, 0)
        self.grid.addWidget(self.prefix_edit, 1, 1)

        calculate_button = QtGui.QPushButton("Calculate")
        calculate_button.clicked.connect(self.button_clicked)
        
        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(calculate_button)

        subnet_label = QtGui.QLabel('Subnet')
        first_host_label = QtGui.QLabel('First Host')
        last_host_label = QtGui.QLabel('Last Host')
        broadcast_label = QtGui.QLabel('Broadcast')
        subnet_mask_label = QtGui.QLabel('Subnet Mask')
       
        result_label_box = QtGui.QVBoxLayout()
        result_label_box.addWidget(subnet_label)
        result_label_box.addWidget(first_host_label)
        result_label_box.addWidget(last_host_label)
        result_label_box.addWidget(broadcast_label)
        result_label_box.addWidget(subnet_mask_label)

        self.grid.addLayout(hbox, 2, 1)
        self.grid.addLayout(self.error_box, 3, 1)
        self.grid.addLayout(result_label_box, 4, 0)
        self.grid.addLayout(self.result_box, 4, 1)

        self.setLayout(self.grid)
        self.resize(320,0)
        self.move(300,300)
        self.setWindowTitle('CS725 HW1')

        self.show()

    def button_clicked(self):
        for i in reversed (range(self.error_box.count())): 
            self.error_box.itemAt(i).widget().setText('')
            
        for i in reversed (range(self.result_box.count())): 
            self.result_box.itemAt(i).widget().setText('')

        ip = str(self.ip_edit.text())
        prefix = str(self.prefix_edit.text())

        errors = []

        try:
            ip = ip_helper.format_ip(ip)
        except Exception, e:
            self.ip_error.setText(str(e))
            errors += [e]

        try: 
            prefix = ip_helper.format_prefix(prefix)
        except Exception, e:
            self.prefix_error.setText(str(e))
            errors += [e]
        

        if not errors:
            subnet_mask = ip_helper.get_subnet_mask(prefix)
            subnet = ip_helper.get_subnet_addr(ip, subnet_mask)
            broadcast = ip_helper.get_broadcast(ip, prefix)
            first = ip_helper.get_first_host(subnet)
            last = ip_helper.get_last_host(broadcast)

            self.subnet.setText(ip_helper.format_output(subnet))
            self.first_host.setText(ip_helper.format_output(first))
            self.last_host.setText(ip_helper.format_output(last))
            self.subnet_mask.setText(ip_helper.format_output(subnet_mask))
            self.broadcast.setText(ip_helper.format_output(broadcast))

        self.repaint()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    gui = GUI()
    sys.exit(app.exec_())


