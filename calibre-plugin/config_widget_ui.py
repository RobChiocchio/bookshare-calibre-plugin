# Form implementation generated from reading ui file '/tmp/tmpw4f01up_robchio/calibre/gui2/config_widget.ui'
#
# Created by: PyQt6 UI code generator 6.5.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(460, 110)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.tags = QtWidgets.QLineEdit(parent=Form)
        self.tags.setObjectName("tags")
        self.gridLayout.addWidget(self.tags, 4, 1, 1, 1)
        self.password = QtWidgets.QLineEdit(parent=Form)
        self.password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.password.setObjectName("password")
        self.gridLayout.addWidget(self.password, 1, 1, 1, 1)
        self.tabs_label = QtWidgets.QLabel(parent=Form)
        self.tabs_label.setObjectName("tabs_label")
        self.gridLayout.addWidget(self.tabs_label, 4, 0, 1, 1)
        self.username = QtWidgets.QLineEdit(parent=Form)
        self.username.setObjectName("username")
        self.gridLayout.addWidget(self.username, 0, 1, 1, 1)
        self.username_label = QtWidgets.QLabel(parent=Form)
        self.username_label.setObjectName("username_label")
        self.gridLayout.addWidget(self.username_label, 0, 0, 1, 1)
        self.open_external = QtWidgets.QCheckBox(parent=Form)
        self.open_external.setObjectName("open_external")
        self.gridLayout.addWidget(self.open_external, 3, 0, 1, 2)
        self.password_label = QtWidgets.QLabel(parent=Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.password_label.sizePolicy().hasHeightForWidth())
        self.password_label.setSizePolicy(sizePolicy)
        self.password_label.setObjectName("password_label")
        self.gridLayout.addWidget(self.password_label, 1, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):

        Form.setWindowTitle(_("Form"))
        self.tabs_label.setText(_("Added tags:"))
        self.username_label.setText(_("Username:"))
        self.open_external.setText(_("Open store in external web browser"))
        self.password_label.setText(_("Password:"))