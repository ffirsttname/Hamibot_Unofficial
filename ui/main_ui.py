# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Hamibot_UIYUPXZc.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(671, 433)
        MainWindow.setToolButtonStyle(Qt.ToolButtonIconOnly)
        MainWindow.setAnimated(True)
        MainWindow.setDockOptions(QMainWindow.AllowTabbedDocks|QMainWindow.AnimatedDocks)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(0, 0, 671, 401))
        self.tabWidget.setMaximumSize(QSize(671, 401))
        font = QFont()
        font.setFamily(u"Noto Sans SC Medium")
        font.setPointSize(12)
        self.tabWidget.setFont(font)
        self.robots_list = QWidget()
        self.robots_list.setObjectName(u"robots_list")
        self.robots_table = QTableWidget(self.robots_list)
        if (self.robots_table.columnCount() < 5):
            self.robots_table.setColumnCount(5)
        __qtablewidgetitem = QTableWidgetItem()
        self.robots_table.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.robots_table.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.robots_table.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.robots_table.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.robots_table.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        self.robots_table.setObjectName(u"robots_table")
        self.robots_table.setGeometry(QRect(0, 0, 671, 371))
        self.robots_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.robots_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.robots_table.setTextElideMode(Qt.ElideMiddle)
        self.robots_table.setColumnCount(5)
        self.robots_table.horizontalHeader().setVisible(False)
        self.robots_table.verticalHeader().setVisible(False)
        self.tabWidget.addTab(self.robots_list, "")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.dev_script_table = QTableWidget(self.tab)
        if (self.dev_script_table.columnCount() < 2):
            self.dev_script_table.setColumnCount(2)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.dev_script_table.setHorizontalHeaderItem(0, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.dev_script_table.setHorizontalHeaderItem(1, __qtablewidgetitem6)
        self.dev_script_table.setObjectName(u"dev_script_table")
        self.dev_script_table.setGeometry(QRect(0, 0, 531, 371))
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dev_script_table.sizePolicy().hasHeightForWidth())
        self.dev_script_table.setSizePolicy(sizePolicy)
        self.dev_script_table.setEditTriggers(QAbstractItemView.AnyKeyPressed)
        self.dev_script_table.setAlternatingRowColors(False)
        self.dev_script_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.dev_script_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.dev_script_table.setRowCount(0)
        self.dev_script_table.setColumnCount(2)
        self.dev_script_table.horizontalHeader().setVisible(False)
        self.dev_script_table.horizontalHeader().setCascadingSectionResizes(False)
        self.dev_script_table.horizontalHeader().setHighlightSections(True)
        self.dev_script_table.verticalHeader().setVisible(False)
        self.dev_script_robots_combobox = QComboBox(self.tab)
        self.dev_script_robots_combobox.addItem("")
        self.dev_script_robots_combobox.setObjectName(u"dev_script_robots_combobox")
        self.dev_script_robots_combobox.setGeometry(QRect(550, 10, 103, 31))
        self.dev_script_robots_combobox.setEditable(False)
        self.folder_location = QLineEdit(self.tab)
        self.folder_location.setObjectName(u"folder_location")
        self.folder_location.setGeometry(QRect(538, 240, 91, 29))
        self.edit_dev_script_button = QPushButton(self.tab)
        self.edit_dev_script_button.setObjectName(u"edit_dev_script_button")
        self.edit_dev_script_button.setGeometry(QRect(560, 280, 75, 31))
        self.folder_choose = QLabel(self.tab)
        self.folder_choose.setObjectName(u"folder_choose")
        self.folder_choose.setGeometry(QRect(632, 240, 31, 31))
        self.folder_choose.setPixmap(QPixmap(u":/123/folder.png"))
        self.folder_choose.setScaledContents(True)
        self.dev_script_edit_config = QCheckBox(self.tab)
        self.dev_script_edit_config.setObjectName(u"dev_script_edit_config")
        self.dev_script_edit_config.setGeometry(QRect(540, 320, 121, 16))
        self.layoutWidget = QWidget(self.tab)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(560, 60, 77, 144))
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.dev_script_run_button = QPushButton(self.layoutWidget)
        self.dev_script_run_button.setObjectName(u"dev_script_run_button")

        self.verticalLayout.addWidget(self.dev_script_run_button)

        self.dev_script_stop_button = QPushButton(self.layoutWidget)
        self.dev_script_stop_button.setObjectName(u"dev_script_stop_button")

        self.verticalLayout.addWidget(self.dev_script_stop_button)

        self.dev_script_stopall_button = QPushButton(self.layoutWidget)
        self.dev_script_stopall_button.setObjectName(u"dev_script_stopall_button")

        self.verticalLayout.addWidget(self.dev_script_stopall_button)

        self.tabWidget.addTab(self.tab, "")
        self.setting = QWidget()
        self.setting.setObjectName(u"setting")
        self.layoutWidget1 = QWidget(self.setting)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(1, 0, 661, 31))
        self.horizontalLayout = QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.layoutWidget1)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.tokens = QLineEdit(self.layoutWidget1)
        self.tokens.setObjectName(u"tokens")

        self.horizontalLayout.addWidget(self.tokens)

        self.get_tokens_url = QLabel(self.layoutWidget1)
        self.get_tokens_url.setObjectName(u"get_tokens_url")
        palette = QPalette()
        brush = QBrush(QColor(0, 0, 0, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.WindowText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        brush1 = QBrush(QColor(120, 120, 120, 255))
        brush1.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.WindowText, brush1)
        self.get_tokens_url.setPalette(palette)
        self.get_tokens_url.setFocusPolicy(Qt.NoFocus)
        self.get_tokens_url.setOpenExternalLinks(True)

        self.horizontalLayout.addWidget(self.get_tokens_url)

        self.layoutWidget2 = QWidget(self.setting)
        self.layoutWidget2.setObjectName(u"layoutWidget2")
        self.layoutWidget2.setGeometry(QRect(0, 40, 208, 31))
        self.horizontalLayout_3 = QHBoxLayout(self.layoutWidget2)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.language_switch = QComboBox(self.layoutWidget2)
        self.language_switch.addItem("")
        self.language_switch.addItem("")
        self.language_switch.addItem("")
        self.language_switch.setObjectName(u"language_switch")

        self.horizontalLayout_3.addWidget(self.language_switch)

        self.lower_api_quotas = QCheckBox(self.layoutWidget2)
        self.lower_api_quotas.setObjectName(u"lower_api_quotas")

        self.horizontalLayout_3.addWidget(self.lower_api_quotas)

        self.tabWidget.addTab(self.setting, "")
        self.log_bar = QLabel(self.centralwidget)
        self.log_bar.setObjectName(u"log_bar")
        self.log_bar.setGeometry(QRect(5, 400, 660, 31))
        self.log_bar.setFont(font)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 671, 21))
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Hamibot_UI（非官方）", None))
        ___qtablewidgetitem = self.robots_table.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"id", None));
        ___qtablewidgetitem1 = self.robots_table.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"名字", None));
        ___qtablewidgetitem2 = self.robots_table.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"型號", None));
        ___qtablewidgetitem3 = self.robots_table.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"狀態", None));
        ___qtablewidgetitem4 = self.robots_table.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"標籤", None));
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.robots_list), QCoreApplication.translate("MainWindow", u"機械人", None))
        ___qtablewidgetitem5 = self.dev_script_table.horizontalHeaderItem(0)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"id", None));
        ___qtablewidgetitem6 = self.dev_script_table.horizontalHeaderItem(1)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"名字", None));
        self.dev_script_robots_combobox.setItemText(0, QCoreApplication.translate("MainWindow", u"選擇機械人", None))

        self.dev_script_robots_combobox.setCurrentText(QCoreApplication.translate("MainWindow", u"選擇機械人", None))
        self.edit_dev_script_button.setText(QCoreApplication.translate("MainWindow", u"修改腳本", None))
        self.folder_choose.setText("")
        self.dev_script_edit_config.setText(QCoreApplication.translate("MainWindow", u"修改配置文件", None))
        self.dev_script_run_button.setText(QCoreApplication.translate("MainWindow", u"運行", None))
        self.dev_script_stop_button.setText(QCoreApplication.translate("MainWindow", u"停止", None))
        self.dev_script_stopall_button.setText(QCoreApplication.translate("MainWindow", u"停止所有", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"開發腳本", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"個人訪問令牌 ：", None))
        self.get_tokens_url.setText(QCoreApplication.translate("MainWindow", u"（獲取令牌）", None))
        self.language_switch.setItemText(0, QCoreApplication.translate("MainWindow", u"語言：", None))
        self.language_switch.setItemText(1, QCoreApplication.translate("MainWindow", u"繁體", None))
        self.language_switch.setItemText(2, QCoreApplication.translate("MainWindow", u"简体", None))

        self.lower_api_quotas.setText(QCoreApplication.translate("MainWindow", u"降低配額使用量", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.setting), QCoreApplication.translate("MainWindow", u"設定", None))
        self.log_bar.setText("")
    # retranslateUi

